from django import template
register = template.Library()

@register.simple_tag
def blink_to(url, text="BSButtonLink", btype="btn-default"):
    return "<a href='{}' class='btn {}'>{}</a>".format(url, btype, text)

