"""
 Developers : Dmitrij Petters,
 All code is property of original developers.
 Copyright 2011. All Rights Reserved.
"""
 
import re

from django import template
from django.template import FilterExpression
from django.template.loader import get_template

register = template.Library()

def _setup_macros_dict(parser):
    ## Metadata of each macro are stored in a new attribute 
    ## of 'parser' class. That way we can access it later
    ## in the template when processing 'usemacro' tags.
    try:
        ## Only try to access it to eventually trigger an exception
        parser._macros
    except AttributeError:
        parser._macros = {}

class DefineMacroNode(template.Node):
    def __init__(self, name, nodelist, args):
        self.name = name
        self.nodelist = nodelist
        self.args = args

    def render(self, context): #@UnusedVariable
        ## empty string - {% macro %} tag does no output
        return ''

@register.tag(name="macro")
def do_macro(parser, token):
    try:
        args = token.split_contents()
        tag_name, macro_name, args = args[0], args[1], args[2:] #@UnusedVariable
    except IndexError:
        raise template.TemplateSyntaxError, "'%s' tag requires at least one argument (macro name)" % token.contents.split()[0]
    # TODO: check that 'args' are all simple strings ([a-zA-Z0-9_]+)
    r_valid_arg_name = re.compile(r'^[a-zA-Z0-9_]+$')
    for arg in args:
        if not r_valid_arg_name.match(arg):
            raise template.TemplateSyntaxError, "Argument '%s' to macro '%s' contains illegal characters. Only alphanumeric characters and '_' are allowed." % (arg, macro_name)
    nodelist = parser.parse(('endmacro', ))
    parser.delete_first_token()

    ## Metadata of each macro are stored in a new attribute 
    ## of 'parser' class. That way we can access it later
    ## in the template when processing 'usemacro' tags.
    _setup_macros_dict(parser)

    parser._macros[macro_name] = DefineMacroNode(macro_name, nodelist, args)
    return parser._macros[macro_name]

class LoadMacrosNode(template.Node):
    def render(self, context): #@UnusedVariable
        ## empty string - {% loadmacros %} tag does no output
        return ''

@register.tag(name="loadmacros")
def do_loadmacros(parser, token):
    try:
        tag_name, filename = token.split_contents() #@UnusedVariable
    except IndexError:
        raise template.TemplateSyntaxError, "'%s' tag requires at least one argument (macro name)" % token.contents.split()[0]
    if filename[0] in ('"', "'") and filename[-1] == filename[0]:
        filename = filename[1:-1]
    t = get_template(filename)
    macros = t.nodelist.get_nodes_by_type(DefineMacroNode)
    ## Metadata of each macro are stored in a new attribute 
    ## of 'parser' class. That way we can access it later
    ## in the template when processing 'usemacro' tags.
    _setup_macros_dict(parser)
    for macro in macros:
        parser._macros[macro.name] = macro
    return LoadMacrosNode()
    
class UseMacroNode(template.Node):
    def __init__(self, macro, filter_expressions):
        self.nodelist = macro.nodelist
        self.args = macro.args
        self.filter_expressions = filter_expressions
    def render(self, context):
        for (arg, fe) in [(self.args[i], self.filter_expressions[i]) for i in range(len(self.args))]:
            context[arg] = fe.resolve(context)
        return self.nodelist.render(context)

@register.tag(name="usemacro")
def do_usemacro(parser, token):
    try:
        args = token.split_contents()
        tag_name, macro_name, values = args[0], args[1], args[2:] #@UnusedVariable
    except IndexError:
        raise template.TemplateSyntaxError, "'%s' tag requires at least one argument (macro name)" % token.contents.split()[0]
    try:
        macro = parser._macros[macro_name]
    except (AttributeError, KeyError):
        raise template.TemplateSyntaxError, "Macro '%s' is not defined" % macro_name

    if (len(values) != len(macro.args)):
        raise template.TemplateSyntaxError, "Macro '%s' was declared with %d parameters and used with %d parameter" % (
            macro_name,
            len(macro.args),
            len(values))
    filter_expressions = []
    for val in values:
        if (val[0] == "'" or val[0] == '"') and (val[0] != val[-1]):
            raise template.TemplateSyntaxError, "Non-terminated string argument: %s" % val[1:]
        filter_expressions.append(FilterExpression(val, parser))
    return UseMacroNode(macro, filter_expressions)