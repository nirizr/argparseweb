import web

try:
  import page
except:
  from . import page

class WebuiResultException(Exception)
  def __init__(self, namespace):
    self.namespace = namespace

class Webui(object):
  def __init__(self, parser):
    self._parser = parser

  def get_urls(self):
    return ('/', 'index')

  def get_classes(self, dispatch):
    class WebuiPageWrapper(page.WebuiPage):
      _parser = self._parser
      _dispatch = dispatch

    return {'index': WebuiPageWrapper}

  def app(self, dispatch):
    # Make sure we get an argh-like object here that has a dispatch object
    if dispatch and not hasattr(self._parser, 'dispatch'):
      raise ValueError("Can't dispatch a non dispatchable argument parser")

    urls = self.get_urls()
    classes = self.get_classes(dispatch)

    return web.application(urls, classes)

  def dispatch(self):
    self.app(dispatch=True).run()

  def get(self, count=True):
    # stop condition: if count is a number decrease and loop until 0,
    #   if count is True, loop forever
    while count:
      try:
        self.app(dispatch=False).run()
      except WebuiResultException as ex:
        yield ex.namespace
      
      if type(count) == int:
        count -= 1

  def getone(self):
    self.get(count=1)

  def wsgi(self):
    return self.app(dispatch=True).wsgifunc()
