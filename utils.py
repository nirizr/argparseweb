
# util
class ReloadedIterable:
  """This is an automatically reloaded iterable object.
  Every time it starts an iteration it'll call the specified function
  and generate an updated version of the sequence, yielding one item at a time.

  Its generally useful but specifically created to wrap argparse.Action.choices-like parameters,
  so they'll be updated in new without the argparse object being re-generated."""
  def __init__(self, f, *args, **kwargs):
    self._f = f
    self._args = args
    self._kwargs = kwargs

  def generate(self):
    return self._f(*self._args, **self._kwargs)

  def __iter__(self):
    for item in self.generate():
       yield item

  def __getitem__(self, i):
    return self.generate()[i]
