"""Publication signals — fetched at build time, and OPTIONAL (spec §4.3, §4.4).

Downloads, stars, and clone counts are page CONTENT, fetched from the git host
at build time so no visitor's browser ever contacts it. But a repo may have NO
signals — it may be pre-public on the staging host, a permanent and intended
lifecycle stage, not an error. So:

  - absence is NEVER fatal, NEVER a placeholder, NEVER dressed up;
  - the concept is named for what it is ("publication signals from wherever a
    repo is published"), not for one host — GitHub is one source, not the model.

Loud != fatal: a fetch that fails is recorded in the result as 'unavailable'
with a reason, so the build's delta report can distinguish 'not yet public'
from 'should be there and isn't' — it never silently reads as zero.
"""

import json
import urllib.error
import urllib.request


class Signals:
    """The publication signals for one repo. Every field may be absent."""

    def __init__(self, stars=None, latest_release=None, downloads=None,
                 available=True, reason=""):
        self.stars = stars
        self.latest_release = latest_release
        self.downloads = downloads
        self.available = available   # False => not published yet / unreachable
        self.reason = reason         # why, when unavailable (for the delta report)

    @property
    def present(self):
        return self.available and (
            self.stars is not None
            or self.latest_release is not None
            or self.downloads is not None
        )

    def as_dict(self):
        return {
            "stars": self.stars,
            "latest_release": self.latest_release,
            "downloads": self.downloads,
            "available": self.available,
            "reason": self.reason,
        }


def _get_json(url, token=None, timeout=10):
    req = urllib.request.Request(url, headers={"User-Agent": "CommonStage"})
    if token:
        req.add_header("Authorization", f"Bearer {token}")
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return json.loads(resp.read().decode())


def fetch_github(org, repo, token=None, api="https://api.github.com"):
    """Fetch publication signals for a GitHub repo.

    A 404 (repo not yet pushed to this host) returns an 'unavailable' Signals
    with a reason — NOT an exception, NOT zeros. That is the pre-public case,
    which is expected and must not break the build.
    """
    try:
        meta = _get_json(f"{api}/repos/{org}/{repo}", token)
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return Signals(available=False, reason="not published to this host yet")
        return Signals(available=False, reason=f"host error {e.code}")
    except (urllib.error.URLError, TimeoutError) as e:
        return Signals(available=False, reason=f"unreachable: {e}")

    stars = meta.get("stargazers_count")

    latest_release = None
    downloads = None
    try:
        rel = _get_json(f"{api}/repos/{org}/{repo}/releases/latest", token)
        latest_release = rel.get("tag_name")
        downloads = sum(a.get("download_count", 0) for a in rel.get("assets", []))
    except urllib.error.HTTPError as e:
        if e.code != 404:  # 404 just means no releases — a normal, silent absence
            return Signals(stars=stars, available=True,
                           reason=f"releases unavailable ({e.code})")
    except (urllib.error.URLError, TimeoutError):
        pass  # signals are garnish; a release-fetch hiccup does not fail the build

    return Signals(stars=stars, latest_release=latest_release,
                   downloads=downloads, available=True)
