# builtin
import os
import sys
import cStringIO as StringIO
import argparse
import collections

# 3rd party
import web
import argh

class WebuiPage(object):
  _parser = None
  _dispatch = None
  _parsed = True
  _form_template = web.template.frender(os.path.join(os.path.dirname(__file__), "templates/input.html"), globals={'type': type, 'basestring': basestring})

  def __init__(self):
    self._actions = collections.OrderedDict()

    form_inputs = self.get_form_inputs()
    self._form = web.form.Form(*form_inputs)

  def GET(self):
    form = self._form()
    yield self._form_template(form)

  def multiple_args(self, nargs):
    if nargs == '?':
      return False
    if nargs == '*' or nargs == '+':
      return True
    if type(nargs) == int and nargs > 1:
      return True
    return False

  def parsable_add_value(self, argv, action, value):
    if action.nargs == 0:
      pass
    elif self.multiple_args(action.nargs):
      argv.extend(value)
    else:
      argv.append(value)

  def get_input(self, form):
    for action_id, action in self._actions.items():
      if not action_id in form.value:
        continue

      value = form.d[action_id]
      yield action_id, action, value

  def POST(self):
    form = self._form()

    if not form.validates():
      return self._form_template(form)

    # make sure form is filled according to input
    defs = {}
    for action_id, action, _ in self.get_input(form):
      if self.multiple_args(action.nargs):
        defs[action_id] = []
    i = web.input(**defs)
    form.fill(i)

    # get parameters without prefix
    pos_argv = []
    opt_argv = []

    for _, action, value in self.get_input(form):
      if self.get_disposition(action) == 'optional':
        action_name = self.get_name(action)
        arg_name = "--" + action_name
        opt_argv.append(arg_name)
        self.parsable_add_value(opt_argv, action, value)
      elif self.get_disposition(action) == 'positional':
        self.parsable_add_value(pos_argv, action, value)

    arg = pos_argv + opt_argv
    print(arg)

    stdout = StringIO.StringIO()
    stderr = StringIO.StringIO()
    old_stderr = None
    old_stdout = None
    try:
      sys.stderr, old_stderr = stderr, sys.stderr
      sys.stdout, old_stdout = stdout, sys.stdout
      if self._parsed:
        arg = self._parser.parse_args(args=arg)
      result = self._dispatch(arg)
    finally:
      if old_stderr:
        sys.stderr = old_stderr
      if old_stdout:
        sys.stdout = old_stdout
    print(stderr.getvalue())

    return "Running: {}\nErrors: {}\nResult: {}\nOutput:\n{}".format(arg, stderr.getvalue(), result, stdout.getvalue())

#class WebuiParser(argh.ArghParser):
#  def __init__(self, *args, **kwargs):
#    super(WebuiParser, self).__init__(*args, **kwargs)
#    self.webui = Webui(self)

  def get_base_id(self, action):
    base_id = action.dest
    for opt_name in action.option_strings:
      if len(base_id) < len(opt_name):
        base_id = opt_name
    if base_id == argparse.SUPPRESS:
      base_id = "command"
    return base_id.lstrip('-')

  def get_class(self, prefix):
    return "_".join(prefix) if prefix else ""

  def get_id(self, action, prefix):
    return self.get_class(prefix+[self.get_base_id(action)])

  def get_name(self, action):
    return self.get_base_id(action)

  def get_description(self, action):
    base_id = self.get_base_id(action)
    base_id = base_id.replace('_', ' ').replace('-', ' ')
    return base_id[0].upper() + base_id[1:]

  def get_nargs(self, action):
    if action.nargs is None:
      return 1
    if type(action.nargs) == int:
      return action.nargs
    if action.nargs == '?' or action.nargs == '+' or action.nargs == '*':
      return action.nargs
    if hasattr(action.nargs, 'isdigit') and action.nargs.isdigit():
      return int(action.nargs)
    return 1

  def get_help(self, action):
    if not action.help:
      return ""
    return action.help % action.__dict__

  def get_disposition(self, action):
    if len(action.option_strings):
      return "optional"
    else:
      return "positional"

  def get_subparser(self, action):
    return isinstance(action, argparse._SubParsersAction)

  def filter_input_object(self, action):
    if isinstance(action, argparse._VersionAction):
      return True
    if isinstance(action, argparse._HelpAction):
      return True
    return False

  # TODO: maybe this function should move to be near the opposite in webuipage.POST
  def get_input_object(self, action, prefix):
    input_parameters = {}
    input_parameters['class'] = self.get_class(prefix)
    input_parameters['name'] = self.get_id(action, prefix)
    input_parameters['id'] = self.get_id(action, prefix)

    input_type = web.form.Textbox

    if action.choices:
      input_type = web.form.Dropdown
      input_parameters['args'] = [choice for choice in action.choices]
      if action.nargs:
        if action.nargs == '*' or action.nargs == '+' or (action.nargs.isdigit() and int(action.nargs) > 1):
          input_parameters['multiple'] = 'multiple'
          input_parameters['size'] = 4
    elif isinstance(action, (argparse._StoreTrueAction, argparse._StoreFalseAction, argparse._StoreConstAction)):
      input_type = web.form.Checkbox
      input_parameters['checked'] = True if action.default else False
      input_parameters['value'] = action.const
    else:
      input_parameters['value'] = action.default if action.default else ""

    if isinstance(action, argparse._SubParsersAction):
      input_parameters['onChange'] = "javascript: update_show(this);"
      input_parameters['value'] = action.choices.keys()[0]

    if len(action.option_strings):
      input_parameters['default'] = action.default
      # if optional argument may be present with either 1 or no parameters, the default shifts
      # to being the no parameter's value. this is mearly to properly display actual values to the user
      if action.nargs == '?':
        ipnut_parameters['value'] = action.const
      
    # TODO: support these actions: append, append_const, count
    self._actions[self.get_id(action, prefix)] = action
    input_object = input_type(**input_parameters)

    input_object.description = self.get_description(action)
    input_object.nargs = self.get_nargs(action)
    input_object.help = self.get_help(action)
    input_object.disposition = self.get_disposition(action)
    input_object.subparser = self.get_subparser(action)

    return input_object

  def get_form_inputs(self, parser=None, prefix=[]):
    inputs = []

    if parser is None:
      parser = self._parser

    group_actions = [group_actions
                     for group_actions in parser._mutually_exclusive_groups]
    subparser_actions = parser._subparsers
    actions = [action
               for action in parser._actions
               if action not in group_actions]

    for action in actions:
      if not self.filter_input_object(action):
        inputs.append(self.get_input_object(action, prefix))

      if isinstance(action, argparse._SubParsersAction):
        for choice_name, choice_parser in action.choices.items():
          inputs.extend(self.get_form_inputs(choice_parser, prefix + [choice_name]))

    return inputs
