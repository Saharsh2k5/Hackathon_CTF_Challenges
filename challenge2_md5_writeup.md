# Challenge 2 Write-up: Bait-and-Switch Hard (MD5 Edition, Port 9999)

## Objective
Create and submit two different valid PDF files such that:
1. `MD5(file1) == MD5(file2)`
2. `SHA256(file1) != SHA256(file2)`

## Service Rules (Observed)
The service on port `9999` provides a base64 challenge PDF and asks for two base64 submissions, each terminated by a line containing only `.`.

## Key Discovery
The provided PDF already contains two embedded collision candidates:
- A primary collision payload inside the live stream section.
- An alternate collision payload between markers after EOF:
  - `% ALTERNATE_BLOCK_BEGIN`
  - `% ALTERNATE_BLOCK_END`

## Approach

### 1. Decode provided PDF
- Extract base64 from banner and decode to `hard_file1.pdf`.

### 2. Locate payloads in raw bytes
- Primary region begins after:
  - `% collision block follows\n% `
- In this challenge, that region length is `135` bytes:
  - `7` fixed prefix bytes + `128` collision bytes.
- Alternate region is exactly `128` bytes between:
  - `% ALTERNATE_BLOCK_BEGIN\n% ` and `\n% ALTERNATE_BLOCK_END`

### 3. Construct second PDF correctly
Important: replace only the `128-byte` collision payload, not the full `135-byte` primary region.

- Keep the 7-byte fixed prefix untouched.
- Swap primary 128-byte block with alternate 128-byte block.
- Save as `hard_file2.pdf`.

## Local Verification
Validate before submitting:
1. `MD5(hard_file1.pdf) == MD5(hard_file2.pdf)`
2. `SHA256(hard_file1.pdf) != SHA256(hard_file2.pdf)`
3. Both are valid PDFs.

Observed successful pair:
- MD5 (both): `d22da871000aebfbf977a3eb9161e8f2`
- SHA256 file1: `54f94df31bba4dd0c113e901e3d735a10da5c7a7aa81824aea2a0602168c1fe7`
- SHA256 file2: `8102463b24bad6c2bf4a080e3a2cdee11eecc1052fc18c5af6fa2edbabb652ff`

## Submission Flow
1. Connect to `nc 4.188.84.14 9999`.
2. Submit base64 of `hard_file1.pdf`, then `.` line.
3. Submit base64 of `hard_file2.pdf`, then `.` line.
4. Service checks and accepts when:
   - both valid PDFs
   - MD5 matches
   - SHA256 differs

## Why This Works
- MD5 collision blocks were intentionally embedded in the challenge PDF.
- Correct byte-aligned block substitution preserves MD5 while changing the actual file contents.
- Since contents differ, SHA256 diverges.

## Pitfalls Avoided
- Replacing the full marked primary region breaks the collision due to length mismatch.
- Swapping exactly the aligned 128-byte payload is required.
- Base64 line wrapping and prompt-aware socket I/O prevent timeout/protocol issues.
