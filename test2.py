import math

def __concatMap__(k, m):
  return lambda c:m(lambda a:k(a)(c))

def __singleton__(x):
  return lambda f:f(x)

def callCC(f):
  return lambda c:f(lambda a:lambda _:c(a))(c)

def __fail__():
  raise "Failure is not an option for continuations"

def ret(x):
  return __singleton__(x)

def id(x):
  return x

def solve(a, b, c):
  return callCC(lambda throw: [((-b-d)/(2*a), (-b+d)/(2*a))
                               for a0 in (ret(a) if a!=0 else throw("Not quadratic"))
                               for d2 in ret(b*b-4*a*c)
                               for d in (ret(math.sqrt(d2)) if d2>=0 else throw("No roots"))
                              ])

print solve(1, 0, -9)(id)
print solve(1, 1, 9)(id)
print solve(0, 1, 9)(id)