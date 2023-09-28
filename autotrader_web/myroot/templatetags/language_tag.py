from django import template

register = template.Library()

@register.filter
def language_tag(language_dict, keyword):
    result = keyword
    if keyword in language_dict:
        result = language_dict[keyword]
    return result
