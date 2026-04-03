# OTP Chapter 3 Write-up

## Challenge
- Name: OTP Chapter 3
- Points: 50
- Target: http://4.188.84.14:4444/
- Given credentials:
  - Email: manish@iitgn.ac.in
  - Password: pineapple321

## Goal
Bypass the OTP layer and retrieve the flag without brute force.

## Recon Summary
1. Login form posts to /verify.
2. Successful login returns OTP page that posts to verify/process.php.
3. verify/process.php returns a page that performs AJAX POST to check.php with:
   - goodness: "0"
4. Normal flow with a wrong OTP returns HTTP 401 and body Bad OTP!.

## Vulnerability
The backend is vulnerable to duplicate parameter handling inconsistency (parameter pollution / type confusion style issue).

When posting duplicate keys for goodness in this exact order:
- goodness=0
- goodness=1

the OTP check logic reaches the success branch and returns the flag.

## Exploit
### Step flow
1. Authenticate with provided email/password.
2. Submit any OTP digits to verify/process.php (only to advance state).
3. POST to verify/check.php with duplicate goodness values in ordered array form:
   - goodness=["0", "1"]
4. Read response body for flag.

## Final Flag
HRCTF{SM4LL_M1ST4K3_B1G_PR0BL3M}

## Minimal HTTP idea
- /verify (POST): valid credentials
- /verify/process.php (POST): any otp_1..otp_6
- /verify/check.php (POST): duplicate goodness keys, ordered as 0 then 1

## Notes
- No brute forcing required.
- Root cause is unsafe server-side handling of repeated parameters.
- This is a classic small-validation-mistake, big-security-impact bug.
