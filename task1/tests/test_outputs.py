import subprocess
import os
import pytest
from datetime import datetime, timezone
from cryptography import x509
from cryptography.hazmat.backends import default_backend


SSL_DIR = "/app/ssl"
ROOT_CRT = f"{SSL_DIR}/root/root.crt"
INTERMEDIATE_CRT = f"{SSL_DIR}/intermediate/intermediate.crt"
LEAF_CRT = f"{SSL_DIR}/leaf/leaf.crt"
CHAIN_CRT = f"{SSL_DIR}/chain.crt"
FULLCHAIN_CRT = f"{SSL_DIR}/fullchain.crt"


def load_cert(path):
    with open(path, "rb") as f:
        return x509.load_pem_x509_certificate(f.read(), default_backend())


def test_root_cert_exists():
    assert os.path.exists(ROOT_CRT)

def test_intermediate_cert_exists():
    assert os.path.exists(INTERMEDIATE_CRT)

def test_leaf_cert_exists():
    assert os.path.exists(LEAF_CRT)

def test_chain_file_exists():
    assert os.path.exists(CHAIN_CRT)

def test_fullchain_file_exists():
    assert os.path.exists(FULLCHAIN_CRT)

def test_openssl_verifies_full_chain():
    """Verify leaf cert against the full chain using openssl."""
    result = subprocess.run(
        ["openssl", "verify", "-CAfile", ROOT_CRT, "-untrusted", CHAIN_CRT, LEAF_CRT],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0, f"Chain verification failed: {result.stderr}"

def test_openssl_verifies_intermediate_against_root():
    result = subprocess.run(
        ["openssl", "verify", "-CAfile", ROOT_CRT, INTERMEDIATE_CRT],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0, f"Intermediate verification failed: {result.stderr}"

def test_root_is_ca():
    cert = load_cert(ROOT_CRT)
    bc = cert.extensions.get_extension_for_class(x509.BasicConstraints)
    assert bc.value.ca is True

def test_root_is_self_signed():
    cert = load_cert(ROOT_CRT)
    assert cert.issuer == cert.subject

def test_root_key_size():
    cert = load_cert(ROOT_CRT)
    assert cert.public_key().key_size >= 4096

def test_intermediate_is_ca():
    cert = load_cert(INTERMEDIATE_CRT)
    bc = cert.extensions.get_extension_for_class(x509.BasicConstraints)
    assert bc.value.ca is True

def test_intermediate_not_self_signed():
    cert = load_cert(INTERMEDIATE_CRT)
    assert cert.issuer != cert.subject

def test_intermediate_signed_by_root():
    root = load_cert(ROOT_CRT)
    intermediate = load_cert(INTERMEDIATE_CRT)
    assert intermediate.issuer == root.subject

def test_intermediate_pathlen():
    cert = load_cert(INTERMEDIATE_CRT)
    bc = cert.extensions.get_extension_for_class(x509.BasicConstraints)
    assert bc.value.path_length == 0

def test_leaf_is_not_ca():
    cert = load_cert(LEAF_CRT)
    bc = cert.extensions.get_extension_for_class(x509.BasicConstraints)
    assert bc.value.ca is False

def test_leaf_signed_by_intermediate():
    intermediate = load_cert(INTERMEDIATE_CRT)
    leaf = load_cert(LEAF_CRT)
    assert leaf.issuer == intermediate.subject

def test_leaf_has_correct_cn():
    cert = load_cert(LEAF_CRT)
    cn = cert.subject.get_attributes_for_oid(x509.NameOID.COMMON_NAME)[0].value
    assert cn == "dev.example.com"

def test_leaf_has_san():
    cert = load_cert(LEAF_CRT)
    san = cert.extensions.get_extension_for_class(x509.SubjectAlternativeName)
    dns_names = san.value.get_values_for_type(x509.DNSName)
    assert "dev.example.com" in dns_names

def test_leaf_has_server_auth_eku():
    cert = load_cert(LEAF_CRT)
    eku = cert.extensions.get_extension_for_class(x509.ExtendedKeyUsage)
    assert x509.ExtendedKeyUsageOID.SERVER_AUTH in eku.value

def test_leaf_not_expired():
    cert = load_cert(LEAF_CRT)
    assert cert.not_valid_after_utc > datetime.now(timezone.utc)

def test_leaf_key_size():
    cert = load_cert(LEAF_CRT)
    assert cert.public_key().key_size >= 2048

def test_chain_contains_intermediate():
    with open(CHAIN_CRT) as f:
        content = f.read()
    with open(INTERMEDIATE_CRT) as f:
        intermediate_pem = f.read()
    assert intermediate_pem.strip() in content.strip()

def test_chain_contains_root():
    with open(CHAIN_CRT) as f:
        content = f.read()
    with open(ROOT_CRT) as f:
        root_pem = f.read()
    assert root_pem.strip() in content.strip()

def test_fullchain_contains_leaf():
    with open(FULLCHAIN_CRT) as f:
        content = f.read()
    with open(LEAF_CRT) as f:
        leaf_pem = f.read()
    assert leaf_pem.strip() in content.strip()
