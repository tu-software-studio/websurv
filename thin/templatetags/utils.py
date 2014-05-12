from django import template
from websurv import settings

register = template.Library()

@register.simple_tag
def link_to(url, text="Link", classes=""):
    return "<a href='{}' class='{}'>{}</a>".format(url, classes, text)

@register.simple_tag
def blink_to(url, text="BSButtonLink", btype="btn-default"):
    return "<a href='{}' class='btn {}'>{}</a>".format(url, btype, text)

@register.simple_tag
def get_app_version():
    return settings.APP_VERSION