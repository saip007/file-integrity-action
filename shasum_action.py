import hashlib
import subprocess
import os
import json

# Function to compute the SHA256 checksum of a file
def compute_sha256(file_path):
    sha256_hash = hashlib.sha256()
    try:
        with open(file_path, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()
    except Exception as e:
        print(f"Error processing file {file_path}: {str(e)}")
        return None

# Function to get a list of modified files in the most recent commit
def get_modified_files():
    try:
        # Get a list of files modified in the latest commit (excluding merges)
        result = subprocess.run(
            ["git", "diff", "--name-only", "HEAD^", "HEAD"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True
        )
        modified_files = result.stdout.decode("utf-8").strip().split("\n")
        return [file for file in modified_files if file]
    except subprocess.CalledProcessError as e:
        print(f"Error getting git diff: {e.stderr.decode('utf-8')}")
        return []

def main():
    # Get the list of modified files in the most recent commit
    modified_files = get_modified_files()

    if not modified_files:
        print("No files to check.")
        return

    checksums = {}

    for file in modified_files:
        if os.path.exists(file):
            checksum = compute_sha256(file)
            if checksum:
                checksums[file] = checksum
                print(f"Checksum for {file}: {checksum}")
        else:
            print(f"File {file} does not exist!")

    # Output the checksums as a JSON string for use in the GitHub Action
    if checksums:
        print(f"::set-output name=checksums::{json.dumps(checksums)}")

if __name__ == "__main__":
    main()
