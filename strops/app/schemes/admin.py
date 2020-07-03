"""Admin pages for schemes models

On default generates list view admins for all models
"""
from espressodb.base.admin import register_admins

register_admins("strops.app.schemes")
