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

@register.filter(name='cut_multiple')
def cut_multiple(value, arg):
    """Removes all values of arg from the given string."""
    for character in arg:
        value = value.replace(character, '')
    return value