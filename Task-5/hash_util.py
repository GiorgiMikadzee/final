import hashlib
import hmac
import json

SHARED_SECRET = b'bobplusaliceequalslove'


def compute_hmac(file_path: str, key: bytes) -> str:
    with open(file_path, 'rb') as f:
        msg = f.read()
    return hmac.new(key, msg, hashlib.sha256).hexdigest()


def save_tag(tag: str, output_file: str):
    with open(output_file, 'w') as f:
        json.dump({'hmac': tag}, f)


def verify_file(file_path: str, tag_file: str, key: bytes) -> str:
    with open(tag_file, 'r') as f:
        stored_tag = json.load(f)['hmac']
    current_tag = compute_hmac(file_path, key)
    return 'PASS' if hmac.compare_digest(stored_tag, current_tag) else 'FAIL'


# Write original message
with open("original.txt", 'w') as f:
    f.write("Bob, meet me at 7pm behind the office. Let's get married. Alice")

# Compute HMAC
hmac_tag = compute_hmac("original.txt", SHARED_SECRET)
save_tag(hmac_tag, "hashes.json")

# Write a tampered message
with open("tampered.txt", 'w') as f:
    f.write("Bob, meet me at 6pm in park. I want to break up. Alice")

# Verify both
with open("verification_result.txt", 'w') as f:
    f.write(f"original.txt: {verify_file('original.txt', 'hashes.json', SHARED_SECRET)}\n")
    f.write(f"tampered.txt: {verify_file('tampered.txt', 'hashes.json', SHARED_SECRET)}\n")
