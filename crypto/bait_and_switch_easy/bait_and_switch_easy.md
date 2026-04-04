# Challenge 1 Write-up: Bait-and-Switch (CRC32 Edition, Port 8888)

## Objective
Create and submit two different valid PDF files such that:
1. `CRC32(file1) == CRC32(file2)`
2. `MD5(file1) != MD5(file2)`

## Service Rules (Observed)
The service on port `8888` provides a base64-encoded challenge PDF and asks for two base64 file submissions (each terminated by a line containing only `.`).

## Approach

### 1. Decode the provided challenge PDF
- Read server banner.
- Extract base64 content between `--- BEGIN BASE64 ---` and `--- END BASE64 ---`.
- Decode to `crc_file1.pdf`.

### 2. Build a second valid PDF candidate
- Start from the original bytes.
- Append harmless trailing PDF comment text (keeps file parser-tolerant):
  - `\n% switched\n`
- Reserve 4 bytes at the end for a CRC correction patch.

### 3. Compute exact 4-byte CRC32 correction patch
CRC32 is linear over GF(2), so the final CRC can be forced by solving a 32x32 linear system.

- Let `prefix = original + b"\n% switched\n"`.
- Let `base_crc = CRC32(prefix + 00 00 00 00)`.
- For each bit position `i` in a 32-bit patch:
  - Build patch `p_i = (1 << i)` as 4 little-endian bytes.
  - Compute influence column `col_i = CRC32(prefix + p_i) XOR base_crc`.
- Build matrix `M` from these 32 columns.
- Target delta is:
  - `target_delta = CRC32(original) XOR base_crc`
- Solve `M * x = target_delta` in GF(2) using Gaussian elimination.
- Convert solved 32-bit vector `x` to little-endian bytes and append as patch.

Resulting file:
- `crc_file2.pdf = prefix + patch`

## Local Verification
Check before submission:
1. `CRC32(crc_file1.pdf) == CRC32(crc_file2.pdf)`
2. `MD5(crc_file1.pdf) != MD5(crc_file2.pdf)`
3. Both files still parse as valid PDFs (accepted by checker).

Observed successful values:
- Target CRC32: `04fea22e`
- Computed patch (little-endian): `ee9d0b89`

## Submission Flow
1. Connect to `nc 4.188.84.14 8888`.
2. Paste base64 of `crc_file1.pdf`, then send `.` on a new line.
3. Paste base64 of `crc_file2.pdf`, then send `.` on a new line.
4. Service confirms:
   - both valid PDFs
   - CRC32 match
   - MD5 differs

## Why This Works
- CRC32 is not collision-resistant; it is a linear checksum.
- With 32 controllable patch bits, a 32-bit CRC target can be matched exactly.
- MD5 changes automatically because bytes differ.
- PDF parsers/checkers typically tolerate trailing non-structural bytes/comments.

## Minimal Repro Notes
- Use wrapped base64 lines (for terminal stability).
- Wait for prompts before sending next block.
- Treat socket output as bytes when needed to avoid console encoding issues.
