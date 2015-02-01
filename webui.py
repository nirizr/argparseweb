import web

try:
  import page
except:
  from . import page

class Webui(object):
  def __init__(self, parser):
   self.set_parser(parser)

  def set_parser(self, parser):
    self._parser = parser

  def get_urls(self):
    return ('/', 'index')

  def get_classes(self):
    class WebuiPageWrapper(page.WebuiPage):
      _parser = self._parser

    return {'index': WebuiPageWrapper}

  def app(self):
    urls = self.get_urls()
    classes = self.get_classes()

    return web.application(urls, classes)

  def dispatch(self):
    self.app().run()

  def wsgi(self):
    return self.app().wsgifunc()
