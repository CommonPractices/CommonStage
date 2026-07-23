"""Computed-never-stored values (spec §4.1, §4.6).

Storing any of these in a config would create a second home for one fact
(CommonMind/single-source-of-truth-doctrine.md). They are derived here at build
time from facts that already have a home elsewhere.
"""

from pathlib import Path


def resolve_hostname(org_cfg, domain):
    """The §4.1.1 chain: repo/org name -> explicit hostname -> variant affix.

    The affix applies to the CHOSEN hostname, never the namespace, so
    (hostname='workshop', variant='-beta') -> 'workshop-beta', never
    'jschwefel-workshop-beta'.
    """
    base = org_cfg["hostname"] or org_cfg["org"]  # step 1 default, step 2 override
    variant = org_cfg.get("hostname_variant", "")  # step 3 affix (a value, not a bool)
    host = f"{base}{variant}"
    return host


def canonical_url(org_cfg, domain):
    """Canonical site URL from hostname + domain. Never a stored 'url' field."""
    host = resolve_hostname(org_cfg, domain)
    return f"https://{host}.{domain}"


def licence_from_repo(repo_path):
    """Read the licence from the repo's own LICENSE file — never a restated name.

    Returns a short SPDX-ish label when recognisable, else 'see LICENSE'. The
    file is the source of truth; this only labels it for display.
    """
    repo = Path(repo_path)
    for candidate in ("LICENSE", "LICENSE.txt", "LICENSE.md", "COPYING"):
        p = repo / candidate
        if p.is_file():
            head = p.read_text(errors="replace")[:400].lower()
            if "apache license" in head and "2.0" in head:
                return "Apache-2.0"
            if "mit license" in head:
                return "MIT"
            if "business source license" in head or "bsl" in head:
                return "BSL-1.1"
            if "gnu general public" in head:
                return "GPL"
            return "see LICENSE"
    return None  # no LICENSE file — absence is information, not a fabricated licence


def repo_url(org, repo_name, host_base="https://github.com"):
    """Repo URL from org + name — never a stored field that can diverge."""
    return f"{host_base}/{org}/{repo_name}"
