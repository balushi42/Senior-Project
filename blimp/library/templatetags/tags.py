from django import template
from library.models import Category
register = template.Library()

@register.inclusion_tag("tags/categoryoptions.html")
def categoryoptions():
    return {
        "categories": Category.objects.all()
    }
