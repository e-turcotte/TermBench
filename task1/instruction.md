# Generate a Valid SSL Certificate Chain

Generate a three-tier SSL certificate chain using OpenSSL and save all files
under `/app/ssl/`. The chain should consist of a root CA, an intermediate CA
signed by the root, and a leaf certificate signed by the intermediate.

## Requirements

### Directory Structure
Create the following files:
- `/app/ssl/root/root.key` — Root CA private key
- `/app/ssl/root/root.crt` — Root CA certificate
- `/app/ssl/intermediate/intermediate.key` — Intermediate CA private key
- `/app/ssl/intermediate/intermediate.crt` — Intermediate CA certificate
- `/app/ssl/leaf/leaf.key` — Leaf private key
- `/app/ssl/leaf/leaf.crt` — Leaf certificate
- `/app/ssl/chain.crt` — Intermediate + Root concatenated
- `/app/ssl/fullchain.crt` — Leaf + Intermediate concatenated

### Root CA
- Key size: 4096 bits
- Self-signed
- Must have `CA:TRUE` basic constraint
- Valid for at least 1024 days

### Intermediate CA
- Key size: 4096 bits
- Signed by the root CA
- Must have `CA:TRUE` basic constraint
- Must have `pathlen:0` constraint
- Valid for at least 512 days

### Leaf Certificate
- Key size: at least 2048 bits
- Signed by the intermediate CA
- Common Name: `dev.example.com`
- Must have `CA:FALSE` basic constraint
- Must include a Subject Alternative Name (SAN) for `DNS:dev.example.com`
- Must include Extended Key Usage: `serverAuth`
- Valid for at least 365 days

## Verification

The chain must pass the following OpenSSL verification command without errors:

```bash
openssl verify -CAfile /app/ssl/root/root.crt \
    -untrusted /app/ssl/chain.crt \
    /app/ssl/leaf/leaf.crt
```
