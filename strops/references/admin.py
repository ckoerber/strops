"""Admin pages for references models

On default generates list view admins for all models
"""
from espressodb.base.admin import register_admins

register_admins("strops.references")
