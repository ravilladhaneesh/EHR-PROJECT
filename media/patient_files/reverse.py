n=int(input())


"""
c=1
for i in range(n):
    for j in range(i):
        print(c,end=" ")
        c+=1
    print()
"""



for i in range(n):
    for j in range(2*i):
        print(" ",end="")
    for j in range(2*n-2*i-1):
        print("* ",end="")
    print()
