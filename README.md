# File Integrity Checker GitHub Action

This GitHub Action calculates the SHA256 checksum of files in your repository to verify their integrity. It is useful for tracking file changes and ensuring that the content of files hasn't been tampered with during the CI/CD process.

## Usage

### Inputs:
- `path`: (Optional) The directory to check for modified files. Defaults to `./` (repository root).

### Outputs:
- `checksums`: A string containing the SHA256 checksums of the modified files.

### Example Workflow

```yaml
name: Check File Integrity

on:
  push:
    branches:
      - main

jobs:
  integrity-check:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v3

      - name: Run File Integrity Checker
        id: sha-check
        uses: username/file-integrity-action@main
        with:
          path: "./"

      - name: Display SHA256
        run: echo "SHA of recent files: ${{ steps.sha-check.outputs.checksums }}"
