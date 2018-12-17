'''
@author: Mohammad Naji Kadri

A program that generate powersets
'''

#returns a string representation of a numbers list
def stringify(lst):
    return ''.join([str(x) for x in lst])

'''PowerSet Algorithm:
the parameter n is the number of elements in the list/set
The algorithm is pretty straightforward and the technique
used is as if someone was doing it manually.
The is idea inspired from the membership table of the set theory
in discrete mathematics.
1 denotes membership and 0 the opposite.
We start with a list with no members (all 0's)
we look from right to left of the list.
if the element is not found (0) we replace it with 1
if the element is from 1's we turn 1's to 0's and 
we make the 0 after the last 1, into a 1
we keep doing this until we turn all the 0's to 1's.
'''
def makeBinary(n):
    lst = [0 for x in range(n)]
    #string representations of the membership list
    bn = [''.join([str(x) for x in lst])]
    #the while loop always terminates after 2^n iterations
    while sum(lst) < n:
        for i in range(n):
            if lst[-(i+1)] == 0:
                lst[-(i+1)] = 1
                break
            elif lst[-(i+1)] == 1:
                lst[-(i+1)] = 0
                if  i != n-1 and lst[-(i + 2)] == 0:
                    lst[-(i + 2)] = 1
                    break
                else:
                    continue
        bn.append(stringify(lst))
    return bn

#creates the powerset of a set/list
def generatePowerSet (lst):
    n = len(lst)
    binaries = makeBinary(n)
    powerset = []
    #relate the created membership list to our list elements
    for binary in binaries:
        curset = []
        for i in range(len(binary)):
            if binary[i] == '1':
                curset.append(lst[i])
        powerset.extend([curset])
    return powerset

#order powerset by subsets size and elements
def orderedPS (ps):
    return [[]] + sorted(ps[1:], key = lambda x: (len(x),x))

'''Algorithm Complexity

The makeBinary function makes 2^n iterations
and the generatePowerSet uses that function and
loop for 2^n times, therefore the asymptotic complexity
of the algorithm is O(2^n)

PS: Eventhough the algorithm has the same complexity as
that of the book I like my algorithm better because it is more
clear and straightforward

'''

""" #driver test
lst = [1,2,3]

ps = orderedPS(generatePowerSet(lst))

print(ps) """
