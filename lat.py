#to compute the special product of the two numbers in bitwise manner, i.e here compute mask
def mask(mask_bit, x):
	output = 0
	while mask_bit > 0 and x > 0:
		temp = int(mask_bit % 2) * int(x % 2) #Product of ith bit  of mask and ith bit of x
		output = output ^ int(temp) #xor with the product of same ith bit of mask and ith bit of x
		mask_bit /= 2
		x /= 2
	return output

#To compute bias given alpha and beta for the SBOX	
def compute(alpha, beta):
	count  = 0
	for x in range(16):
		if mask(alpha,x) == mask(beta,sbox[x]):
			count += 1  #incrementing counter for matching condition of LHS and RHS
	return count - 8

sbox = [12, 10, 13, 3, 14, 11, 15, 7, 9, 8, 1, 5, 0, 2, 4, 6]#SBOX from previos assignment
lat = [[0] * 16 for _ in range(16)] #2-D array for Linear Approximation Table

for alpha in range(16):
	for beta in range(16):
		lat[alpha][beta] = compute(alpha, beta) #For each pair (alpha and beta) ranging from 0-15 calculate its biasing and store 

#Printing LAT TABLE
for alpha in range(16):
	for beta in range(16):
		print(lat[alpha][beta], end ="\t") # displaying elements of the LAT
	print()



# This code can be used for Latex
# for alpha in range(16):
# 	print(alpha, end =" & ")
# 	for beta in range(16):
# 		if lat[alpha][beta]:
# 			print(lat[alpha][beta], end ="")
# 		else:
# 			print("-", end = "")
# 		if beta != 15:
# 			print(" & ", end ="")
# 	print(" \\\\")
# 	print("\\hline")