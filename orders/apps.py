from django.apps import AppConfig
from django.template.defaultfilters import register

@register.filter(name='split')
def split(value, key):
    """Splits a string by a given delimiter key argument"""
    if isinstance(value, str):
        return [item.strip() for item in value.split(key)]
    return value
    
class OrdersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'orders'
    verbose_name = 'Orders Management'
