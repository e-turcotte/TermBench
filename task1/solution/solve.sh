#!/bin/bash
set -e

mkdir -p /app/ssl/{root,intermediate,leaf}

# --- Root CA ---
openssl genrsa -out /app/ssl/root/root.key 4096

openssl req -x509 -new -nodes \
    -key /app/ssl/root/root.key \
    -sha256 -days 1024 \
    -out /app/ssl/root/root.crt \
    -subj "/C=US/ST=California/O=RootCA/CN=Root CA"

# --- Intermediate CA ---
openssl genrsa -out /app/ssl/intermediate/intermediate.key 4096

openssl req -new \
    -key /app/ssl/intermediate/intermediate.key \
    -out /app/ssl/intermediate/intermediate.csr \
    -subj "/C=US/ST=California/O=IntermediateCA/CN=Intermediate CA"

# Create extensions file for intermediate CA
cat > /app/ssl/intermediate/intermediate.ext << EOF
basicConstraints=critical,CA:TRUE,pathlen:0
keyUsage=critical,keyCertSign,cRLSign
subjectKeyIdentifier=hash
authorityKeyIdentifier=keyid:always,issuer
EOF

openssl x509 -req \
    -in /app/ssl/intermediate/intermediate.csr \
    -CA /app/ssl/root/root.crt \
    -CAkey /app/ssl/root/root.key \
    -CAcreateserial \
    -out /app/ssl/intermediate/intermediate.crt \
    -days 512 \
    -sha256 \
    -extfile /app/ssl/intermediate/intermediate.ext

# --- Leaf Certificate ---
openssl genrsa -out /app/ssl/leaf/leaf.key 2048

openssl req -new \
    -key /app/ssl/leaf/leaf.key \
    -out /app/ssl/leaf/leaf.csr \
    -subj "/C=US/ST=California/O=MyOrg/CN=dev.example.com"

cat > /app/ssl/leaf/leaf.ext << EOF
basicConstraints=critical,CA:FALSE
keyUsage=critical,digitalSignature,keyEncipherment
extendedKeyUsage=serverAuth
subjectAltName=DNS:dev.example.com
subjectKeyIdentifier=hash
authorityKeyIdentifier=keyid:always,issuer
EOF

openssl x509 -req \
    -in /app/ssl/leaf/leaf.csr \
    -CA /app/ssl/intermediate/intermediate.crt \
    -CAkey /app/ssl/intermediate/intermediate.key \
    -CAcreateserial \
    -out /app/ssl/leaf/leaf.crt \
    -days 365 \
    -sha256 \
    -extfile /app/ssl/leaf/leaf.ext

# --- Bundle the chain ---
cat /app/ssl/intermediate/intermediate.crt /app/ssl/root/root.crt \
    > /app/ssl/chain.crt

cat /app/ssl/leaf/leaf.crt /app/ssl/intermediate/intermediate.crt \
    > /app/ssl/fullchain.crt
