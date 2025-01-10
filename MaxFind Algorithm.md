#algorithm  #dataminig #ADM


maxFind(A):
input : A: array of size n 
ouptut : the maximum among the values in A ;
	max <- A[1]
	for i = 2 to n :
		if A[i] > A[1]:
			max <- A[i]
		end if 
	end for 
	return max 

how to check computational cost :: 

1. Function MaxFind(A)
2. Input: A: Array of size n
3. Output: The maximum among the values in A
4. max ← A[1]
5. i ← 2
6. while i ≤ n:
7.     if A[i] > max:
8.         max ← A[i]
9.     end if
10.    i ← i + 1
11. end while
12. return max
