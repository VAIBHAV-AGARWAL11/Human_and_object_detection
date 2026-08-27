import smtplib
import ssl
import socket
import sys

sender = "vv3151773@gmail.com"
app_password = "ermi zvzu vimv dwrs"
receiver = "akshatkumar67353@gmail.com"

print("=" * 60)
print("SMTP CONNECTION DIAGNOSTIC TOOL")
print("=" * 60)
print("Python Version:", sys.version)
print("-" * 60)

# Test 1: Simple TCP Socket connection
for port in [465, 587, 25]:
    print(f"Test 1.{port}: Connecting to smtp.gmail.com:{port} (TCP)...")
    try:
        s = socket.create_connection(("smtp.gmail.com", port), timeout=3)
        print(f"  -> SUCCESS! Plain TCP connection established to port {port}.")
        s.close()
    except Exception as e:
        print(f"  -> FAILED: {e}")
print("-" * 60)

# Test 2: SMTP SSL connection on 465
print("Test 2: Connecting via SMTP_SSL (Port 465)...")
try:
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context, timeout=5) as server:
        print("  -> Connection established. Attempting login...")
        server.login(sender, app_password)
        print("  -> LOGIN SUCCESS!")
except Exception as e:
    print(f"  -> FAILED: {e}")
print("-" * 60)

# Test 3: SMTP connection on 587 (TLS/STARTTLS)
print("Test 3: Connecting via SMTP + STARTTLS (Port 587)...")
try:
    with smtplib.SMTP("smtp.gmail.com", 587, timeout=5) as server:
        print("  -> Connection established. Starting TLS...")
        context = ssl.create_default_context()
        server.starttls(context=context)
        print("  -> TLS started. Attempting login...")
        server.login(sender, app_password)
        print("  -> LOGIN SUCCESS!")
except Exception as e:
    print(f"  -> FAILED: {e}")
print("-" * 60)

# Test 4: SMTP SSL connection with disabled cert verification (Mac certification issues check)
print("Test 4: Connecting via SMTP_SSL (Port 465) with disabled certificate verification...")
try:
    context = ssl._create_unverified_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context, timeout=5) as server:
        print("  -> Connection established. Attempting login...")
        server.login(sender, app_password)
        print("  -> LOGIN SUCCESS!")
except Exception as e:
    print(f"  -> FAILED: {e}")
print("=" * 60)
