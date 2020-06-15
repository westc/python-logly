from datetime import datetime
from logly import Log

l = Log(datetime.utcnow().strftime("logs/%Y/%m (%B)/%d (%A)/%Y-%m-%dT%H.%M.%SZ.log"), indent_string="  ")

@l.decorate(log_args=True)
def a(*args, **kwargs):
  l.log(f"Called a: {args}")
  b()
  l.log("Done stuff")


@l.decorate(header="BB")
def b():
  l.log("Called b")
  l.indent()
  l.log("Cool stuff")
  l.indent()
  l.log("Cool stuff 2")
  l.indent()
  l.log("Cool stuff 3")
  raise Exception("4")

l.log(1)
x = []
x.append(x)
a(3,4, dumb=3, x=x)
l.log(2)
