import os
from django import template

register = template.Library()


@register.filter
def get_fields(obj):
    """
    <ul>
        {% for key, val in object|get_fields %}
            <li>{{ key }}: {{ val }}</li>
        {% endfor %}
    </ul>
    """
    return [(field.name, field.value_to_string(obj)) for field in obj._meta.fields]


@register.filter
def filename(value):
    return os.path.basename(value)


@register.filter
def where_id(users, user_id):
    return filter(lambda u: u.pk == user_id, users)
