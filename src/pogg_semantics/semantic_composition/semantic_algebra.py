"""
The semantic_algebra module contains the SemanticAlgebra class which contains methods for semantic composition of SEMENT structures.

[See usage examples here.](project:/usage_nbs/pogg/semantic_composition/SemanticAlgebra_usage.ipynb)
"""

from pathlib import Path
from delphin import mrs
from pogg.my_delphin.my_delphin import SEMENT
from pogg.semantic_composition.sement_util import POGGSEMENTUtil
from pogg.pogg_config import POGGCompositionConfig

from pogg.semantic_composition.call_tracer import SemAlgTracer


class SemanticAlgebra:
    """
    A `SemanticAlgebra` object contains functions for performing basic semantic composition.
    """
    def __init__(self, composition_config: POGGCompositionConfig | Path | str):
        """
        Initialize the `SemanticAlgebra` object.

        Each parameter may also be accessed as an instance attribute.

        **Parameters / Instance Attributes**
        | Parameter | Type | Description |
        | --------- | ---- | ----------- |
        | `composition_config` | `POGGCompositionConfig` | `POGGCompositionConfig` object that contains information about the SEMI and variable labeler |
        """
        if not isinstance(composition_config, POGGCompositionConfig):
            self.composition_config = POGGCompositionConfig(composition_config)
        else:
            self.composition_config = composition_config


    def _get_slots(self, ep):
        """
        Get the slots contributed by a particular EP to send into a SEMENT.

        The information about what slots are contirbuted is obtained from the [SEMI]().

        **Parameters**
        | Parameter | Type | Description |
        | --------- | ---- | ----------- |
        | `ep` | `delphin.mrs.EP` | EP (elementary predicate) object to get slots from |

        **Returns**
        | Type | Description | Example |
        | ---- | ----------- | ------- |
        | `dict` | dict of slots contributed by the EP | `{'ARG1': 'i2', 'ARG2': 'u3', 'ARG3': 'i4'}` |
        """
        slots = {}
        for arg in ep.args:
            # include all semantic arguments except the intrinsic variable (usually ARG0) or CARG
            # EXCEPT for quantifiers, where ARG0 is also a slot
            if (ep.args[arg] != ep.iv and arg != "CARG") or ep.predicate.endswith("_q"):
                slots[arg] = ep.args[arg]
        return slots

    @SemAlgTracer.trace
    def create_base_SEMENT(self, predicate, intrinsic_variable_properties=None, synopsis_dict=None):
        """
        Make the base case SEMENT.

        That is, a SEMENT with only one EP in the `RELS` list before any composition has occurred.

        **Parameters**
        | Parameter | Type | Description | Default | Example |
        | --------- | ---- | ----------- | ------- | ------- |
        | `predicate` | `str` | ERG predicate label, obtained from the [SEMI](project:/education/erg.rst) | | `_cookie_n_1` |
        | `intrinsic_variable_properties` | `dict` | optional dictionary of properties of the intrinsic variable | `{}` | `{'NUM': 'sg'}` |

        **Returns**
        | Type | Description |
        | ---- | ----------- |
        | `SEMENT` | newly created SEMENT with one EP in the `RELS` list |
        """
        if intrinsic_variable_properties is None:
            intrinsic_variable_properties = {}

        # get semantic arguments for given predicate
        args = self.composition_config.concretize(predicate, synopsis_dict)

        # create EP
        # create a handle that will serve as the LBL for the EP
        lbl = self.composition_config.var_labeler.get_var_name('h')
        ep = mrs.EP(predicate, lbl, args)


        # if the predicate ends in "_q" it's a quantifier, so a new handle needs to be created to serve as the LTOP
        # otherwise, use the LBL as LTOP
        if predicate.endswith("_q"):
            ltop = self.composition_config.var_labeler.get_var_name('h')
        else:
            ltop = lbl

        # create SEMENT with one EP on the RELS list
        # top, index, rels, slots, eqs, hcons, icons, variables, lnk, surface, identifier
        # send in empty lists for eqs, hcons, and icons for ease of composition
        return SEMENT(ltop, ep.args['ARG0'], [ep], self._get_slots(ep), [], [], [], {ep.args['ARG0']: intrinsic_variable_properties})

    @SemAlgTracer.trace
    def create_CARG_SEMENT(self, predicate, carg_value, intrinsic_variable_properties={}):
        """
        Make a base case SEMENT for an EP with a CARG argument.

        For example, a SEMENT with the EP `named`, with a `CARG` value of "Liz".

        **Parameters**
        | Parameter | Type | Description | Default | Example |
        | --------- | ---- | ----------- | ------- | ------- |
        | `predicate` | `str` | ERG predicate label, obtained from the [SEMI](project:/education/erg.rst) | | `named` |
        | `carg_value` | `str` | Value for the `CARG` argument | | `"Liz"`
        | `intrinsic_variable_properties` | `dict` | optional dictionary of properties of the intrinsic variable | `{}` | `{'NUM': 'sg'}` |

        **Returns**
        | Type | Description |
        | ---- | ----------- |
        | `SEMENT` | newly created SEMENT with one EP in the `RELS` list |
        """

        # get semantic arguments for given predicate
        args = self.composition_config.concretize(predicate)
        # create EP
        # create a handle that will serve as the LBL for the EP
        lbl = self.composition_config.var_labeler.get_var_name('h')
        ep = mrs.EP(predicate, lbl, args)
        # add CARG as an argument and set the value
        ep.args['CARG'] = carg_value


        # create SEMENT with one EP on the RELS list
        # top, index, rels, slots, eqs, hcons, icons, variables, lnk, surface, identifier
        # send in empty lists for eqs, hcons, and icons for ease of composition
        return SEMENT(lbl, ep.args['ARG0'], [ep], self._get_slots(ep), [], [], [], {ep.args['ARG0']: intrinsic_variable_properties})

    @SemAlgTracer.trace
    def op_non_scopal_argument_hook_slots(self, functor, argument, slot_label):
        """
        Perform non-scopal composition on two SEMENTs. The hook (i.e. the `LTOP` and `INDEX`) of the resulting SEMENT comes from the argument.
        Typically used when the functor is a modifier (e.g. *tasty cookie*).

        **Parameters**
        | Parameter | Type | Description | Example |
        | --------- | ---- | ----------- | ------- |
        | `functor` | `SEMENT` | SEMENT object for the functor  |  |
        | `argument` | `SEMENT` | SEMENT object for the argument  |  |
        | `slot_label` | `str` | label for the semantic argument slot in the functor that the argument is plugging | `ARG1` |

        **Returns**
        | Type | Description |
        | ---- | ----------- |
        | `SEMENT` | newly created SEMENT resulting from composition |
        """

        # FUNC = semantic functor
        # ARG = semantic argument
        # SLOT = hole to be filled on the functor by composition
        # RES = SEMENT resulting from composition

        # RES.TOP = ARG.TOP (note TOP serves as LTOP for SEMENTs)
        # RES.INDEX = ARG.INDEX
        # RES.RELS = FUNC.RELS + ARG.RELS
        # RES.EQS = FUNC.EQS + ARG.EQS + (FUNC.TOP = ARG.TOP) + (FUNC.SLOTS.slot_label = ARG.INDEX)
        # ... (1) identify LTOPs and (2) add EQ between plugged ARG and ARG's INDEX
        # RES.SLOTS = ARG.SLOTS
        # ... take the slots from whichever SEMENT is contributing the HOOK

        # RES.HCONS = FUNC.HCONS + ARG.HCONS
        # RES.ICONS = FUNC.HCONS + ARG.HCONS

        result_top = argument.top
        result_index = argument.index

        result_rels = functor.rels + argument.rels

        result_eqs = functor.eqs + argument.eqs
        # identify (L)TOPs
        result_eqs.append((functor.top, argument.top))
        # add EQ between FUNC.SLOTS.slot_label and ARG.INDEX
        result_eqs.append((functor.slots[slot_label], argument.index))

        result_slots = argument.slots.copy()

        result_hcons = functor.hcons + argument.hcons

        result_icons = functor.icons + argument.icons

        result_variables = {}
        result_variables.update(functor.variables)
        result_variables.update(argument.variables)

        # top, index, rels, slots, eqs, hcons, icons, variables, lnk, surface, identifier
        return SEMENT(result_top, result_index, result_rels, result_slots, result_eqs, result_hcons, result_icons, result_variables)

    @SemAlgTracer.trace
    def op_non_scopal_functor_hook_slots(self, functor, argument, slot_label):
        """
        Perform non-scopal composition on two SEMENTs. The hook of the resulting SEMENT comes from the functor.
        Typically used when the argument is a complement (e.g. *give a cookie*) or preposition (*in the park*).

        **Parameters**
        | Parameter | Type | Description | Example |
        | --------- | ---- | ----------- | ------- |
        | `functor` | `SEMENT` | SEMENT object for the functor  |  |
        | `argument` | `SEMENT` | SEMENT object for the argument  |  |
        | `slot_label` | `str` | label for the semantic argument slot in the functor that the argument is plugging | `ARG1` |

        **Returns**
        | Type | Description |
        | ---- | ----------- |
        | `SEMENT` | newly created SEMENT resulting from composition |
        """

        # FUNC = semantic functor
        # ARG = semantic argument
        # SLOT = hole to be filled on the functor by composition
        # RES = SEMENT resulting from composition

        # RES.TOP = FUNC.TOP (note TOP serves as LTOP for SEMENTs)
        # RES.INDEX = FUNC.INDEX
        # RES.RELS = FUNC.RELS + ARG.RELS
        # RES.EQS = FUNC.EQS + ARG.EQS + (FUNC.TOP = ARG.TOP) + (FUNC.SLOTS.slot_label = ARG.INDEX)
        # ... (1) identify LTOPs and (2) add EQ between plugged ARG and ARG's INDEX
        # RES.SLOTS = FUNC.SLOTS - FUNC.SLOTS.slot_label
        # ... take the slots from whichever SEMENT is contributing the HOOK

        # RES.HCONS = FUNC.HCONS + ARG.HCONS
        # RES.ICONS = FUNC.ICONS + ARG.ICONS

        result_top = functor.top
        result_index = functor.index

        result_rels = functor.rels + argument.rels

        result_eqs = functor.eqs + argument.eqs
        # identify (L)TOPs
        result_eqs.append((functor.top, argument.top))
        # add EQ between FUNC.SLOTS.slot_label and ARG.INDEX
        result_eqs.append((functor.slots[slot_label], argument.index))

        result_slots = functor.slots.copy()
        # delete the slot that's been plugged
        del result_slots[slot_label]

        result_hcons = functor.hcons + argument.hcons

        result_icons = functor.icons + argument.icons

        result_variables = {}
        result_variables.update(functor.variables)
        result_variables.update(argument.variables)

        # top, index, rels, slots, eqs, hcons, icons, variables, lnk, surface, identifier
        return SEMENT(result_top, result_index, result_rels, result_slots, result_eqs, result_hcons, result_icons, result_variables)

    @SemAlgTracer.trace
    def op_scopal_argument_index_slots(self, functor, argument, slot_label):
        """
        Perform scopal composition where the INDEX comes from the argument, but the LTOP comes from the functor.
        Used when the argument is a scopal modifier (e.g. *probably sleeps*).

        **Parameters**
        | Parameter | Type | Description | Example |
        | --------- | ---- | ----------- | ------- |
        | `functor` | `SEMENT` | SEMENT object for the functor  |  |
        | `argument` | `SEMENT` | SEMENT object for the argument  |  |
        | `slot_label` | `str` | label for the semantic argument slot in the functor that the argument is plugging | `ARG1` |

        **Returns**
        | Type | Description |
        | ---- | ----------- |
        | `SEMENT` | newly created SEMENT resulting from composition |
        """

        # FUNC = semantic functor
        # ARG = semantic argument
        # SLOT = hole to be filled on the functor by composition
        # RES = SEMENT resulting from composition

        # RES.TOP = FUNC.TOP (note TOP serves as LTOP for SEMENTs)
        # RES.INDEX = ARG.INDEX
        # RES.RELS = FUNC.RELS + ARG.RELS
        # RES.EQS = FUNC.EQS + ARG.EQS
        # ... no new EQs here just a QEQ in HCONS
        # RES.SLOTS = FUNC.SLOTS - FUNC.SLOTS.slot_label
        # ... take the slots from whichever SEMENT is contributing the HOOK

        # RES.HCONS = FUNC.HCONS + ARG.HCONS + FUNC.slot_label =q ARG.TOP
        # RES.ICONS = FUNC.ICONS + ARG.ICONS

        result_top = functor.top
        result_index = argument.index

        result_rels = functor.rels + argument.rels

        result_eqs = functor.eqs + argument.eqs

        result_slots = argument.slots.copy()

        result_hcons = functor.hcons + argument.hcons
        result_hcons.append(mrs.HCons(functor.slots[slot_label], "qeq", argument.top))

        result_icons = functor.icons + argument.icons

        result_variables = {}
        result_variables.update(functor.variables)
        result_variables.update(argument.variables)

        # it's possible that the hi-handle in the handle constraint here is not type "h" (e.g. for "probably" it would be type "u")
        # so to ensure it is properly constrained later, add an "artificial eq" between the current hi-handle and a newly created "h" variable
        new_h = self.composition_config.var_labeler.get_var_name("h")
        result_variables.update({new_h: {}})
        result_eqs.append((new_h, functor.slots[slot_label]))

        # top, index, rels, slots, eqs, hcons, icons, variables, lnk, surface, identifier
        return SEMENT(result_top, result_index, result_rels, result_slots, result_eqs, result_hcons, result_icons, result_variables)

    @SemAlgTracer.trace
    def op_scopal_functor_index_slots(self, functor, argument, slot_label):
        """
        Perform scopal composition where the INDEX comes from the functor (as does the LTOP, but this is true for all versions of scopal composition).
        Used when the argument is a complement (e.g. *believes it's raining*).

        **Parameters**
        | Parameter | Type | Description | Example |
        | --------- | ---- | ----------- | ------- |
        | `functor` | `SEMENT` | SEMENT object for the functor  |  |
        | `argument` | `SEMENT` | SEMENT object for the argument  |  |
        | `slot_label` | `str` | label for the semantic argument slot in the functor that the argument is plugging | `ARG1` |

        **Returns**
        | Type | Description |
        | ---- | ----------- |
        | `SEMENT` | newly created SEMENT resulting from composition |
        """

        # FUNC = semantic functor
        # ARG = semantic argument
        # SLOT = hole to be filled on the functor by composition
        # RES = SEMENT resulting from composition

        # RES.TOP = FUNC.TOP (note TOP serves as LTOP for SEMENTs)
        # RES.INDEX = FUNC.INDEX
        # RES.RELS = FUNC.RELS + ARG.RELS
        # RES.EQS = FUNC.EQS + ARG.EQS
        # ... no new EQs here just a QEQ in HCONS
        # RES.SLOTS = FUNC.SLOTS - FUNC.SLOTS.slot_label
        # ... take the slots from whichever SEMENT is contributing the HOOK

        # RES.HCONS = FUNC.HCONS + ARG.HCONS + FUNC.slot_label =q ARG.TOP
        # RES.ICONS = FUNC.ICONS + ARG.ICONS

        result_top = functor.top
        result_index = functor.index

        result_rels = functor.rels + argument.rels

        result_eqs = functor.eqs + argument.eqs

        result_slots = functor.slots.copy()
        # delete the slot that's been plugged
        del result_slots[slot_label]

        result_hcons = functor.hcons + argument.hcons
        result_hcons.append(mrs.HCons(functor.slots[slot_label], "qeq", argument.top))

        result_icons = functor.icons + argument.icons

        result_variables = {}
        result_variables.update(functor.variables)
        result_variables.update(argument.variables)

        # it's possible that the hi-handle in the handle constraint here is not type "h" (e.g. for "probably" it would be type "u")
        # so to ensure it is properly constrained later, add an "artificial eq" between the current hi-handle and a newly created "h" variable
        new_h = self.composition_config.var_labeler.get_var_name("h")
        result_variables.update({new_h: {}})
        result_eqs.append((new_h, functor.slots[slot_label]))

        # top, index, rels, slots, eqs, hcons, icons, variables, lnk, surface, identifier
        return SEMENT(result_top, result_index, result_rels, result_slots, result_eqs, result_hcons, result_icons, result_variables)

    @SemAlgTracer.trace
    def op_scopal_functor_index_argument_slots(self, functor, argument, slot_label):
        """
        Perform scopal composition where the INDEX comes from the functor (as does the LTOP, but this is true for all versions of scopal composition)
        but the slots come *from the argument*.
        Used for negation because the INDEX must come from `neg` but the slots of the argument should persist (e.g. *the player who has not eaten a berry*).

        **Parameters**
        | Parameter | Type | Description | Example |
        | --------- | ---- | ----------- | ------- |
        | `functor` | `SEMENT` | SEMENT object for the functor  |  |
        | `argument` | `SEMENT` | SEMENT object for the argument  |  |
        | `slot_label` | `str` | label for the semantic argument slot in the functor that the argument is plugging | `ARG1` |

        **Returns**
        | Type | Description |
        | ---- | ----------- |
        | `SEMENT` | newly created SEMENT resulting from composition |
        """

        # FUNC = semantic functor
        # ARG = semantic argument
        # SLOT = hole to be filled on the functor by composition
        # RES = SEMENT resulting from composition

        # RES.TOP = FUNC.TOP (note TOP serves as LTOP for SEMENTs)
        # RES.INDEX = FUNC.INDEX
        # RES.RELS = FUNC.RELS + ARG.RELS
        # RES.EQS = FUNC.EQS + ARG.EQS
        # ... no new EQs here just a QEQ in HCONS
        # RES.SLOTS = ARG.SLOTS
        # ... take the slots from argument specifically in this case

        # RES.HCONS = FUNC.HCONS + ARG.HCONS + FUNC.slot_label =q ARG.TOP
        # RES.ICONS = FUNC.ICONS + ARG.ICONS

        result_top = functor.top
        result_index = functor.index

        result_rels = functor.rels + argument.rels

        result_eqs = functor.eqs + argument.eqs

        result_slots = argument.slots.copy()

        result_hcons = functor.hcons + argument.hcons
        result_hcons.append(mrs.HCons(functor.slots[slot_label], "qeq", argument.top))

        result_icons = functor.icons + argument.icons

        result_variables = {}
        result_variables.update(functor.variables)
        result_variables.update(argument.variables)

        # it's possible that the hi-handle in the handle constraint here is not type "h" (e.g. for "probably" it would be type "u")
        # so to ensure it is properly constrained later, add an "artificial eq" between the current hi-handle and a newly created "h" variable
        new_h = self.composition_config.var_labeler.get_var_name("h")
        result_variables.update({new_h: {}})
        result_eqs.append((new_h, functor.slots[slot_label]))

        # top, index, rels, slots, eqs, hcons, icons, variables, lnk, surface, identifier
        return SEMENT(result_top, result_index, result_rels, result_slots, result_eqs, result_hcons, result_icons,
                      result_variables)

    @SemAlgTracer.trace
    def op_scopal_quantifier(self, functor, argument):
        """
        Perform scopal composition between a quantifier SEMENT and a quantified SEMENT (e.g. *the cookie*).
        This involves the plugging of two slots (`ARG0` directly, `RSTR` with a qeq) thus warranting a separate function.

        **Parameters**
        | Parameter | Type | Description | Example |
        | --------- | ---- | ----------- | ------- |
        | `functor` | `SEMENT` | SEMENT object for the functor  |  |
        | `argument` | `SEMENT` | SEMENT object for the argument  |  |

        **Returns**
        | Type | Description |
        | ---- | ----------- |
        | `SEMENT` | newly created SEMENT resulting from composition |
        """

        # FUNC = semantic functor
        # ARG = semantic argument
        # SLOT = hole to be filled on the functor by composition
        # RES = SEMENT resulting from composition

        # RES.TOP = FUNC.TOP (note TOP serves as LTOP for SEMENTs)
        # RES.INDEX = FUNC.INDEX
        # RES.RELS = FUNC.RELS + ARG.RELS
        # RES.EQS = FUNC.EQS + ARG.EQS + (FUNC.SLOTS.ARG0 = ARG.INDEX)
        # ... add EQ between ARG0 and INDEX of thing being quantified
        # RES.SLOTS = FUNC.SLOTS - FUNC.SLOTS.slot_label
        # ... take the slots from whichever SEMENT is contributing the HOOK

        # RES.HCONS = FUNC.HCONS + ARG.HCONS + FUNC.RSTR =q ARG.TOP
        # RES.ICONS = FUNC.ICONS + ARG.ICONS

        result_top = functor.top
        result_index = functor.index

        result_rels = functor.rels + argument.rels

        result_eqs = functor.eqs + argument.eqs
        result_eqs.append((functor.slots["ARG0"], argument.index))

        result_slots = functor.slots.copy()
        # delete the slot that's been plugged
        del result_slots["ARG0"]

        result_hcons = functor.hcons + argument.hcons
        result_hcons.append(mrs.HCons(functor.slots["RSTR"], "qeq", argument.top))
        del result_slots["RSTR"]

        result_icons = functor.icons + argument.icons

        result_variables = {}
        result_variables.update(functor.variables)
        result_variables.update(argument.variables)

        # top, index, rels, slots, eqs, hcons, icons, variables, lnk, surface, identifier
        return SEMENT(result_top, result_index, result_rels, result_slots, result_eqs, result_hcons, result_icons, result_variables)

    @SemAlgTracer.trace
    def prepare_for_generation(self, sement):
        """
        Prepare the given SEMENT for generation.

        :::{question} How does a SEMENT get prepared for generation?
        :collapsible:
        To prepare a SEMENT for generation the following steps must occur:

        1. check if the INDEX is of type `e`

            - If not...

                1. check if given SEMENT is quantified, and wrap in generic quantifier if necessary
                2. wrap in `unknown` event

        2. create a new GTOP handle and set it to be QEQ to the SEMENT's previous LTOP
        3. overwrite all EQs to one representative value
        4. constrain all hi-handles in QEQ relationships to be of type `h`
        :::

        **Parameters**
        | Parameter | Type | Description |
        | --------- | ---- | ----------- |
        | `sement` | `SEMENT` | SEMENT to prepare to be sent to the ERG for generation |

        **Returns**
        | Type | Description |
        | ---- | ----------- |
        | `SEMENT` | SEMENT object that has been prepared for generation |
        """

        # duplicate sement to avoid editing the original
        unprepared_sement = POGGSEMENTUtil.duplicate_sement(sement)


        # TODO: i can't get "the cat probably sleeps" bc the top lvl INDEX is i
        # TODO: BUT if i set this check to be only 'x' then it doesn't wrap stand-alone adjs like "black"
        # TODO: a more complex check could be like ,,, if it's i THEN see if the ARG1 of the rel who has that as ARG0 is in a qeq
        # TODO: i guess this depends tho like why the hell is probably's 'i' okay as the top level INDEX is that even real
        if sement.index[0] != "e":
            # check if quantified, wrap in one if not
            if not POGGSEMENTUtil.check_if_quantified(unprepared_sement):
                # if the top level predicate is "named," use "proper_q"
                quant_sement = None
                for rel in unprepared_sement.rels:
                    # if rel.predicate == "named" and rel.args['ARG0'] == unprepared_sement.index:
                    #     quant_sement = self.create_base_SEMENT("def_or_proper_q")
                    if rel.predicate == "card" and rel.args['ARG0'] == unprepared_sement.index:
                        quant_sement = self.create_base_SEMENT("number_q")

                if quant_sement is None:
                    quant_sement = self.create_base_SEMENT("def_udef_a_q")

                quantified_sement = self.op_scopal_quantifier(quant_sement, unprepared_sement)
            else:
                quantified_sement = sement

            # wrap in "unknown" event
            unknown_sement = self.create_base_SEMENT("unknown")
            e_type_sement = self.op_non_scopal_functor_hook_slots(unknown_sement, quantified_sement, "ARG")
        else:
            e_type_sement = unprepared_sement

        # wrap with GTOP
        # check if there's already a GTOP
        has_gtop = False
        for hcon in e_type_sement.hcons:
            if e_type_sement.top == hcon.hi:
                has_gtop = True

        if not has_gtop:
            gtop = self.composition_config.var_labeler.get_var_name("h")
            new_hcon = mrs.HCons(gtop, "qeq", e_type_sement.top)

            # change top and add hcon
            e_type_sement.top = gtop
            e_type_sement.hcons.append(new_hcon)

        # go through all handle constraints, if any variable is not of type h, add another EQ
        # e.g. if the hi argument in an hcon is u1 then add < u1 eq h2 >
        # then when EQs are overwritten the most specific one, h2, is chosen
        for hcon in e_type_sement.hcons:
            if hcon.hi[0] != "h":
                new_h = self.composition_config.var_labeler.get_var_name("h")
                e_type_sement.eqs.append((new_h, hcon.hi))
                e_type_sement.variables[new_h] = {}
            if hcon.lo[0] != "h":
                new_h = self.composition_config.var_labeler.get_var_name("h")
                e_type_sement.eqs.append((new_h, hcon.lo))
                e_type_sement.variables[new_h] = {}

        final_sement = POGGSEMENTUtil.overwrite_eqs(e_type_sement)
        return final_sement

    # @SemAlgTracer.trace
    # def decompose_MRS(self, mrs):
    #     # strip an MRS that came out of the ERG of its "wrapper" material
    #     # return a new SEMENT that can participate in composition
    #
    #     # duplicate because i don't like modifying arguments...
    #     updated_mrs = POGGSEMENTUtil.duplicate_sement(mrs)
    #
    #     # strip the GTOP if present
    #     hcons_to_remove = None
    #     for hcon in updated_mrs.hcons:
    #         if updated_mrs.top == hcon.hi:
    #             # set TOP to the lo handle
    #             updated_mrs.top = hcon.lo
    #             to_remove = hcon
    #             break
    #     updated_mrs.hcons.remove(hcons_to_remove)
    #
    #     # delete "unknown" predicate if present
    #     key_rel = POGGSEMENTUtil.get_key_rel(updated_mrs)
    #
    #     if key_rel.predicate == "unknown":
    #         hcons_to_remove = None
    #         rels_to_remove = None
    #
    #         # mark "unknown" rel for removal
    #         rels_to_remove.append(key_rel)
    #
    #         key_variable = key_rel.args['ARG']
    #         for rel in updated_mrs.rels:
    #             # candidate for key_rel
    #             if rel.args['ARG0'] == key_variable:
    #                 # if it's a quantifier, mark it as to_remove and also remove associated HCon
    #                 pass








