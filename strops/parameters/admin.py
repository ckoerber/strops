"""Admin pages for parameters models

On default generates list view admins for all models
"""
from espressodb.base.admin import register_admins

register_admins("strops.parameters")
