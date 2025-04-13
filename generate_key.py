import os
import secrets

key = secrets.token_hex(32)
os.makedirs("shared", exist_ok=True)
with open("shared/api_key.txt", "w") as f:
    f.write(key)

print(f"Generated API key:\n{key}")