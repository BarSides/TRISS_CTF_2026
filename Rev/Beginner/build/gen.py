# Prints the encoded byte arrays used in skip_the_line.c.
CODE = b"KENNYWOOD1898"
FLAG = b"BarSides{skipped_the_line_at_kennywood}"
K = 0x5A
fmt = lambda bs: ", ".join(f"0x{b:02x}" for b in bs)
print("code:", fmt(c ^ K for c in CODE))
print("flag:", fmt(f ^ CODE[i % len(CODE)] for i, f in enumerate(FLAG)))
