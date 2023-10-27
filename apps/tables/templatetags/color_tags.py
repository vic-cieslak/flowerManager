from django.template.defaulttags import register

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

@register.filter
def items(dictionary):
    return dictionary.items()

@register.filter
def dict_values_neq(dictionary, value):
    return {k: v for k, v in dictionary.items() if v != value}

@register.filter
def dict_values_eq(dictionary, value):
    return {k: v for k, v in dictionary.items() if v == value}