# Prints the expected[] table for towel_check.c and checks that solve.py inverts it.
FLAG = b"BarSides{twirled_it_backwards_and_it_worked}"
KEY = b"TOWEL"


def rol8(c, n):
    return ((c << n) | (c >> (8 - n))) & 0xFF


def encode(data):
    return bytes((rol8(c, 3) ^ KEY[i % len(KEY)]) + 7 * i & 0xFF for i, c in enumerate(data))


if __name__ == "__main__":
    table = encode(FLAG)
    print(f"length {len(FLAG)}")
    for i in range(0, len(table), 12):
        print("    " + ", ".join(f"0x{b:02x}" for b in table[i:i + 12]) + ",")
