"""End-to-end: assemble a portfolio site from configs and assert the output.

Runs the generator with --no-build (no Zola needed) against a synthetic org +
two product repos in a tempdir, then asserts the assembled Zola content is
correct. The negative control: a repo with an off-enum status must FAULT while
the others render, and the run must exit non-zero.
"""

import json
import subprocess
import sys
import tempfile
from pathlib import Path

GEN = Path(__file__).parent.parent
FOUNDATION = GEN.parent.parent / "CommonMind" / "assets" / "foundation.css"


def _make_repo(root, name, status_kind):
    d = root / name
    d.mkdir()
    (d / ".commonstage.json").write_text(json.dumps({
        "name": name, "tagline": f"{name} tagline", "role": "ROLE",
        "status": {"kind": status_kind, "detail": f"{status_kind} detail"},
        "description": f"{name} body prose.",
    }))
    (d / "LICENSE").write_text("Apache License\nVersion 2.0")
    return d


def _run(org_cfg, repos_dir, out):
    return subprocess.run(
        [sys.executable, str(GEN / "build_site.py"),
         "--org-config", str(org_cfg), "--repos-dir", str(repos_dir),
         "--out", str(out), "--foundation", str(FOUNDATION), "--no-build"],
        capture_output=True, text=True)


def test_portfolio_assembles_all_products():
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        repos = tmp / "repos"; repos.mkdir()
        _make_repo(repos, "Alpha", "living")
        _make_repo(repos, "Beta", "draft")
        org = tmp / "site.json"
        org.write_text(json.dumps({
            "org": "TestOrg", "hostname": "testorg", "shape": "portfolio",
            "name": "TestOrg", "tagline": "t", "blurb": "b",
        }))
        out = tmp / "out"
        r = _run(org, repos, out)
        assert r.returncode == 0, r.stdout + r.stderr
        assert (out / "content" / "_index.md").is_file()
        assert (out / "content" / "alpha" / "index.md").is_file()
        assert (out / "content" / "beta" / "index.md").is_file()
        # apparatus installed
        assert (out / "static" / "foundation.css").is_file()
        assert (out / "static" / "stage.css").is_file()
        assert (out / "templates" / "product-page.html").is_file()
        # signals absent => omitted, never null (would break TOML / fabricate zero)
        alpha = (out / "content" / "alpha" / "index.md").read_text()
        assert "null" not in alpha
        print("PASS test_portfolio_assembles_all_products")


def test_product_shape_single_page():
    """A `product`-shape org: one product page AS the index, using
    product-index.html (section variables). Regression guard for the bug where
    the index section tried to use page.* and failed."""
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        repos = tmp / "repos"; repos.mkdir()
        _make_repo(repos, "SoloOrg", "shipping")  # repo shares the org name
        org = tmp / "site.json"
        org.write_text(json.dumps({
            "org": "SoloOrg", "hostname": "solo", "shape": "product",
            "name": "SoloOrg",
        }))
        out = tmp / "out"
        r = _run(org, repos, out)
        assert r.returncode == 0, r.stdout + r.stderr
        # single product = the index section, not a sub-page
        idx = out / "content" / "_index.md"
        assert idx.is_file()
        assert 'template = "product-index.html"' in idx.read_text()
        assert (out / "templates" / "product-index.html").is_file()
        print("PASS test_product_shape_single_page")


def test_bad_config_faults_but_others_render():
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        repos = tmp / "repos"; repos.mkdir()
        _make_repo(repos, "Good", "living")
        _make_repo(repos, "Bad", "notakind")  # off-enum
        org = tmp / "site.json"
        org.write_text(json.dumps({
            "org": "TestOrg", "hostname": "t", "shape": "portfolio", "name": "T",
        }))
        out = tmp / "out"
        r = _run(org, repos, out)
        # NEGATIVE CONTROL: must exit non-zero, name the fault, still render Good.
        assert r.returncode == 1, f"expected fault exit, got {r.returncode}"
        assert "Bad" in r.stdout and "notakind" in r.stdout
        assert (out / "content" / "good" / "index.md").is_file()
        assert not (out / "content" / "bad" / "index.md").is_file()
        print("PASS test_bad_config_faults_but_others_render")


if __name__ == "__main__":
    import traceback
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    passed = failed = 0
    for t in tests:
        try:
            t(); passed += 1
        except Exception:
            print(f"FAIL {t.__name__}"); traceback.print_exc(); failed += 1
    print(f"\n{passed} passed, {failed} failed")
    sys.exit(1 if failed else 0)
