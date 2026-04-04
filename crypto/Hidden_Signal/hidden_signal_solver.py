#!/usr/bin/env python3
"""Solve the Hidden Signal whitespace-stego challenge.

Rule used:
- Single space between words -> bit 0
- Double space between words -> bit 1

The collected bit string is interpreted as binary and converted to decimal.
"""

import re

TEXT = (
    "My love grows quietly when  I think of  you  smiling, choosing me daily, "
    "holding hope,  sharing  silence,  and  building  tomorrow together with "
    "patience,  laughter, courage,  trust,  warmth  forever  always  still here."
)


def decode_spaces_to_decimal(text: str) -> tuple[str, int]:
    # Capture all runs of spaces between tokens.
    gaps = re.findall(r" +", text)
    bits = "".join("1" if len(g) == 2 else "0" for g in gaps)
    value = int(bits, 2)
    return bits, value


def main() -> None:
    bits, value = decode_spaces_to_decimal(TEXT)
    print("bitstring:", bits)
    print("decimal:", value)
    print(f"flag: HRCTF{{{value}}}")


if __name__ == "__main__":
    main()
