"""
The `base_constructions` module contains the Mixin class for creating SEMENTs from a number of "basic" constructions of English.

[See usage examples here.](project:/usage_nbs/pogg/semantic_composition/SemanticComposition_usage.ipynb)
"""
import copy

from delphin import mrs
from pogg_semantics.my_delphin import SEMENT, sementcodecs
from pogg_semantics.semantic_composition._sement_util import SEMENTUtil
from pogg_semantics.semantic_composition._call_tracer import SemCompTracer

# TODO: would prefer tracing this separately but i don't wanna deal with changing the eval objs rn and those numbers aren't super interesting anyway
class SurgicalConstructionsMixin:
    """
    The `SurgicalConstructionsMixin` contains functions for composing new SEMENTs using two input SEMENTs.
    """

    def dequantify(self, quantified_SEMENT: SEMENT) -> (SEMENT, SEMENT):
        duplicated_SEMENT = SEMENTUtil.duplicate_sement(quantified_SEMENT)

        if not SEMENTUtil.check_if_quantified(quantified_SEMENT):
            return duplicated_SEMENT
        else:
            key_rel = SEMENTUtil.get_key_rel(duplicated_SEMENT)
            for pred in duplicated_SEMENT.predications:
                if pred.iv == key_rel.iv and (pred.predicate.endswith("_q") or pred.predicate.endswith("_q_i")):
                    key_quant = pred

        duplicated_SEMENT.top = key_rel.label

        duplicated_SEMENT.predications.remove(key_quant)
        hcon_to_remove = None
        for hcon in duplicated_SEMENT.hcons:
            if hcon.hi == key_quant.args["RSTR"]:
                hcon_to_remove = hcon
                break
        if hcon_to_remove is not None:
            duplicated_SEMENT.hcons.remove(hcon_to_remove)

        slot_to_remove = None
        for slot_name, slot_value in duplicated_SEMENT.slots.items():
            if slot_name in key_quant.args:
                if key_quant.args[slot_name] == slot_value:
                    slot_to_remove = slot_name
                    break
        if slot_to_remove is not None:
            duplicated_SEMENT.slots.pop(slot_to_remove)


        new_quant = self.quantifier(key_quant.predicate)

        return new_quant, duplicated_SEMENT

    def extract_predicate_collection(self, given_SEMENT: SEMENT, key_EP: mrs.EP, working_EPs=None,
                                     working_HCons=None) -> SEMENT:
        given_SEMENT = SEMENTUtil.overwrite_eqs(given_SEMENT)
        extracted_index = key_EP.iv
        extracted_eps = []
        extracted_hcons = []
        extracted_variables = {}

        if working_EPs is None:
            working_EPs = copy.deepcopy(given_SEMENT.rels)
        if working_HCons is None:
            working_HCons = []
            for hcon in given_SEMENT.hcons:
                working_HCons.append(mrs.HCons(hcon.hi, "qeq", hcon.lo))

        # get key_quant if applicable
        key_quant = None
        if key_EP.iv.startswith("x"):
            for predication in given_SEMENT.predications:
                if predication.iv == key_EP.iv and (
                        predication.predicate.endswith("_q") or predication.predicate.endswith("_q_i")):
                    key_quant = predication
                    extracted_top = self.semantic_algebra.composition_config.var_labeler.get_var_name("h")
                    break
        else:
            extracted_top = key_EP.label

        # get preds with shared labels; recurse on predicates whose LBL is the hcon.lo to QEQ where hcon.hi is an ARG of an EP with a shared LBL
        # e.g. 'the cat who told the chicken to call' ... tell.ARG3 qeq call.LBL, so we need to extract call and all its associates
        working_copy = copy.copy(working_EPs)
        for pred in working_copy:
            if key_quant and pred.label == key_quant.label:
                extracted_eps.append(pred)
                working_EPs.remove(pred)
                continue
            if pred.label == key_EP.label:
                # # if it's a CARG predication and the CARGs don't match, keep doing
                # if "CARG" in key_EP.args and "CARG" in pred.args:
                #    if key_EP.args["CARG"] != pred.args["CARG"]:
                #        continue

                extracted_eps.append(pred)
                working_EPs.remove(pred)
                # recurse on each arg of the extracted_ep
                # check for new labels to extract
                for var_name, var in pred.args.items():
                    if var_name == "ARG0":
                        continue
                    # if the ARG is h-type, need to identify the nested predicate via a QEQ
                    if var.startswith('h'):
                        for hcon in given_SEMENT.hcons:
                            if hcon.hi == var:
                                # find *some* predication with hcon.lo as LBL and recurse
                                for scoped_pred in working_EPs:
                                    if scoped_pred.label == hcon.lo:
                                        nested_collection = self.extract_predicate_collection(given_SEMENT, scoped_pred,
                                                                                         working_EPs)
                                        extracted_eps.extend(nested_collection.rels)
                    # if it's e or x, can use nested pred directly instead of finding qeq
                    # ... and it's not equal to the key_EP.iv ? like i don't wanna recurse on "tiny.ARG1" ...
                    elif var != key_EP.iv and (var.startswith("e") or var.startswith("x")):
                        for nested_pred in working_EPs:
                            if nested_pred.iv == var and not (
                                    nested_pred.predicate.endswith("_q") or nested_pred.predicate.endswith("_q_i")):
                                nested_collection = self.extract_predicate_collection(given_SEMENT, nested_pred, working_EPs)
                                extracted_eps.extend(nested_collection.rels)
                                break
                    # if i/p/u then it's unfilled so move on
                    else:
                        continue

        for hcon in copy.copy(working_HCons):
            for ep in extracted_eps:
                if hcon.lo == ep.label:
                    extracted_hcons.append(hcon)
                    working_HCons.remove(hcon)
                    break

        for var, var_props in given_SEMENT.variables.items():
            for ep in extracted_eps:
                if var == ep.iv:
                    extracted_variables[var] = var_props

        dummy_SEMENT = SEMENT(extracted_top, extracted_index, extracted_eps, None, None, extracted_hcons,
                              None, extracted_variables, None)
        return dummy_SEMENT

    def extract_semantic_role_of_predicate(self, original_SEMENT: SEMENT, role: str) -> (SEMENT, SEMENT):
        updated_SEMENT = SEMENTUtil.duplicate_sement(original_SEMENT)
        updated_SEMENT = SEMENTUtil.overwrite_eqs(updated_SEMENT)
        extracted_SEMENT = None

        # only go forward if it's a verby SEMENT
        if updated_SEMENT.index.startswith("e"):
            # get matrix_EP
            matrix_EP = None
            for predication in updated_SEMENT.predications:
                if predication.iv == updated_SEMENT.index:
                    matrix_EP = predication
                    break

            # if the matrix_EP is a coordinator, set the matrix_EP one level "deeper"
            if matrix_EP.predicate.endswith("_c"):
                for predication in updated_SEMENT.predications:
                    if predication.iv == matrix_EP.args[role]:
                        if not predication.predicate.endswith("_q") and not predication.predicate.endswith("_q_i"):
                            matrix_EP = predication
                            break

            key_EP = None
            for predication in updated_SEMENT.predications:
                if predication.iv == matrix_EP.args[role]:
                    if not predication.predicate.endswith("_q") and not predication.predicate.endswith("_q_i"):
                        key_EP = predication

                        # add slot to updated_SEMENT
                        updated_SEMENT.slots[role] = key_EP.iv
                        extracted_SEMENT = self.extract_predicate_collection(updated_SEMENT, key_EP)
                        break

        if extracted_SEMENT is not None:
            for extracted_ep in extracted_SEMENT.rels:
                updated_SEMENT.rels.remove(extracted_ep)
            for extracted_hcon in extracted_SEMENT.hcons:
                updated_SEMENT.hcons.remove(extracted_hcon)
            for extracted_var in extracted_SEMENT.variables:
                try:
                    updated_SEMENT.variables.pop(extracted_var)
                except KeyError:
                    # the "TOP" for a quantified extracted NP won't be in the original SEMENT bc it's artificial
                    continue

        return extracted_SEMENT, updated_SEMENT

    def replace_role_of_predicate(self, original_SEMENT: SEMENT, replacement_SEMENT: SEMENT, role: str) -> SEMENT:
        extracted_SEMENT, updated_SEMENT = self.extract_semantic_role_of_predicate(original_SEMENT, role)

        if SEMENTUtil.check_if_quantified(replacement_SEMENT):
            quant_replacement = replacement_SEMENT
        else:
            quant_replacement = self.quantify_generic(replacement_SEMENT)

        return self.semantic_algebra.op_non_scopal_functor_hook_slots(updated_SEMENT, quant_replacement, role)

    def find_isomorphic_arguments(self, first_SEMENT: SEMENT, second_SEMENT: SEMENT):
        first_key = SEMENTUtil.get_key_rel(first_SEMENT)
        second_key = SEMENTUtil.get_key_rel(second_SEMENT)

        first_extractions = {}
        for arg_name in first_key.args:
            if arg_name != "ARG0":
                first_extractions[arg_name] = self.extract_semantic_role_of_predicate(first_SEMENT, arg_name)

        second_extractions = {}
        for arg_name in second_key.args:
            if arg_name != "ARG0":
                second_extractions[arg_name] = self.extract_semantic_role_of_predicate(second_SEMENT, arg_name)

        isomorphic_pairs = []
        for f_arg, f_e in first_extractions.items():
            if f_e[0] is None:
                continue
            for s_arg, s_e in second_extractions.items():
                if s_e[0] is None:
                    continue
                if SEMENTUtil.is_sement_isomorphic(f_e[0], s_e[0]):
                    isomorphic_pairs.append((f_arg, s_arg))

        return isomorphic_pairs

    # @SemCompTracer.trace
    # def compose_propositions_via_relativization(self, matrix_SEMENT: SEMENT, relativized_SEMENT: SEMENT, slot_label: str, distinguished_rel_ARG: str) -> SEMENT:
    #     # collapse to simplify surgery lol
    #     collapsed_matrix = SEMENTUtil.overwrite_eqs(matrix_SEMENT)
    #     collapsed_relative = SEMENTUtil.overwrite_eqs(relativized_SEMENT)
    #     # hacky but whatever
    #     collapsed_matrix.eqs, collapsed_relative.eqs = [], []
    #
    #     key_relativized_rel = SEMENTUtil.get_key_rel(collapsed_relative)
    #     distinguished_var = key_relativized_rel.args[distinguished_rel_ARG]
    #     # get the LBL for the predication whose ARG0 is the distinguished_var
    #     for rel in collapsed_relative.rels:
    #         if rel.iv == distinguished_var and not (rel.predicate.endswith("_q") or rel.predicate.endswith("_q_i")):
    #             disinguished_lbl = rel.label
    #             break
    #
    #     # perform non_scopal composition as normal
    #     matrix_slot_plugged = self.semantic_algebra.op_non_scopal_functor_hook_slots(collapsed_matrix, collapsed_relative, slot_label)
    #     # the new SEMENT now has two EQs that need to be changed:
    #     # 1. matrix_key_rel.plugged_slot = relativized_SEMENT.index ... needs to be matrix_key_rel.plugged_slot = distinguished_var
    #     # e.g. eat.ARG2 = tasty.ARG0 needs to be changed to eat.ARG2 = cake.ARG0
    #     # 2. matrix_key_rel.LBL = relativized_SEMENT.top ... needs to be relativized_SEMENT.top = distinguished_rel_ARG.LBL
    #     # e.g. eat.LBL = tasty.LBL ... needs to be tasty.LBL = cake.LBL
    #     new_eqs = []
    #     for eq in matrix_slot_plugged.eqs:
    #         if collapsed_relative.index in eq:
    #             new_tuple = list(eq)
    #             new_tuple.remove(collapsed_relative.index)
    #             new_tuple.append(distinguished_var)
    #             new_eqs.append(tuple(new_tuple))
    #         elif collapsed_relative.top in eq:
    #             new_tuple = list(eq)
    #             new_tuple.remove(matrix_slot_plugged.top)
    #             new_tuple.append(disinguished_lbl)
    #             new_eqs.append(tuple(new_tuple))
    #         else:
    #             pass
    #
    #
    #     matrix_slot_plugged.eqs = new_eqs
    #     return matrix_slot_plugged


    @SemCompTracer.trace
    def universal_singular(self, original_SEMENT: SEMENT) -> SEMENT:
        updated_SEMENT = SEMENTUtil.duplicate_sement(original_SEMENT)

        for predication in updated_SEMENT.predications:
            pred_ARG0 = predication.args['ARG0']

            if (pred_ARG0.startswith('x') and
                    (predication.predicate != "card" and predication.predicate != "ord")):

                if "NUM" not in updated_SEMENT.variables[pred_ARG0]:
                    updated_SEMENT.variables[pred_ARG0]["NUM"] = "sg"

        return updated_SEMENT

    @SemCompTracer.trace
    def universal_present(self, original_SEMENT: SEMENT) -> SEMENT:
        updated_SEMENT = SEMENTUtil.duplicate_sement(original_SEMENT)

        for predication in updated_SEMENT.predications:
            pred_ARG0 = predication.args['ARG0']

            if pred_ARG0.startswith('e'):
                if "TENSE" in updated_SEMENT.variables[pred_ARG0] and updated_SEMENT.variables[pred_ARG0][
                    "TENSE"] == "tensed":
                    updated_SEMENT.variables[pred_ARG0]["TENSE"] = "pres"

        return updated_SEMENT

    @SemCompTracer.trace
    def specify_quantifiers_to_a(self, original_SEMENT: SEMENT) -> SEMENT:
        updated_SEMENT = SEMENTUtil.duplicate_sement(original_SEMENT)

        for predication in updated_SEMENT.predications:
            if predication.predicate == "def_udef_a_q":
                if (predication.iv in original_SEMENT.variables and
                        "NUM" in original_SEMENT.variables[predication.iv]):
                    if "NUM" in original_SEMENT.variables[predication.iv] == "sg":
                        predication.predicate = "_a_q"
                    else:
                        continue
                predication.predicate = "_a_q"

        return updated_SEMENT

    @SemCompTracer.trace
    def specify_quantifiers_to_the(self, original_SEMENT: SEMENT) -> SEMENT:
        updated_SEMENT = SEMENTUtil.duplicate_sement(original_SEMENT)

        for predication in updated_SEMENT.predications:
            if predication.predicate == "def_udef_a_q":
                predication.predicate = "_the_q"

        return updated_SEMENT


    @SemCompTracer.trace
    def sentence_coordination_merge(self, sent1_SEMENT: SEMENT, sent2_SEMENT: SEMENT, conjunction_SEMENT: SEMENT=None):
        # TODO: this is probably not ideal but i need to get this done so just default to "and" for now
        if conjunction_SEMENT is None:
            conjunction_SEMENT = self.manual_synopsis("_and_c",
                                      synopsis_dict = {
                                          "roles": [
                                              {"name":"ARG0", "value": "e"},
                                              {"name":"ARG1", "value": "u"},
                                              {"name":"ARG2", "value": "u"},
                                          ]
                                    }, intrinsic_variable_properties={"TENSE":"tensed"}
            )

        conj_ARG1 = self.semantic_algebra.op_non_scopal_functor_hook_slots(conjunction_SEMENT, sent1_SEMENT, "ARG1")
        return self.semantic_algebra.op_non_scopal_functor_hook_slots(conj_ARG1, sent2_SEMENT, "ARG2")

    @SemCompTracer.trace
    def sentence_coordination_and_pronoun_replacement_merge(self, sent1_SEMENT: SEMENT, sent2_SEMENT: SEMENT) -> SEMENT:
        isomorphic_args = self.find_isomorphic_arguments(sent1_SEMENT, sent2_SEMENT)

        if len(isomorphic_args) > 0:
            # extract the isomorphic info from sent1 to set var props
            sent1_extract, _ = self.extract_semantic_role_of_predicate(sent1_SEMENT, isomorphic_args[0][0])

            # 3rd person for now idc
            pron_var_props = sent1_extract.variables[sent1_extract.index]
            if "PERS" not in pron_var_props:
                pron_var_props["PERS"] = "3"
            if "PT" not in pron_var_props:
                pron_var_props["PT"] = "std"
            pron = self.pronoun(pron_var_props)

            # just do first, whatever
            sent2_with_pron = self.replace_role_of_predicate(sent2_SEMENT, pron, isomorphic_args[0][1])
            return self.sentence_coordination_merge(sent1_SEMENT, sent2_with_pron)
        else:
            # return None when merges fail
            return None

    @SemCompTracer.trace
    def pronoun_replacement_merge(self, sent1_SEMENT: SEMENT, sent2_SEMENT: SEMENT, pronoun_SEMENT: SEMENT=None) -> (SEMENT, SEMENT):
        isomorphic_args = self.find_isomorphic_arguments(sent1_SEMENT, sent2_SEMENT)

        if len(isomorphic_args) > 0:
            # 3rd person for now idc
            if pronoun_SEMENT is None:
                # extract the isomorphic info from sent1 to set var props
                sent1_extract, _ = self.extract_semantic_role_of_predicate(sent1_SEMENT, isomorphic_args[0][0])

                # 3rd person for now idc
                pron_var_props = sent1_extract.variables[sent1_extract.index]
                if "PERS" not in pron_var_props:
                    pron_var_props["PERS"] = "3"
                if "PT" not in pron_var_props:
                    pron_var_props["PT"] = "std"
                pron = self.pronoun(pron_var_props)
            else:
                pron = pronoun_SEMENT
            # just do first, whatever
            sent2_with_pron = self.replace_role_of_predicate(sent2_SEMENT, pron, isomorphic_args[0][1])
            return sent1_SEMENT, sent2_with_pron
        else:
            # return None when merges fail
            return None

    @SemCompTracer.trace
    def verb_phrase_coordination_merge(self, sent1_SEMENT: SEMENT, sent2_SEMENT: SEMENT) -> SEMENT:
        isomorphic_args = self.find_isomorphic_arguments(sent1_SEMENT, sent2_SEMENT)
        if len(isomorphic_args) > 0:
            # extract and retain first instance of NP and VP to coordinate from first sentence
            representative_np, extracted_1 = self.extract_semantic_role_of_predicate(sent1_SEMENT, isomorphic_args[0][0])
            # extract the VP from the second sentence
            _, extracted_2 = self.extract_semantic_role_of_predicate(sent2_SEMENT, isomorphic_args[0][1])


            conjunction_SEMENT = self.manual_synopsis("_and_c",
                                                      synopsis_dict={
                                                          "roles": [
                                                              {"name": "ARG0", "value": "e"},
                                                              {"name": "ARG1", "value": "u"},
                                                              {"name": "ARG2", "value": "u"},
                                                          ]
                                                      }, intrinsic_variable_properties={"TENSE": "tensed"}
                                                      )

            conj_ARG1 = self.semantic_algebra.op_embed_coordinand(conjunction_SEMENT, extracted_1, "ARG1", isomorphic_args[0][0])

            conj_ARG2 = self.semantic_algebra.op_embed_coordinand(conj_ARG1, extracted_2, "ARG2", isomorphic_args[0][1])
            # plug the role that the representative NP is from from the original sent1 with it
            return self.semantic_algebra.op_non_scopal_functor_hook_slots(conj_ARG2, representative_np, "ARGcoord")

        else:
            # return None when merges fail
            return None

    @SemCompTracer.trace
    def relative_clause_merge(self, sent1_SEMENT: SEMENT, sent2_SEMENT: SEMENT) -> SEMENT:
        isomorphic_args = self.find_isomorphic_arguments(sent1_SEMENT, sent2_SEMENT)
        if len(isomorphic_args) > 0:
            # extract and retain first instance of NP and VP to coordinate from first sentence
            representative_np, extracted_1 = self.extract_semantic_role_of_predicate(sent1_SEMENT,
                                                                                     isomorphic_args[0][0])
            re_quant, deq_np = self.dequantify(representative_np)

            # extract the VP from the second sentence
            _, extracted_2 = self.extract_semantic_role_of_predicate(sent2_SEMENT, isomorphic_args[0][1])

            # modifying representative_np with extracted_2
            rep_np_reled = self.semantic_algebra.op_non_scopal_argument_hook_slots(extracted_2, deq_np, isomorphic_args[0][1])
            quant_rep_np_reled = self.quantify(re_quant, rep_np_reled)

            return self.semantic_algebra.op_non_scopal_functor_hook_slots(extracted_1, quant_rep_np_reled, isomorphic_args[0][0])

        else:
            return None

    @SemCompTracer.trace
    def apposition_merge(self, sent1_SEMENT: SEMENT, sent2_SEMENT: SEMENT) -> SEMENT:
        sent1_keyrel = SEMENTUtil.get_key_rel(sent1_SEMENT)
        sent2_keyrel = SEMENTUtil.get_key_rel(sent2_SEMENT)
        apposify = None
        primary = None
        if sent1_keyrel.predicate == "_be_v_id":
            apposify = sent1_SEMENT
            primary = sent2_SEMENT
        elif sent2_keyrel.predicate == "_be_v_id":
            apposify = sent2_SEMENT
            primary = sent1_SEMENT

        if apposify is None:
            return None


        isomorphic_args = self.find_isomorphic_arguments(primary, apposify)
        if len(isomorphic_args) > 0:
            # extract representative NP and primary predication
            representative_np, extracted_primary = self.extract_semantic_role_of_predicate(primary, isomorphic_args[0][0])

            # extract duplicate NP
            _, copula_plus_appos = self.extract_semantic_role_of_predicate(apposify, isomorphic_args[0][1])
            if isomorphic_args[0][1] == "ARG1":
                other_arg = "ARG2"
            else:
                other_arg = "ARG1"
            extracted_appos, _ = self.extract_semantic_role_of_predicate(copula_plus_appos, other_arg)

            apposed = self.appositive(representative_np, extracted_appos)
            return self.semantic_algebra.op_non_scopal_functor_hook_slots(extracted_primary, apposed, isomorphic_args[0][0])




