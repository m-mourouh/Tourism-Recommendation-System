from django import template

register = template.Library()

@register.simple_tag

def rangeNum(n):
    return range(n)

def calculate(n):
    return 5 - n;

def imgURL(url):
    return 'img/hotels/' + str(url)

register.filter('imgURL', imgURL)
register.filter('calculate', calculate)
register.filter('rangeNum', rangeNum)