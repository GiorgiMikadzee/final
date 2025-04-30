import hashlib
import json


def compute_hashes(file_path: str) -> dict:
    with open(file_path, 'rb') as f:
        data = f.read()
    return {
        "md5": hashlib.md5(data).hexdigest(),
        "sha1": hashlib.sha1(data).hexdigest(),
        "sha256": hashlib.sha256(data).hexdigest()
    }


def save_hashes(hashes: dict, output_file: str):
    with open(output_file, 'w') as f:
        json.dump(hashes, f, indent=2)


def verify_integrity(file_path: str, hash_file: str) -> str:
    current = compute_hashes(file_path)
    with open(hash_file, 'r') as f:
        saved = json.load(f)
    return "PASS" if saved == current else "FAIL"


# Step 1: Create original file
with open("original.txt", 'w') as f:
    f.write("Bob, meet me at 5pm behind the office. Let's get married.")

# Step 2: Compute & Save Hashes
save_hashes(compute_hashes("original.txt"), "hashes.json")

# Step 3: Tamper the file
with open("tampered.txt", 'w') as f:
    f.write("Bob, meet me at 6pm in the park. I want to break up.")

# Step 4: Verify both files
with open("verification_result.txt", 'w') as f:
    f.write(f"original.txt: {verify_integrity('original.txt', 'hashes.json')}\n")
    f.write(f"tampered.txt: {verify_integrity('tampered.txt', 'hashes.json')}\n")
