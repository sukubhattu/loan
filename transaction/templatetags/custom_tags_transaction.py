from django import template

register = template.Library()


@register.filter(name='get_loan_status')
def get_loan_status(status):
    return 'hello'
