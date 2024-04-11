from django import template

register = template.Library()
@register.simple_tag
def member_paid(practice, user):
    return practice.paid(user)