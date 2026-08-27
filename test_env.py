import os
import sys

print("Python version:", sys.version)
print("Environment variables:")
for k, v in os.environ.items():
    if "proxy" in k.lower() or "mail" in k.lower() or "smtp" in k.lower() or "pass" in k.lower():
        print(f"{k}: {v}")
