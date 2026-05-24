# from pogg.my_delphin.my_delphin import SEMENT
# import re
# from pogg.semantic_composition.sement_util import POGGSEMENTUtil
#
# class PerplexityConstructionsMixin:
#     """
#     The `BaseConstructionsMixin` contains functions for composing new SEMENTs using two input SEMENTs.
#     """
#     def boolean_value(self, value: bool) -> SEMENT:
#         # turning it into a SEMENT for consistency of what semantic composition functions return
#         if value:
#             return self.adjective("_true_a_of")
#         else:
#             return self.adjective("_false_a_of")
#
#     def boolean_property(self, boolean_node_SEMENT: SEMENT, modified_SEMENT: SEMENT, true_SEMENT: SEMENT, false_SEMENT: SEMENT) -> SEMENT:
#         key_rel = None
#         for rel in boolean_node_SEMENT.rels:
#             if boolean_node_SEMENT.index == rel.id and not rel.predicate.endswith("_q"):
#                 key_rel = rel
#                 break
#
#         if key_rel:
#             if key_rel.predicate == "_true_a_of":
#                 return self.generic_descriptor(true_SEMENT, modified_SEMENT)
#             else:
#                 return self.generic_descriptor(false_SEMENT, modified_SEMENT)
#         else:
#             return None
#
#     def boolean_ARG1_relative_clause(self, boolean_node_SEMENT: SEMENT, ARG1_SEMENT: SEMENT, ARG2_SEMENT: SEMENT,
#                                      true_SEMENT: SEMENT, false_SEMENT: SEMENT) -> SEMENT:
#         key_rel = None
#         for rel in boolean_node_SEMENT.rels:
#             if boolean_node_SEMENT.index == rel.id and not rel.predicate.endswith("_q"):
#                 key_rel = rel
#                 break
#
#         if key_rel:
#             if key_rel.predicate == "_true_a_of":
#                 return self.ARG1_relative_clause(true_SEMENT, ARG1_SEMENT, ARG2_SEMENT)
#             else:
#                 return self.ARG1_relative_clause(false_SEMENT, ARG1_SEMENT, ARG2_SEMENT)
#         else:
#             return None
#
#     def boolean_ARG2_relative_clause(self, boolean_node_SEMENT: SEMENT, true_SEMENT: SEMENT, false_SEMENT: SEMENT,
#                                      ARG2_SEMENT: SEMENT, ARG1_SEMENT: SEMENT=None) -> SEMENT:
#         key_rel = None
#         for rel in boolean_node_SEMENT.rels:
#             if boolean_node_SEMENT.index == rel.id and not rel.predicate.endswith("_q"):
#                 key_rel = rel
#                 break
#
#         if key_rel:
#             if key_rel.predicate == "_true_a_of":
#                 return self.ARG2_relative_clause(true_SEMENT, ARG2_SEMENT)
#             else:
#                 return self.ARG2_relative_clause(false_SEMENT, ARG2_SEMENT)
#         else:
#             return None
#
#     # def boolean_edge(self, boolean_SEMENT: SEMENT, static_SEMENT: SEMENT,
#     #                  true_SEMENT: SEMENT, false_SEMENT: SEMENT, comp_btw_bool_and_static: SEMENT) -> SEMENT:
#     #
#     #     # get the composition function based on the name
#     #     pass
#
#
#
#     # def boolean_subj_rel_clause(self, boolean_node_SEMENT: SEMENT, modified_SEMENT: SEMENT, true_SEMENT: SEMENT, false_SEMENT: SEMENT) -> SEMENT:
#     #     key_rel = None
#     #     for rel in boolean_node_SEMENT.rels:
#     #         if boolean_node_SEMENT.index == rel.id and not rel.predicate.endswith("_q"):
#     #             key_rel = rel
#     #             break
#     #
#     #     if key_rel:
#     #         if key_rel.predicate == "_true_a_of":
#     #             return self.subject_relative_clause(true_SEMENT, modified_SEMENT)
#     #         else:
#     #             return self.subject_relative_clause(false_SEMENT, modified_SEMENT)
#     #     else:
#     #         return None
#     #
#     #
#     # def edge_introduced_obj_rel_clause(self, subject_SEMENT: SEMENT, object_SEMENT: SEMENT, edge_SEMENT: SEMENT) -> SEMENT:
#     #     relative_clause_SEMENT = self.subject_of_verb(edge_SEMENT, subject_SEMENT)
#     #     return self.object_relative_clause(relative_clause_SEMENT, object_SEMENT)
#
#
#
#     def un_prefix(self, negated_SEMENT: SEMENT) -> SEMENT:
#         un_SEMENT = self.basic("_un-_a_neg")
#         return self.semantic_algebra.op_non_scopal_argument_hook(un_SEMENT, negated_SEMENT, "ARG1")
#
#     def generic_descriptor(self, descriptor_SEMENT: SEMENT, described_SEMENT: SEMENT) -> SEMENT:
#         # edges labeled "descriptor" may have an adjective or a participle as their child
#         # so the function has to determine which type of descriptor it has and do composition based on that
#
#         # if it's an adjective...
#         # TODO: is the only way to tell this whether the predicate has _a_ in the name?
#
#         # MAKE A SEMENTUTIL FUNCITON THAT DOES THIS...?
#         for rel in descriptor_SEMENT.rels:
#             if descriptor_SEMENT.index == rel.id and not rel.predicate.endswith("_q"):
#                 key_rel = rel
#                 break
#
#         if re.match(r"_[a-z]+_v_", key_rel.predicate):
#             # is there an ARG2?
#             if 'ARG2' in key_rel.args:
#                 return self.passive_participle_modifier(descriptor_SEMENT, described_SEMENT)
#             else:
#                 result = self.present_participle_modifier(descriptor_SEMENT, described_SEMENT)
#                 return result
#         # if it's a noun, treat it like a compound
#         elif re.match(r"_[a-z]+_n_", key_rel.predicate):
#             return self.compound_noun(described_SEMENT, descriptor_SEMENT)
#         # just assuming it's an adjective otherwise
#         else:
#             # assume BaseConstructionsMixin... this might be a bad idea but oh well...
#             return self.prenominal_adjective(descriptor_SEMENT, described_SEMENT)