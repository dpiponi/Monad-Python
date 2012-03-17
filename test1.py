a = [x for y in [1,2,3]
       if y>2
       for x in [y,10*y]
       if x>15]

print a

def concatMap(k, m):
  return lambda c:m(lambda a:k(a)(c))

def singleton(x):
  return lambda f:f(x)

def callCC(f):
  return lambda c:f(lambda a:lambda _:c(a))(c)

def fail():
  raise "Oh shit!"

a = callCC(lambda k: [(u,y) for x in singleton(11)
                            for u in (k(1000) if x>10 else singleton(x))
                            for y in singleton(2)])

print a(str)

a = callCC(lambda k: [x for x in singleton(11)
                        if x > 10])

print a(str)
