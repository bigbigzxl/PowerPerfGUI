a = [1,2,3,4]
b = [10.0, 10.0, 10.0, 10.0]

v = list(map(lambda x: x[0]/x[1], zip(a, b)))
print v