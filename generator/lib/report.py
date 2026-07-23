"""The build delta report (spec §4.4).

Loud != fatal. A build that quietly succeeds while repos are missing, saying
nothing, is the failure to avoid. The report distinguishes three states so
'not yet public' is never confused with 'should be there and isn't':

  rendered   — a product page was produced
  unpublished — rendered, but its publication signals are absent (pre-public);
                expected, not a fault
  faulted    — something went wrong for this repo (bad config, etc.)

This report is a free migration/progress signal from a system built anyway.
"""


class DeltaReport:
    def __init__(self, org, shape):
        self.org = org
        self.shape = shape
        self.rendered = []      # (repo, status_kind)
        self.unpublished = []   # (repo, reason)
        self.faulted = []       # (repo, error)

    def mark_rendered(self, repo, status_kind, signals_present):
        self.rendered.append((repo, status_kind))
        if not signals_present:
            # rendered fine, but no publication signals — the pre-public case
            self.unpublished.append((repo, "no publication signals"))

    def mark_faulted(self, repo, error):
        self.faulted.append((repo, str(error)))

    @property
    def has_faults(self):
        return bool(self.faulted)

    def render(self):
        lines = [f"── CommonStage build: {self.org} ({self.shape}) ──"]
        lines.append(f"  rendered:    {len(self.rendered)}")
        for repo, kind in self.rendered:
            lines.append(f"      · {repo} [{kind}]")
        if self.unpublished:
            lines.append(f"  unpublished: {len(self.unpublished)} "
                         f"(pre-public — expected, not a fault)")
            for repo, reason in self.unpublished:
                lines.append(f"      · {repo} — {reason}")
        if self.faulted:
            lines.append(f"  FAULTED:     {len(self.faulted)}")
            for repo, err in self.faulted:
                lines.append(f"      ✗ {repo} — {err}")
        else:
            lines.append("  faulted:     0")
        return "\n".join(lines)
