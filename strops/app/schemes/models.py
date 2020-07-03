# """Models of schemes
# """
#
# # Note: if you want your models to use espressodb features, they must inherit from Base
#
# from django.db import models
# from espressodb.base.models import Base
#
#
# class ExpansionScheme(Base):
#     """An expansion scheme which relates operators at different scales.
#
#     It must provides keys which allow ordering different opator relations.
#     """
#
#     name = models.CharField(max_length=256, help_text="Name of the expansion scheme.")
#     source_scale = models.CharField(
#         max_length=256, choices=SCALES, help_text="The source scale of the expansion."
#     )
#     target_scale = models.CharField(
#         max_length=256, choices=SCALES, help_text="The target scale of the expansion."
#     )
#     parameters = models.JSONField(
#         help_text="List of expansion parameters which must be present for"
#         " each term (OperatorRelation) in the expansion."
#     )
#     references = models.ManyToManyField(
#         Publication, help_text="Publications specifying the operator relationship."
#     )
#
#     def check_consistency(self):
#         """Checks if parameters key is a list of sympy expressions."""
#         assert isinstance(self.parameters, list)
#         for par in self.parameters:
#             sympify(par)
#
#
# class BilinearOperatorRelation(Base):
#     """Table storing information between different oprator representation bridging scales.
#
#     For example, this quark operator maps to the following nucleon operators.
#     """
#
#     source = models.ForeignKey(
#         BilinearOperator,
#         on_delete=models.CASCADE,
#         related_name="source_for",
#         help_text="More fundamental operator as a source for the propagation of scales.",
#     )
#     target = models.ForeignKey(
#         BilinearOperator,
#         on_delete=models.CASCADE,
#         related_name="target_of",
#         help_text="Operator as a source for the propagation of scales.",
#     )
#     factor = SympyField(
#         encoder="expression",
#         help_text="Factor associated with the propagation of scales."
#         " E.g., 'source -> factor * target' at 'order'.",
#     )
#     order = models.JSONField(
#         null=True,
#         blank=True,
#         help_text="Additional information allowing to order different operators"
#         " by their relevance."
#         " E.g., chiral power counting scheme.",
#     )
#     references = models.ManyToManyField(
#         Publication, help_text="Publications specifying the operator relationship."
#     )
#     scheme = models.ForeignKey(
#         ExpansionScheme,
#         on_delete=models.CASCADE,
#         help_text="Key for grouping different schemes to form a complete representation"
#         " (e.g., if an expansion scheme is workout over several publications)."
#         " Relationships with the same tag should share the same 'order' keys"
#         " to allow sorting them by relevance. ",
#     )
#     parameters = models.ManyToManyField(
#         Parameter, help_text="Parameter present in the expression."
#     )
#
#     def check_consistency(self):
#         """Runs consistency checks on operator relation.
#
#         Checks:
#             * factor can be converted to sympy expression
#             * target scale equals scheme target scale
#             * source scale equals scheme source scale
#             * all expansion parameters defined by scheme are present
#         """
#         sympify(self.factor)
#
#         if self.target.scale != self.scheme.target_scale:
#             raise ValueError
#         if self.source.scale != self.scheme.source_scale:
#             raise ValueError
#
#         if not set(self.order.keys()) != set(self.scheme.parameters):
#             raise ValueError
