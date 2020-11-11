def myGen():
  yield 1
  yield 2
  yield 3
  yield 4
  return 4

def myFun():
  return 4


print(myFun())
# for i in myGen():
#   print(i)

print(next(myGen()))
print(next(myGen()))#这是可以停止的函数


my = myGen()
print(next(my))
print(next(my))
print(next(my))
