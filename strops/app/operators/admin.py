"""Admin pages for operators models

On default generates list view admins for all models
"""

from espressodb.base.admin import register_admins
from espressodb.base.admin import ListViewAdmin as LVA


class ListViewAdmin(LVA):
    @staticmethod
    def instance_name(obj) -> str:
        """Returns the name of the instance
        Arguments:
            obj: The model instance to render.
        """
        return obj.latex if hasattr(obj, "latex") else str(obj)


register_admins(
    "strops.app.operators", exclude_models=["Operator"], admin_class=ListViewAdmin
)
