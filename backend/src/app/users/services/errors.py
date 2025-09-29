
from __future__ import annotations
import logging
from typing import Optional, Tuple
from sqlalchemy.exc import IntegrityError, DBAPIError

log = logging.getLogger(__name__)

CONSTRAINT_MESSAGES = {
    "users_username_key": "Username already exists",
    "uq_users_username": "Username already exists",
    "users_email_key": "Email already exists",
    "uq_users_email": "Email already exists",
    "users_phone_number_key": "Phone Number already registered",
    "uq_users_phone_number": "Phone Number already registered",
    "fk_users_org_id_organizations_id": "Organization does not exist",
    "ck_users_birth_date": "Invalid birth date",
}


PG_UNIQUE_VIOLATION = "23505"
PG_FOREIGN_KEY_VIOLATION = "23503"
PG_CHECK_VIOLATION = "23514"
PG_NOT_NULL_VIOLATION = "23502"

def _get_sqlstate(exc: DBAPIError) -> Optional[str]:
    """Пытаемся достать SQLSTATE из orig (asyncpg/psycopg2)."""
    orig = getattr(exc, "orig", None)
    if not orig:
        return None
    sqlstate = getattr(orig, "sqlstate", None) or getattr(orig, "pgcode", None)
    return sqlstate

def _get_constraint_name(exc: DBAPIError) -> Optional[str]:
    """Имя констрейнта (если есть)."""
    orig = getattr(exc, "orig", None)
    if not orig:
        return None

    cname = getattr(orig, "constraint_name", None)

    return cname

def classify_integrity_error(e: IntegrityError) -> Tuple[int, str]:

    sqlstate = _get_sqlstate(e)
    cname = _get_constraint_name(e)

    log.warning("IntegrityError sqlstate=%s constraint=%s message=%s", sqlstate, cname, str(e.orig))

    if cname and cname in CONSTRAINT_MESSAGES:
        code = 409 if sqlstate == PG_UNIQUE_VIOLATION else 400
        return code, CONSTRAINT_MESSAGES[cname]

    # 2) по SQLSTATE
    if sqlstate == PG_UNIQUE_VIOLATION:
        return 409, "Duplicate value violates unique constraint"
    if sqlstate == PG_FOREIGN_KEY_VIOLATION:
        return 400, "Referenced object does not exist"
    if sqlstate == PG_NOT_NULL_VIOLATION:
        return 400, "Required field is missing"
    if sqlstate == PG_CHECK_VIOLATION:
        return 400, "Value violates a check constraint"

    return 400, "Integrity error"
