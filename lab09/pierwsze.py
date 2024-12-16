# wyszukanie liczb pierwszych z zakresu od l do r

l=2
r=100_000_0

def pierwsza(k):
# sprawdzenie, czy k jest pierwsza
 for i in range (2,k-1):
   if i*i>k:
     return True
   if k%i == 0:
     return False
 return True

pierwsze = []
for i in range (l,r+1):
  if pierwsza(i):
    pierwsze.append(i)

# print(pierwsze)
