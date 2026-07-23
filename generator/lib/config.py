"""Config loading + validation.

Reads the two strict-JSON config files the schema defines (spec §4.6):
  - the org's  site.json          (identity + shape)
  - each repo's .commonstage.json (that product's own facts)

Validation is where Honest status (North Star #1) becomes enforceable rather
than decorative: status.kind must be one of a defined set, so a page can never
claim a maturity the family has not defined. An off-enum value is a config
error, never a silent pass.

Strict JSON only (CommonMind/data-format-doctrine.md): json.load rejects
comments and trailing commas by construction, so a JSONC/JSON5 file fails here
loudly — which is the doctrine's intent, not a bug to work around.
"""

import json
from pathlib import Path


# The status enum (spec §4.6). Open to extension — add a kind when a real
# product needs one — but a value OUTSIDE it is an error, not a silent pass.
STATUS_KINDS = {
    "shipping",  # released, has versioned artifacts to download
    "active",    # usable + maintained, no formal release cadence
    "living",    # mutable-by-design; evolves continuously, not versioned
    "beta",      # works, not yet stable
    "draft",     # exists, pre-1.0, incomplete
    "wip",       # design/build stage; not yet usable
}

SHAPES = {"product", "portfolio"}


class ConfigError(Exception):
    """A config is malformed or claims something the schema forbids.

    Loud and fatal with a map: names the file, the field, and the fix — the
    LiteController 'unavailable, here is how to fix it' lesson applied to config.
    """


def _require(data, field, where):
    if field not in data:
        raise ConfigError(f"{where}: missing required field '{field}'")
    return data[field]


def _load_strict_json(path):
    p = Path(path)
    if not p.is_file():
        raise ConfigError(f"config not found: {p}")
    try:
        return json.loads(p.read_text())
    except json.JSONDecodeError as e:
        raise ConfigError(
            f"{p}: not valid strict JSON (RFC 8259 — no comments, no trailing "
            f"commas): {e}"
        )


def _validate_status(status, where):
    """A status is {kind, detail}; kind must be in the enum. This is the
    honest-status contract made checkable."""
    if not isinstance(status, dict):
        raise ConfigError(f"{where}: 'status' must be an object {{kind, detail}}")
    kind = status.get("kind")
    if kind not in STATUS_KINDS:
        allowed = ", ".join(sorted(STATUS_KINDS))
        raise ConfigError(
            f"{where}: status.kind '{kind}' is not a defined maturity. "
            f"Allowed: {allowed}. (A page may not claim a maturity the family "
            f"has not defined — spec §4.6.)"
        )
    # detail is free text and optional; kind is the load-bearing part.
    return {"kind": kind, "detail": status.get("detail", "")}


def load_org_config(path):
    """Load and validate an org's site.json. Returns a normalized dict."""
    data = _load_strict_json(path)
    where = str(path)

    org = _require(data, "org", where)
    hostname = _require(data, "hostname", where)
    shape = _require(data, "shape", where)
    if shape not in SHAPES:
        raise ConfigError(
            f"{where}: shape '{shape}' invalid; must be one of {sorted(SHAPES)}"
        )

    status = data.get("status")
    if status is not None:
        status = _validate_status(status, f"{where} (org status)")

    opt = data.get("_optional", {})
    return {
        "org": org,
        "hostname": hostname,
        "shape": shape,
        "name": data.get("name", org),
        "tagline": data.get("tagline", ""),
        "blurb": data.get("blurb", ""),
        "status": status,
        "hostname_variant": opt.get("hostname_variant", ""),
        "branch": opt.get("branch", ""),
        "exclude": opt.get("exclude", []),
        "order": opt.get("order", []),
        "featured": opt.get("featured", []),
    }


def load_product_config(path):
    """Load and validate a repo's .commonstage.json. Returns a normalized dict."""
    data = _load_strict_json(path)
    where = str(path)

    name = _require(data, "name", where)
    status = _validate_status(_require(data, "status", where), where)

    opt = data.get("_optional", {})
    return {
        "name": name,
        "tagline": data.get("tagline", ""),
        "role": data.get("role", ""),
        "status": status,
        "description": data.get("description", ""),
        "screenshots": opt.get("screenshots", []),
        "install": opt.get("install"),
        "featured_signals": opt.get("featured_signals", []),
    }
