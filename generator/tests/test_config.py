"""Tests for config loading + the honest-status enum contract.

Run: python3 -m pytest generator/tests/ -v   (or plain: python3 tests/test_config.py)

The negative controls matter most: an off-enum status.kind and a JSONC file
must be REJECTED. A validator that accepts them certifies a bug.
"""

import json
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from lib import config, derive


def _tmp(content):
    f = tempfile.NamedTemporaryFile("w", suffix=".json", delete=False)
    f.write(content)
    f.close()
    return f.name


# ── Honest-status enum: the load-bearing contract ──────────────────────────

def test_valid_status_kind_accepted():
    p = _tmp(json.dumps({"name": "X", "status": {"kind": "living", "detail": "d"}}))
    out = config.load_product_config(p)
    assert out["status"]["kind"] == "living"
    assert out["status"]["detail"] == "d"


def test_offenum_status_kind_REJECTED():
    # NEGATIVE CONTROL: 'awesome' is not a defined maturity — must raise.
    p = _tmp(json.dumps({"name": "X", "status": {"kind": "awesome"}}))
    try:
        config.load_product_config(p)
    except config.ConfigError as e:
        assert "awesome" in str(e) and "not a defined maturity" in str(e)
        return
    raise AssertionError("off-enum status.kind was ACCEPTED — a page could claim "
                         "a maturity the family never defined")


def test_missing_required_field_rejected():
    p = _tmp(json.dumps({"status": {"kind": "living"}}))  # no name
    try:
        config.load_product_config(p)
    except config.ConfigError as e:
        assert "name" in str(e)
        return
    raise AssertionError("missing required 'name' was accepted")


def test_jsonc_rejected():
    # NEGATIVE CONTROL: strict JSON only. A // comment must fail loudly.
    p = _tmp('{\n  // a comment\n  "name": "X", "status": {"kind": "wip"}\n}')
    try:
        config.load_product_config(p)
    except config.ConfigError as e:
        assert "strict JSON" in str(e)
        return
    raise AssertionError("JSONC (with a comment) was accepted — Data Format "
                         "Doctrine violated")


def test_invalid_shape_rejected():
    p = _tmp(json.dumps({"org": "O", "hostname": "h", "shape": "nonsense"}))
    try:
        config.load_org_config(p)
    except config.ConfigError as e:
        assert "nonsense" in str(e)
        return
    raise AssertionError("invalid shape accepted")


# ── Hostname resolution (§4.1.1) ───────────────────────────────────────────

def test_hostname_variant_applies_to_chosen_not_namespace():
    # The §4.1.1 rule: affix on the CHOSEN hostname, never the namespace.
    cfg = {"org": "jschwefel-workshop", "hostname": "workshop",
           "hostname_variant": "-beta"}
    assert derive.resolve_hostname(cfg, "schwefel.net") == "workshop-beta"


def test_hostname_defaults_to_org_when_unset():
    cfg = {"org": "myorg", "hostname": "", "hostname_variant": ""}
    assert derive.resolve_hostname(cfg, "schwefel.net") == "myorg"


def test_canonical_url():
    cfg = {"org": "o", "hostname": "commonpractices", "hostname_variant": ""}
    assert derive.canonical_url(cfg, "schwefel.net") == \
        "https://commonpractices.schwefel.net"


if __name__ == "__main__":
    import traceback
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    passed = failed = 0
    for t in tests:
        try:
            t()
            print(f"PASS {t.__name__}")
            passed += 1
        except Exception:
            print(f"FAIL {t.__name__}")
            traceback.print_exc()
            failed += 1
    print(f"\n{passed} passed, {failed} failed")
    sys.exit(1 if failed else 0)
