from django import template

register = template.Library()

@register.filter(name='joinAll')
def concat(arg1):

    if isinstance(arg1, list):
        result = ''.join(arg1)
        prova = result.replace('(',' (')
        prova = prova.replace('Republic', ' Republic')
        prova = prova.replace('Islamic', ', Islamic')
        print(prova)
        return prova
    else:
        return str(arg1)
