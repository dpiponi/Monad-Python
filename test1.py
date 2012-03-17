# Some simple regression tests

a = [(x, y, z) for x in [0, 1, 2]
               for y in [0, 1, 2]
               for z in [0, 1, 2]]

print len(a)

b = [(x, y) for x in [0,1]
            for y in [0,1]
            if x+y < 2]

print b

c = [(x, y, z) for x in range(1, 10)
               for y in range(1, 10)
               if x < y
               for z in range(1, 10)
               if x*x+y*y == z*z]

print c