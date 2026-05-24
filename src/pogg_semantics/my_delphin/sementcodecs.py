"""
Serialization functions for the SEMENT format.
Code directly taken from pydelphin with small changes to account for the additional EQ and SLOT features of a SEMENT.

Ideally will be merged with pydelphin and maybe some redundancy can be eliminated, but for now just copied.

[See usage examples here.](project:/usage_nbs/pogg/my_delphin/sementcodecs_usage.ipynb)
"""

import re
from pathlib import Path
from typing import Optional

from delphin import predicate, variable
from delphin.lnk import Lnk
from delphin.mrs import CONSTANT_ROLE, EP, HCons, ICons, MRSSyntaxError
from pogg.my_delphin.my_delphin import SEMENT
from delphin.sembase import property_priority, role_priority
from delphin.util import Lexer

CODEC_INFO = {
    'representation': 'mrs',
}


TOP_FEATURE = 'TOP'


##############################################################################
##############################################################################
# Pickle-API methods


def load(source):
    """
    Deserialize SEMENTs from a file (handle or filename)

    Args:
        source (str, file): input filename or file object
    Returns:
        a list of MRS objects
    """
    if hasattr(source, 'read'):
        ms = list(_decode(source))
    else:
        source = Path(source).expanduser()
        with source.open() as fh:
            ms = list(_decode(fh))
    return ms


def loads(s):
    """
    Deserialize SEMENT string representations

    Args:
        s (str): a SEMENT string
    Returns:
        a list of MRS objects
    """
    ms = list(_decode(s.splitlines()))
    return ms


def dump(ms, destination, properties=True, lnk=True,
         indent=False, encoding='utf-8'):
    """
    Serialize MRS objects to SEMENT and write to a file

    Args:
        ms: an iterator of MRS objects to serialize
        destination: filename or file object where data will be written
        properties: if `False`, suppress morphosemantic properties
        lnk: if `False`, suppress surface alignments and strings
        indent (bool, int): if `True` or an integer value, add newlines and indentation
        encoding (str): if *destination* is a filename, write to the file with the given encoding; otherwise it is ignored
    """
    text = dumps(ms, properties=properties, lnk=lnk, indent=indent)
    if hasattr(destination, 'write'):
        print(text, file=destination)
    else:
        destination = Path(destination).expanduser()
        with destination.open('w', encoding=encoding) as fh:
            print(text, file=fh)


def dumps(ms, properties=True, lnk=True, indent=False):
    """
    Serialize MRS objects to a SEMENT representation

    Args:
        ms: an iterator of MRS objects to serialize
        properties: if `False`, suppress variable properties
        lnk: if `False`, suppress surface alignments and strings
        indent (bool, int): if `True` or an integer value, add newlines and indentation
    Returns:
        a SEMENT string representation of a corpus of MRS objects
    """
    return _encode(ms, properties, lnk, indent)


def decode(s):
    """
    Deserialize an MRS object from a SEMENT string.
    """
    lexer = SEMENTLexer.lex(s.splitlines())
    return _decode_sement(lexer)


def encode(m, properties=True, lnk=True, indent=False):
    """
    Serialize a MRS object to a SEMENT string.

    Args:
        m: an MRS object
        properties (bool): if `False`, suppress variable properties
        lnk: if `False`, suppress surface alignments and strings
        indent (bool, int): if `True` or an integer value, add newlines and indentation
    Returns:
        a SEMENT-serialization of the MRS object
    """
    return _encode([m], properties, lnk, indent)


##############################################################################
##############################################################################
# Deserialization


SEMENTLexer = Lexer(
    tokens=[
        (r'\[', 'LBRACK:['),
        (r'\]', 'RBRACK:]'),
        (r'<(?:-?\d+[:#]-?\d+'
         r'|@\d+'
         r'|\d+(?: +\d+)*)>', 'LNK:a lnk value'),
        (r'"([^"\\]*(?:\\.[^"\\]*)*)"', 'DQSTRING:a string'),
        (r"'([^ \n:<>\[\]]+)", 'SQSYMBOL:a quoted symbol'),
        (r'_[^\s_]+'  # lemma
         r'_[nvajrscpqxud]'  # pos
         r'(?:_(?:[^\s_<]|<(?![-0-9:#@ ]*>\s))+)?'  # optional sense
         r'(?:_rel)?',  # optional suffix
         'PREDICATE:a surface predicate'),
        (r'<', 'LANGLE:<'),
        (r'>', 'RANGLE:>'),
        (r'([^\s:<>\[\]]+):', 'FEATURE:a feature'),
        (r'(?:[^ \n\]<]+'
         r'|<(?![-0-9:#@ ]*>\s))+', 'SYMBOL:a symbol'),
        (r'[^\s]', 'UNEXPECTED'),
    ],
    error_class=MRSSyntaxError)


LBRACK    = SEMENTLexer.tokentypes.LBRACK
RBRACK    = SEMENTLexer.tokentypes.RBRACK
LNK       = SEMENTLexer.tokentypes.LNK
DQSTRING  = SEMENTLexer.tokentypes.DQSTRING
SQSYMBOL  = SEMENTLexer.tokentypes.SQSYMBOL
PREDICATE = SEMENTLexer.tokentypes.PREDICATE
LANGLE    = SEMENTLexer.tokentypes.LANGLE
RANGLE    = SEMENTLexer.tokentypes.RANGLE
FEATURE   = SEMENTLexer.tokentypes.FEATURE
SYMBOL    = SEMENTLexer.tokentypes.SYMBOL


def _decode(lineiter):
    lexer = SEMENTLexer.lex(lineiter)
    try:
        while lexer.peek():
            yield _decode_sement(lexer)
    except StopIteration:
        pass


def _decode_sement(lexer):
    top = index = lnk = surface = identifier = None
    rels = []
    hcons = []
    icons = []
    eqs = []
    slots = {}
    variables = {}
    lexer.expect_type(LBRACK)
    lnk = _decode_lnk(lexer)
    surface = _decode_dqstring(lexer.accept_type(DQSTRING))
    feature = lexer.accept_type(FEATURE)
    while feature is not None:
        feature = feature.upper()
        if feature in ('LTOP', 'TOP'):
            top = lexer.expect_type(SYMBOL).lower()
        elif feature == 'INDEX':
            index = _decode_variable(lexer, variables)
        elif feature == 'RELS':
            lexer.expect_type(LANGLE)
            while lexer.peek()[0] == LBRACK:
                rels.append(_decode_rel(lexer, variables))
            lexer.expect_type(RANGLE)
        elif feature == 'HCONS':
            lexer.expect_type(LANGLE)
            while lexer.peek()[0] == SYMBOL:
                hcons.append(_decode_cons(lexer, HCons, variables))
            lexer.expect_type(RANGLE)
        elif feature == 'ICONS':
            lexer.expect_type(LANGLE)
            while lexer.peek()[0] == SYMBOL:
                icons.append(_decode_cons(lexer, ICons, variables))
            lexer.expect_type(RANGLE)
        elif feature == "EQS":
            lexer.expect_type(LANGLE)
            while lexer.peek()[0] == SYMBOL:
                eqs.append(_decode_eq(lexer, variables))
            lexer.expect_type(RANGLE)
        elif feature == "SLOTS":
            lexer.expect_type(LANGLE)
            while lexer.peek()[0] == FEATURE:
                slot = _decode_slot(lexer, variables)
                slots[slot[0]] = slot[1]
            lexer.expect_type(RANGLE)
        else:
            raise ValueError('invalid feature: ' + feature)
        feature = lexer.accept_type(FEATURE)
    lexer.expect_type(RBRACK)
    return SEMENT(top, index, rels, slots, eqs, hcons,
               icons=icons, variables=variables,
               lnk=lnk, surface=surface, identifier=identifier)


def _decode_lnk(lexer):
    lnk = lexer.accept_type(LNK)
    if lnk is not None:
        lnk = Lnk(lnk)
    return lnk


def _decode_dqstring(dqstring: Optional[str]) -> Optional[str]:
    if dqstring is not None:
        dqstring = _unescape(dqstring)
    return dqstring


def _decode_variable(lexer, variables):
    var = lexer.expect_type(SYMBOL).lower()
    if var not in variables:
        variables[var] = {}
    props = variables[var]
    if lexer.accept_type(LBRACK):
        lexer.accept_type(SYMBOL)  # variable type
        feature = lexer.accept_type(FEATURE)
        while feature is not None:
            value = lexer.expect_type(SYMBOL)
            props[feature.upper()] = value.lower()
            feature = lexer.accept_type(FEATURE)
        lexer.expect_type(RBRACK)
    return var


def _decode_rel(lexer, variables):
    args = {}
    surface = None
    lexer.expect_type(LBRACK)
    pred = _decode_predicate(lexer)
    lnk = _decode_lnk(lexer)
    surface = _decode_dqstring(lexer.accept_type(DQSTRING))
    _, label = lexer.expect((FEATURE, 'LBL'), (SYMBOL, None))
    # any remaining are arguments or a constant
    role = lexer.accept_type(FEATURE)
    while role is not None:
        role = role.upper()
        if role == 'CARG':
            value = _decode_dqstring(lexer.expect_type(DQSTRING))
        else:
            value = _decode_variable(lexer, variables)
        args[role] = value
        role = lexer.accept_type(FEATURE)
    lexer.expect_type(RBRACK)
    return EP(pred,
              label.lower(),
              args=args,
              lnk=lnk,
              surface=surface,
              base=None)


def _decode_predicate(lexer) -> str:
    predstring = lexer.accept_type(DQSTRING)
    if predstring is not None:
        predstring = _decode_dqstring(predstring)
    else:
        predstring = lexer.choice_type(SQSYMBOL, PREDICATE, SYMBOL)[1]
    return predicate.normalize(predstring)


def _decode_cons(lexer, cls, variables):
    lhs = _decode_variable(lexer, variables)
    relation = lexer.expect_type(SYMBOL).lower()
    rhs = _decode_variable(lexer, variables)
    return cls(lhs, relation, rhs)

def _decode_eq(lexer, variables):
    eq = set()
    # add first variable
    eq.add(_decode_variable(lexer, variables))
    # as long as the next datum is "eq" keep adding to this ongoing eq
    # e.q. x1 eq x2 eq x3, eqs aren't necessarily pairs
    while lexer.peek()[1].lower() == 'eq':
        # lex the 'eq' relation
        lexer.expect_type(SYMBOL)
        # add next variable
        eq.add(_decode_variable(lexer, variables))
    return eq

def _decode_slot(lexer, variables):
    slot = []
    slot.append(lexer.accept_type(FEATURE))
    slot.append(_decode_variable(lexer, variables))
    return slot


##############################################################################
##############################################################################
# Encoding

def _encode(ms, properties, lnk, indent):
    if indent is None or indent is False:
        indent = False  # normalize None to False
        delim = ' '
    else:
        indent = True  # normalize integers to True
        delim = '\n'
    return delim.join(_encode_sement(m, properties, lnk, indent) for m in ms)


def _encode_sement(s, properties, lnk, indent):
    delim = '\n  ' if indent else ' '
    if properties:
        varprops = dict(s.variables)
    else:
        varprops = {}
    parts = [
        _encode_surface_info(s, lnk),
        _encode_hook(s, varprops, indent),
        _encode_rels(s.rels, varprops, lnk, indent),
        _encode_hcons(s.hcons),
        _encode_icons(s.icons, varprops),
        _encode_eqs(s.eqs),
        _encode_slots(s.slots)
    ]
    return '[ {} ]'.format(
        delim.join(
            ' '.join(tokens) for tokens in parts if tokens))


def _encode_surface_info(m, lnk):
    tokens = []
    if lnk:
        if m.lnk:
            tokens.append(str(m.lnk))
        if m.surface is not None:
            tokens.append('"{}"'.format(_escape(m.surface)))
    return tokens


def _encode_hook(m, varprops, indent):
    delim = '\n  ' if indent else ' '
    tokens = []
    if m.top is not None:
        tokens.append('{}: {}'.format(TOP_FEATURE, m.top))
    if m.index is not None:
        tokens.append('INDEX: {}'.format(_encode_variable(m.index, varprops)))
    if tokens:
        tokens = [delim.join(tokens)]
    return tokens


def _encode_variable(var, varprops):
    tokens = [var]
    if varprops.get(var):
        tokens.append('[')
        tokens.append(variable.type(var))
        for prop in sorted(varprops[var], key=property_priority):
            val = varprops[var][prop]
            tokens.append(prop + ':')
            tokens.append(val)
        tokens.append(']')
        del varprops[var]
    return ' '.join(tokens)


def _encode_rels(rels, varprops, lnk, indent):
    delim = ('\n  ' + ' ' * len('RELS: < ')) if indent else ' '
    tokens = []
    for rel in rels:
        pred = _encode_predicate(rel.predicate)
        if lnk:
            pred += str(rel.lnk)
        reltoks = ['[', pred]
        if lnk and rel.surface is not None:
            reltoks.append('"{}"'.format(_escape(rel.surface)))
        reltoks.extend(('LBL:', rel.label))
        for role in sorted(rel.args, key=role_priority):
            arg = rel.args[role]
            if role == CONSTANT_ROLE:
                arg = '"{}"'.format(_escape(arg))
            else:
                arg = _encode_variable(arg, varprops)
            reltoks.extend((role + ':', arg))
        reltoks.append(']')
        tokens.append(' '.join(reltoks))
    if tokens:
        tokens = ['RELS: <'] + [delim.join(tokens)] + ['>']
    return tokens


def _encode_predicate(predicate: str) -> str:
    if re.search(r"[\s\"':<>[\]]", predicate):
        return f'"{_escape(predicate)}"'
    return predicate


def _encode_hcons(hcons):
    tokens = ['{} {} {}'.format(hc.hi, hc.relation, hc.lo)
              for hc in hcons]
    if tokens:
        tokens = ['HCONS: <'] + [' '.join(tokens)] + ['>']
    return tokens


def _encode_icons(icons, varprops):
    tokens = ['{} {} {}'.format(_encode_variable(ic.left, varprops),
                                ic.relation,
                                _encode_variable(ic.right, varprops))
              for ic in icons]
    if tokens:
        tokens = ['ICONS: <'] + [' '.join(tokens)] + ['>']
    return tokens

def _encode_eqs(eqs):
    # e.g. ['x1', 'eq', 'x2', 'x3', 'eq', 'x4', 'eq, 'x5']
    tokens = None
    if eqs:
        tokens = []
        for eq in eqs:
            eq_tokens = ' eq '.join([member for member in eq])
            tokens.append(eq_tokens)
        tokens = ['EQS: <'] + [' '.join(tokens)] + ['>']
    return tokens

def _encode_slots(slots):
    tokens = None
    if slots:
        tokens = ['{}: {}'.format(slot, slots[slot]) for slot in slots]
        tokens = ['SLOTS: <'] + [' '.join(tokens)] + ['>']
    return tokens


# Character Escaping


_ESCAPES = {
    '\\': '\\\\',
    '"': '\\"',
}


_UNESCAPES = {
    '\\\\': '\\',
    '\\"': '"',
}


def _escape(s: str) -> str:
    return "".join(_ESCAPES.get(c, c) for c in s)


def _unescape(s: str) -> str:
    if not s:
        return s
    cs = []
    i = 0
    while i < len(s):
        if s[i] == '\\' and (i + 1) < len(s):
            cs.append(s[i+1])
            i += 2
        else:
            cs.append(s[i])
            i += 1
    return "".join(cs)