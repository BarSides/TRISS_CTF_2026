# Reference solver: runs the towel_check loop backwards.
# expected[] is copied out of the binary (Ghidra: the 44-byte array the loop compares against).
expected = bytes.fromhex("464bd2f4239a8efdd62e35511881c9e02593643bd3d7e6bf9f0e9231a281311554a6f5ecb1ef48f027839adb")
key = b"TOWEL"

out = []
for i, e in enumerate(expected):
    c = (e - 7 * i) & 0xFF                 # undo the add
    c ^= key[i % len(key)]                 # undo the XOR
    c = ((c >> 3) | (c << 5)) & 0xFF       # undo rotate-left-3 with rotate-right-3
    out.append(c)
print(bytes(out).decode())
