# This function will generate ddt for given sbox and print the ddt table.


# Function to print ddt for document ot latex
def print_latex(table):
    length = len(table[0])
    for i in range(16):
        print(i, end=" & ")
        for j in range(16):
            if j != 15:
                if table[i][j] == 0:
                    print(' - & ', end="")
                else:
                    print(table[i][j], end=" & ")
            else:
                if table[i][j] == 0:
                    print(' - \\\\')
                else:
                    print(table[i][j], end=" \\\\\n")
        print("\\hline")

# Function to get DDT of a given sbox


def DDT(sbox):
    length = len(sbox)
    # Creating a 2d array of the size of SBox
    ddt_table = [[0] * length for _ in range(length)]
    for i in range(length):
        for j in range(length):
            inp_diff = i ^ j  # Finding Input difference
            out_diff = sbox[i] ^ sbox[j]  # Finding output difference
            # Increasing the value of cell corresponding to input_diff and out_diff
            ddt_table[inp_diff][out_diff] += 1

    for i in range(length):
        for j in range(length):
            print(ddt_table[i][j], end="\t")
        print()
    # print_latex(ddt_table)


sbox = [12, 10, 13, 3, 14, 11, 15, 7, 9, 8, 1, 5, 0, 2, 4, 6]
DDT(sbox)
