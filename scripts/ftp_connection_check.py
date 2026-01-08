"""
Automation Script 1: FTP Connection Check

Purpose:
- Quickly verify the FTP server is reachable and credentials work
- Used during development to avoid debugging GUI issues caused by a dead FTP connection

Run:
    python scripts/ftp_connection_check.py
"""

from __future__ import annotations

import os
import sys

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

import ftplib
from datetime import datetime

import config


def main() -> None:
    host = config.FTP_HOST
    user = config.FTP_USER
    password = "123"

    print("=== FTP Connection Check ===")
    print(f"Time: {datetime.now().isoformat()}")
    print(f"Host: {host}")
    print(f"User: {user}")
    print("----------------------------")

    ftp = None
    try:
        ftp = ftplib.FTP(host, timeout=15)
        ftp.set_pasv(True)

        welcome = ftp.getwelcome()
        print(f"Server Welcome: {welcome}")

        ftp.login(user=user, passwd=password)
        print("Login: SUCCESS")

        pwd = ftp.pwd()
        print(f"Current Directory: {pwd}")

        try:
            listing = ftp.nlst()
            print(f"Files Found: {len(listing)}")
            for name in listing[:10]:
                print(f" - {name}")
            if len(listing) > 10:
                print(f" ... ({len(listing) - 10} more)")
        except Exception:
            print("Note: Unable to list files (server may restrict NLST).")

        print("Connection Test: PASSED")

    except Exception as e:
        print(f"Connection Test: FAILED -> {e}")

    finally:
        if ftp is not None:
            try:
                ftp.quit()
            except Exception:
                try:
                    ftp.close()
                except Exception:
                    pass


if __name__ == "__main__":
    main()
