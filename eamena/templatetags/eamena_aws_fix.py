from django import template

register = template.Library()

@register.filter()
def eamena_aws_fix(text):
	ret = text.replace('/files/', '/')
	if not('://' in ret):
		ret = 'https://' + ret.lstrip('/')
	return ret

