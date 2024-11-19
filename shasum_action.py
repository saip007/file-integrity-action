import os
import hashlib

def calculate_sha256(filepath):
    sha256_hash = hashlib.sha256()
    with open(filepath, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

# Get all recently modified files in the current directory
recent_files = [f for f in os.listdir(".") if os.path.isfile(f)]
sha_list = []
for file in recent_files:
    sha = calculate_sha256(file)
    sha_list.append(f"{file}: {sha}")

# Join SHAs into a single string
output = "\n".join(sha_list)

# Write the output to a GitHub Actions environment file
with open(os.environ["GITHUB_OUTPUT"], "a") as env_file:
    env_file.write(f"checksums={output}\n")
