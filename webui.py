import web

import page

import multiprocessing

class Webui(object):
  def __init__(self, parser):
    self._parser = parser

  def get_urls(self):
    return ('/', 'index')

  def app(self, dispatch, parsed):
    class WebuiPageWrapper(page.WebuiPage):
      _parser = self._parser
      _dispatch = dispatch
      _parsed = parsed

    urls = ('/', 'index')
    classes = {'index': WebuiPageWrapper}

    return web.application(urls, classes)

  def dispatch(self, dispatch=None, parsed=False):
    # Make sure we get an argh-like object here that has a dispatch object
    if not dispatch and hasattr(self._parser, 'dispatch'):
      dispatch = self._parser.dispatch

    if not dispatch:
      raise ValueError("Can't dispatch a non dispatchable parser without a dispatch method")

    self.app(dispatch=dispatch, parsed=parsed).run()

  def wsgi(self, dispatch=None, parsed=True):
    return self.app(dispatch, parsed).wsgifunc()

  def get(self, count=True):
    # prepare a process-safe queue to hold all results
    results = multiprocessing.Queue()

    # spawn web.py server in another process, have it's dispatch as queue.put method
    app = self.app(dispatch=results.put, parsed=True)
    t = multiprocessing.Process(target=app.run)
    t.start()

    # stop condition: if count is a number decrease and loop until 0,
    #   if count is True, loop forever
    while count:
      yield results.get()
      
      if type(count) == int:
        count -= 1

    app.stop()
    t.terminate()

  def getone(self):
    return list(self.get(count=1))[0]
