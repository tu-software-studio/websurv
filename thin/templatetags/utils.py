from django import template

register = template.Library()

@register.simple_tag
def link_to(url, text="Link", classes=""):
    return "<a href='{}' class='{}'>{}</a>".format(url, classes, text)

@register.simple_tag
def blink_to(url, text="BSButtonLink", btype="btn-default"):
    return "<a href='{}' class='btn {}'>{}</a>".format(url, btype, text)