"""
Per-user dataset/model ownership.

Storage keys (the `dataset_name` used throughout the filesystem layout and
API paths) are namespaced with the owning user's id: `u{user_id}_{name}`.
This gives real isolation without a database lookup on every request - a
user's JWT fixes their own id, so they can never construct a key that
passes `require_owner` for another user's data, even if they guess or
enumerate dataset names.
"""

import re

from fastapi import HTTPException


def make_dataset_key(user_id: int, name: str) -> str:
    safe_name = re.sub(r"[^A-Za-z0-9._-]", "_", name)
    return f"u{user_id}_{safe_name}"


def owner_prefix(user_id: int) -> str:
    return f"u{user_id}_"


def is_owner(dataset_name: str, user_id: int) -> bool:
    return dataset_name.startswith(owner_prefix(user_id))


def require_owner(dataset_name: str, user_id: int) -> None:
    """
    Raise 404 (not 403) if this dataset key doesn't belong to user_id, so
    we never confirm to a caller that a dataset with that name exists at
    all under someone else's account.
    """
    if not is_owner(dataset_name, user_id):
        raise HTTPException(status_code=404, detail="Dataset not found.")
