# helper script to generate encoded values for 4-bit input

def calculate_bits(data_bits):
    code= [0] * 8
    code[2] = data_bits[3] # d0
    code[4] = data_bits[2] # d1
    code[5] = data_bits[1] # d2
    code[6] = data_bits[0] # d3
    
    code[0] = data_bits[3] ^ data_bits[2] ^ data_bits[0]
    code[1] = data_bits[3] ^ data_bits[1] ^ data_bits[0]
    code[3] = data_bits[2] ^ data_bits[1] ^ data_bits[0]
    code[7] = code[0] ^ code[1] ^ code[2] ^ code[3] ^ code[4] ^ code[5] ^ code[6]
    
    flipped_code = code[::-1]
    return flipped_code

def main():
    while(True):
        data = input("Enter 4-bit data (e.g. 1011): ")
        if len(data) != 4 or any(bit not in "01" for bit in data):
            print("Please enter exactly 4 binary bits.")
            return

        data_bits = list(map(int, data))
        hamming_code = calculate_bits(data_bits)
        print("Hamming(8,4) code:", "".join(map(str, hamming_code)))

if __name__ == "__main__":
    main()

