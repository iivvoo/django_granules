from django import template

from ..registry import granules_registry


"""
    Granules allow child templates and (static) python code to inject granules
    into (base) templates. This allows you to define generic granules sections
    which can later be filled by either pythoncode (globally) or child templates
    (context specific)

    This is somewhat similar to django zekizai but it doesn't require the
    sections to be defined at the toplevel base template (but it does require
    a "{% block granules %}")

    This is all somewhat experimental but seems to work :)
"""

register = template.Library()


@register.tag(name="granule")
def granule(parser, token):
    try:
        tag_name, granulename = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError("%r tag requires a single argument"
                                           % token.contents.split()[0])
    nodelist = parser.parse(("endgranule",))
    parser.delete_first_token()

    return GranuleBlockNode(granulename.strip("'\""), nodelist)


class GranuleBlockNode(template.Node):
    def __init__(self, granulename, nodelist):
        self.granulename = granulename
        self.nodelist = nodelist

    def render(self, context):
        output = self.nodelist.render(context)
        try:
            context.render_context[self.granulename].append(output)
        except KeyError:
            context.render_context[self.granulename] = [output]

        return ''


@register.tag(name="granules")
def granules(parser, token):
    try:
        tag_name, granulename = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError("%r tag requires a single argument" % token.contents.split()[0])
    return GranuleNode(granulename.strip("'\""))


class GranuleNode(template.Node):
    def __init__(self, granulename):
        self.granulename = granulename

    def render(self, context):
        frags = granules_registry.get(self.granulename, [])
        res = ""
        for f in sorted(frags):
            res += f[1]

        for nl in context.render_context.get(self.granulename, []):
            res += nl
        return res

