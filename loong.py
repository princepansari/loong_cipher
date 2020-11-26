constants = [0x01, 0x03, 0x07, 0x0F, 0x1F, 0x3E, 0x3D, 0x3B, 0x37, 0x2F, 0x1E,
			0x3C, 0x39, 0x33, 0x27, 0x0E, 0x1D, 0x3A, 0x35, 0x2B, 0x16, 0x2C,
			0x18, 0x30, 0x21, 0x02, 0x05, 0x0B, 0x17, 0x2E, 0x1C, 0x38, 0x31]


def addRoundKey(state, round_key, const):
	matrix = [[0] * 4 for _ in range(4)]
	rc=[]
	for i in range(6):
		rc.append(const%2)
		const = int(const/2)
	a = rc[5] or rc[4] or rc[3]
	b = rc[2] or rc[1] or rc[0]
	round_constant = [[0, 0, 0, a], [0, 0, 1, b], [0, 0, 2, a], [0, 0, 4, b]]
	for i in range(4):
		for j in range(4):
			matrix[i][j] = state[i][j] ^ round_key[i][j] ^ round_constant[i][j]
	return matrix

def subcell(state):
	matrix = [[0] * 4 for _ in range(4)]
	sbox = [0x0C, 0x0A, 0x0D, 0x03, 0x0E, 0x0B, 0x0F, 0x07, 0x09, 0x08, 0x01, 0x05,0x00, 0x02, 0x04, 0x06]
	for i in range(4):
		for j in range(4):
			matrix[i][j] = sbox[state[i][j]]
	return matrix

def galoisMultiplication(a, b):
    ans = 0
    for i in range(4):
        if b & 1:
            ans ^= a
        check = a & 8
        a = a << 1
        b = b >> 1
        if check == 8:
            a ^= 3
    return ans % 16

def mixRow(state):
	matrix = [[0] * 4 for _ in range(4)]
	mat = [[1, 4, 9, 13], [4, 1, 13, 9], [9, 13, 1, 4], [13, 9, 4, 1]]
	for i in range(4):
		for j in range(4):
			temp = 0
			for k in range(4):
				temp = temp ^ galoisMultiplication(state[i][k], mat[k][j])
			matrix[i][j] = temp
	return matrix

def mixColumn(state):
	matrix = [[0] * 4 for _ in range(4)]
	mat = [ [13, 9, 4, 1], [9, 13, 1, 4], [4, 1, 13, 9], [1, 4, 9, 13]]
	for i in range(4):
		for j in range(4):
			temp = 0
			for k in range(4):
				temp = temp ^ galoisMultiplication(mat[i][k], state[k][j])
			matrix[i][j] = temp
	return matrix

def cipher_from_state(state):
	cipher = ""
	for i in range(4):
		for x in state[i]:
			cipher += "{:01x}".format(x)
	return cipher


def algo_64bit(text, key, rc):
	state = [[0] * 4 for _ in range(4)]
	round_key = [[0] * 4 for _ in range(4)]
	for i in range(4):
		for j in range(4):
			state[i][j] = int(text[4*i+j], 16)
			round_key[i][j] = int(key[4*i+j], 16)
	state = addRoundKey(state, round_key, rc[0])
	for i in range(1, 17):
		state = subcell(state)
		state = mixRow(state)
		state = mixColumn(state)
		state = subcell(state)
		state = addRoundKey(state, round_key, rc[i])
	ciphertext = cipher_from_state(state)
	return ciphertext

def algo_80bit(text, key, rc):
	state = [[0] * 4 for _ in range(4)]
	round_key0 = [[0] * 4 for _ in range(4)]
	round_key1 = [[0] * 4 for _ in range(4)]
	for i in range(4):
		for j in range(4):
			state[i][j] = int(text[4*i+j], 16)
			round_key0[i][j] = int(key[4*i+j], 16)
			if i == 0:
				round_key1[i][j] = int(key[16+j], 16)
			else:
				round_key1[i][j] = int(key[4*(i-1)+j], 16)
	state = addRoundKey(state, round_key0, rc[0])
	for i in range(1, 21):
		state = subcell(state)
		state = mixRow(state)
		state = mixColumn(state)
		state = subcell(state)
		if i % 2:
			state = addRoundKey(state, round_key1, rc[i])
		else:
			state = addRoundKey(state, round_key0, rc[i])
	ciphertext = cipher_from_state(state)
	return ciphertext

def algo_128bit(text, key, rc):
	state = [[0] * 4 for _ in range(4)]
	round_key0 = [[0] * 4 for _ in range(4)]
	round_key1 = [[0] * 4 for _ in range(4)]
	for i in range(4):
		for j in range(4):
			state[i][j] = int(text[4*i+j], 16)
			round_key0[i][j] = int(key[4*i+j], 16)
			round_key1[i][j] = int(key[16+4*i+j], 16)
	state = addRoundKey(state, round_key0, rc[0])
	for i in range(1, 33):
		state = subcell(state)
		state = mixRow(state)
		state = mixColumn(state)
		state = subcell(state)
		if i % 2:
			state = addRoundKey(state, round_key1, rc[i])
		else:
			state = addRoundKey(state, round_key0, rc[i])
	ciphertext = cipher_from_state(state)
	return ciphertext


def encryption(n, plaintext, key):
	if n == 64 and len(plaintext) == 16 and len(key) == 16:
		cipher = algo_64bit(plaintext, key, constants)
	elif n == 80 and len(plaintext) == 16 and len(key) == 20:
		cipher = algo_80bit(plaintext, key, constants)
	elif n == 128 and len(plaintext) == 16 and len(key) == 32:
		cipher = algo_128bit(plaintext, key, constants)
	else:
		return "Wrong Input" 
	return cipher


def decryption(n, cipher, key):
	if n == 64 and len(cipher) == 16 and len(key) == 16:
		reverse_constant = constants[0:17][::-1]
		plaintext = algo_64bit(cipher, key, reverse_constant)
	elif n == 80 and len(cipher) == 16 and len(key) == 20:
		reverse_constant = constants[0:21][::-1]
		plaintext = algo_80bit(cipher, key, reverse_constant)
	elif n == 128 and len(cipher) == 16 and len(key) == 32:
		reverse_constant = constants[0:33][::-1]
		plaintext = algo_128bit(cipher, key, reverse_constant)
	else:
		return "Wrong Input" 
	return plaintext


n = 128
plaintext = "0000000000000000"
key = "00000000000000000000000000000000"
print(plaintext)
ciphertext = encryption(n, plaintext, key)
print(ciphertext)
text = decryption(n, ciphertext, key)
print(text)
print()



n = 80
plaintext = "0000000000000000"
key = "00000000000000000000"
print(plaintext)
ciphertext = encryption(n, plaintext, key)
print(ciphertext)
text = decryption(n, ciphertext, key)
print(text)
print()



n = 64
plaintext = "0000000000000000"
key = "0000000000000000"
print(plaintext)
ciphertext = encryption(n, plaintext, key)
print(ciphertext)
text = decryption(n, ciphertext, key)
print(text)
print()


