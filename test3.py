import math

#
# This implements the probablity monad
# This defines the semantics of [x for a in b
#                                  for c in d]
# to mean something like "the probability of x supposing a is drawn from
# distribution b and then c is drawn from d, conditioned on a
#
class PDF(dict):
    def __hash__(self):
        return hash(tuple(sorted(self.iteritems())))

def scale(alpha, ps):
  result = PDF()
  for k in ps:
    result[k] = alpha*ps[k]
  return result

def combine(pdf1, pdf2):
  result  = pdf1.copy()
  for k in pdf2.keys():
    if result.has_key(k):
      result[k] += pdf2[k]
    else:
      result[k] = pdf2[k]
  return result

def __concatMap__(f, pps):
  result = PDF()
  for k0 in pps.keys():
    p = pps[k0]
    k = f(k0)
    result = combine(result, scale(pps[k0], f(k0)))
  return result

def __singleton__(x):
  return PDF([(x, 1)])

def __fail__(x):
  return PDF()

def certain(x):
  return __singleton__(x)

def expectation(pdf):
  total = 0.0;
  for k in pdf.keys():
    total += pdf[k]*k
  return total

def probability(condition, pdf):
  return expectation([1 if condition(k) else 0 for k in pdf])

################################################################################
# Test code starts here
################################################################################

def bernoulli(p, a = True, b = False):
  """
  A sample from bernoulli(p, a, b) has probability p of taking the value
  a and probabilty 1-p of taking the value b.
  """
  return PDF([(a, p), (b, 1-p)])

# Straightforward coin toss.
test1 = [x for x in bernoulli(0.5)]

print "test1 =", test1

# A pair of coin tosses.
test2 = [(x, y) for x in bernoulli(0.5)
                for y in bernoulli(0.5)]

print "test2 =", test2

# The sum of the result of three coin tosses.
test3 = [a+b+c for a in bernoulli(0.5, 1, 0)
               for b in bernoulli(0.5, 1, 0)
               for c in bernoulli(0.5, 1, 0)]

print "test3 =", test3

################################################################################
# Chinese restaurant code
# http://en.wikipedia.org/wiki/Chinese_restaurant_process
################################################################################

def addGuest(i, tables):
  if i==len(tables):
    return tables+(1,)
  else:
    tableList = list(tables)
    tableList[i] += 1
    return tuple(tableList)

def selectTable(tables):
  newTables = list(tables)+[1]
  n = sum(newTables)
  return PDF(zip(range(len(newTables)), map(lambda x: float(x)/n, newTables)))

def chineseRestaurantProcess(n):
  """
  Simulates the Chinese restaurant process to n steps
  """

  if n==0:
    return certain(())
  else:
    return [addGuest(guestTable, tables) for tables in chineseRestaurantProcess(n-1)
                                         for guestTable in selectTable(tables)]

# Expected table size (occupancy) given by theory.
def theoreticalTableSize(n):
  total = 0.0
  for k in range(0, n):
    total += 1.0/(k+1)
  return total

# Compare theoretical and simulated expected table size.
# Should be equal to machine precision.
test4a = expectation([len(table) for table in chineseRestaurantProcess(10)])
test4b = theoreticalTableSize(10)
print "test4 =", math.fabs(test4a-test4b) < 1e-9

# Estimate the probability that at least one person is sitting on their own.
# Simulates 16 steps. Note that this is a lot of computation, even though it
# is probably much more accurate than a Monte-Carlo simulation using the same
# amount of CPU time.
for i in range(1, 16):
  test5a = probability(lambda table: min(table)==1, chineseRestaurantProcess(i))
  print i, test5a
test5b = 1-math.exp(-1)
print "test5 =", math.fabs(test5a-test5b) < 1e-9
