#!/usr/bin/env python3
"""Deterministic Vault Tool for Archimedes (AES-256-GCM).

Provides secure local credential storage and in-memory injection with zero disk leakage.
"""

from __future__ import annotations

import argparse
import json
import os
import stat
import sys
from pathlib import Path

from cryptography.hazmat.primitives.ciphers.aead import AESGCM

DEFAULT_VAULT_DIR = Path(".vault")
DEFAULT_VAULT_FILE = DEFAULT_VAULT_DIR / "credentials.vault"
DEFAULT_KEY_FILE = DEFAULT_VAULT_DIR / "master.key"
ENV_KEY_VAR = "AGENT_VAULT_KEY"


def ensure_permissions(path: Path, is_dir: bool = False) -> None:
    """Ensure strict file or directory permissions (0700 dir, 0600 file)."""
    if not path.exists():
        return
    mode = stat.S_IRWXU if is_dir else (stat.S_IRUSR | stat.S_IWUSR)
    os.chmod(path, mode)


def get_or_create_key(vault_dir: Path = DEFAULT_VAULT_DIR) -> bytes:
    """Retrieve the AES-256 key from environment or local master.key."""
    vault_dir.mkdir(parents=True, exist_ok=True)
    ensure_permissions(vault_dir, is_dir=True)

    env_key = os.environ.get(ENV_KEY_VAR)
    if env_key:
        try:
            return bytes.fromhex(env_key.strip())
        except ValueError:
            return env_key.encode("utf-8")[:32].ljust(32, b"0")

    key_file = vault_dir / "master.key"
    if key_file.exists():
        key = key_file.read_bytes()
        if len(key) == 32:
            return key

    key = AESGCM.generate_key(bit_length=256)
    key_file.write_bytes(key)
    ensure_permissions(key_file, is_dir=False)
    return key


def load_vault(vault_file: Path = DEFAULT_VAULT_FILE, key: bytes | None = None) -> dict[str, str]:
    """Decrypt and load vault contents into memory dictionary."""
    if not vault_file.exists():
        return {}
    if key is None:
        key = get_or_create_key(vault_file.parent)

    raw_data = vault_file.read_bytes()
    if len(raw_data) < 12:
        return {}

    nonce = raw_data[:12]
    ciphertext = raw_data[12:]
    aesgcm = AESGCM(key)
    try:
        decrypted = aesgcm.decrypt(nonce, ciphertext, None)
        return json.loads(decrypted.decode("utf-8"))
    except Exception as exc:
        raise RuntimeError("Failed to decrypt vault. Incorrect key or corrupted file.") from exc


def save_vault(
    data: dict[str, str], vault_file: Path = DEFAULT_VAULT_FILE, key: bytes | None = None
) -> None:
    """Encrypt and write in-memory dictionary to vault file."""
    vault_dir = vault_file.parent
    vault_dir.mkdir(parents=True, exist_ok=True)
    ensure_permissions(vault_dir, is_dir=True)

    if key is None:
        key = get_or_create_key(vault_dir)

    aesgcm = AESGCM(key)
    nonce = os.urandom(12)
    serialized = json.dumps(data, ensure_ascii=False).encode("utf-8")
    ciphertext = aesgcm.encrypt(nonce, serialized, None)

    vault_file.write_bytes(nonce + ciphertext)
    ensure_permissions(vault_file, is_dir=False)


def main() -> None:
    parser = argparse.ArgumentParser(description="Archimedes AES-256-GCM Vault Manager")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # status
    subparsers.add_parser("status", help="Check vault health and file permissions")

    # set
    set_parser = subparsers.add_parser("set", help="Store or update a credential")
    set_parser.add_argument("--key", required=True, help="Credential identifier")
    set_parser.add_argument("--value", required=True, help="Secret value to store")

    # get
    get_parser = subparsers.add_parser("get", help="Retrieve a credential value in memory")
    get_parser.add_argument("--key", required=True, help="Credential identifier")

    # list
    subparsers.add_parser("list", help="List stored keys without exposing secrets")

    # delete
    del_parser = subparsers.add_parser("delete", help="Remove a credential")
    del_parser.add_argument("--key", required=True, help="Credential identifier")

    args = parser.parse_args()

    key = get_or_create_key()

    if args.command == "status":
        exists = DEFAULT_VAULT_FILE.exists()
        count = len(load_vault(DEFAULT_VAULT_FILE, key)) if exists else 0
        print(f"Vault Status: {'Initialized' if exists else 'Empty/Uninitialized'}")
        print(f"Vault Path: {DEFAULT_VAULT_FILE}")
        print(f"Total Secrets: {count}")
        sys.exit(0)

    elif args.command == "set":
        data = load_vault(DEFAULT_VAULT_FILE, key)
        data[args.key] = args.value
        save_vault(data, DEFAULT_VAULT_FILE, key)
        print(f"Successfully stored key: {args.key}")

    elif args.command == "get":
        data = load_vault(DEFAULT_VAULT_FILE, key)
        if args.key not in data:
            print(f"Error: key '{args.key}' not found in vault.", file=sys.stderr)
            sys.exit(1)
        print(data[args.key])

    elif args.command == "list":
        data = load_vault(DEFAULT_VAULT_FILE, key)
        if not data:
            print("Vault is empty.")
        else:
            print(f"Stored keys ({len(data)}):")
            for k in sorted(data.keys()):
                print(f" - {k}")

    elif args.command == "delete":
        data = load_vault(DEFAULT_VAULT_FILE, key)
        if args.key in data:
            del data[args.key]
            save_vault(data, DEFAULT_VAULT_FILE, key)
            print(f"Deleted key: {args.key}")
        else:
            print(f"Key '{args.key}' not found.", file=sys.stderr)
            sys.exit(1)


if __name__ == "__main__":
    main()
