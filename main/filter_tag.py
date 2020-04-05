from django import template

register = template.Library()

@register.filter(name='user_profile')
def user_profile(value):
    if value == "" or value == None:
        return "-"
    else:
        return value

@register.filter(name='user_likes')
def user_likes(value):
    if value == "" or value == None:
        return "0"
    else:
        return value

@register.filter(name='user_birthday')
def user_birthday(value):
    if value == "" or value == None:
        return "No Birthday"
    else:
        return value

@register.filter(name='user_website')
def user_website(value):
    if value == "" or value == None:
        return "No Website"
    else:
        return value