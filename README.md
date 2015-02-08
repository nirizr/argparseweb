# README #

This web.py based simple module allows you to automatically set up a simple HTTP web server out of advanced `argparse.ArgumentParser` objects and similar (`argh.ArgumentParser`) ones.
Using this on top of argh lets you automatically generate web user interface out of simple functions defined in your application.
This package was made for getting your personal command line scripts to the next stage - internal shared utilities.

### How do I get set up? ###

For a production like setup you'll need:

1. make your main script expose an application global object by calling webui.Webui.wsgi() method

2. modify `index.wsgi` to fit your application (trivial configuration, import aforementioned application)

3. set up a wsgi supporting apache (or any other) server 

For debugging like setup you'll need (but since it's used for internal tools, this might also be fine):

1. run the original command line tool

2. instead of methods like `argparse.ArgumentParser.parse_args()` or `argh.dispatch()`, you'll simply need to call `webui.WebUI.dispatch()` which will create a web.py development application.

### example working snippet ###

This snippet includes three modes of operations:

1. first and simplest: dispatch methods using argh's automatic function to command line parser facilities, this is completely unrelated to webui and that way you won't lose existing command line usage ability.

2. getting `--webui` as the first command line argument, sets up a development web server (defaults to *:8080) and provides the 

```
#!python
def get_parser():
  """Generate generic argument parser"""
  cmd_parser = argh.ArghParser()
  cmd_parser.add_commands([...])

  return cmd_parser

def main():
  # k. get the parser as usual
  cmd_parser = get_parser()

  # last chance to use webui, if --webui is passed as first command line argument
  # remove it as let webui handle the rest
  if sys.argv[1] == '--webui':
    sys.argv.remove('--webui')
    cmd_parser = webui.Webui(cmd_parser) # second mode of operation - development/fast setup

  # dispatch either webui or argh
  cmd_parser.dispatch() # first mode of operation - regular command line

def wsgi():
  global application

  # create a webui application using the command line argument parser object
  # and make it's wsgi function the global `application` parameter as required by wsgi
  cmd_parser = get_parser()
  application = webui.Webui(cmd_parser).wsgi() # third mode of operation - production wsgi application

if __name__ == "__main__":
  # script initialized as main, lets do our trick
  main()
else:
  # if script wasn't initialized as main script, we're probably running
  # in wsgi mode
  wsgi()
```


### known issues ###

* right now vary-length arguments (nargs='?', nargs='*', nargs='+') are limited to  one argument because i didn't write the HTML required for that. i'm considering multiple text inputs or textarea with line separation, input (and code) are most welcome.
* some code reordering is needed (split template to another file - it's grown quite big, handle action parameters better - shouldn't pass everything as html attributes although it's comfortable)
* smoother integration into existing code.


### Who do I talk to? ###

* Repo owner or admin