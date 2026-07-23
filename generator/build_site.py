#!/usr/bin/env python3
"""CommonStage generator — build a family site from configs + the apparatus.

One task, one entry point (family scripting doctrine): a thin orchestrator over
generator/lib/. It reads an org's site.json and each product's
.commonstage.json, computes the derived facts, fetches optional publication
signals, assembles a Zola site from the shared apparatus, runs `zola build`,
and prints the delta report.

Usage:
    build_site.py --org-config PATH --repos-dir DIR --out DIR [options]

    --org-config   path to the org's site.json
    --repos-dir    dir holding product repos (each may carry .commonstage.json)
    --out          where to assemble the Zola site
    --apparatus    apparatus/ dir (default: ../apparatus relative to this file)
    --foundation   path to foundation.css
    --domain       site domain (default: schwefel.net)
    --github-token optional token for publication signals
    --no-build     assemble only; skip `zola build` (for tests)

Exit codes: 0 = built, no faults · 1 = faults in the delta report · 2 = fatal
config error (loud, with a map).
"""

import argparse
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from lib import config, derive, signals as sig, assemble
from lib.report import DeltaReport


def _slug(name):
    return name.lower().replace(" ", "-")


def _discover_products(repos_dir, org_cfg):
    """Every repo dir with a .commonstage.json is a product, minus `exclude`.
    Absence of the file means the repo is not a product page — silent, expected."""
    repos = Path(repos_dir)
    exclude = set(org_cfg.get("exclude", []))
    found = []
    for child in sorted(repos.iterdir()):
        if not child.is_dir() or child.name in exclude:
            continue
        cfg = child / ".commonstage.json"
        if cfg.is_file():
            found.append((child.name, child, cfg))
    # honour explicit order, then the rest alphabetically
    order = org_cfg.get("order", [])
    found.sort(key=lambda t: (order.index(t[0]) if t[0] in order else len(order), t[0]))
    return found


def _derive_for(repo_name, repo_path, org_cfg, args):
    d = {"repo_url": derive.repo_url(org_cfg["org"], repo_name),
         "licence": derive.licence_from_repo(repo_path)}
    s = sig.fetch_github(org_cfg["org"], repo_name, token=args.github_token)
    d["signals"] = s.as_dict()
    d["_signals_obj"] = s
    return d


def build(args):
    org_cfg = config.load_org_config(args.org_config)
    canonical = derive.canonical_url(org_cfg, args.domain)
    report = DeltaReport(org_cfg["org"], org_cfg["shape"])

    apparatus = args.apparatus or str(Path(__file__).parent.parent / "apparatus")
    site = assemble.scaffold(args.out, org_cfg, canonical)
    assemble.install_apparatus(site, apparatus, args.foundation, org_cfg["shape"])

    if org_cfg["shape"] == "product":
        # The org IS the product: one product page as the index.
        # By convention the product repo shares the org name.
        repo_path = Path(args.repos_dir) / org_cfg["org"]
        cfg_path = repo_path / ".commonstage.json"
        try:
            product = config.load_product_config(cfg_path)
            derived = _derive_for(org_cfg["org"], repo_path, org_cfg, args)
            assemble.write_single_product(site, product, derived)
            report.mark_rendered(org_cfg["org"], product["status"]["kind"],
                                 derived["_signals_obj"].present)
        except config.ConfigError as e:
            report.mark_faulted(org_cfg["org"], e)

    else:  # portfolio
        assemble.write_portfolio_index(site, [])
        products = _discover_products(args.repos_dir, org_cfg)
        for weight, (name, path, cfg_path) in enumerate(products):
            try:
                product = config.load_product_config(cfg_path)
                derived = _derive_for(name, path, org_cfg, args)
                assemble.write_portfolio_product(site, _slug(product["name"]),
                                                 product, derived, weight)
                report.mark_rendered(name, product["status"]["kind"],
                                     derived["_signals_obj"].present)
            except config.ConfigError as e:
                report.mark_faulted(name, e)

    if not args.no_build:
        result = subprocess.run(["zola", "build"], cwd=site,
                                capture_output=True, text=True)
        if result.returncode != 0:
            print(result.stdout)
            print(result.stderr, file=sys.stderr)
            report.mark_faulted("(zola build)", "zola build failed")

    print(report.render())
    return 1 if report.has_faults else 0


def main(argv=None):
    p = argparse.ArgumentParser(description="Build a CommonStage family site.")
    p.add_argument("--org-config", required=True)
    p.add_argument("--repos-dir", required=True)
    p.add_argument("--out", required=True)
    p.add_argument("--apparatus")
    p.add_argument("--foundation", required=True)
    p.add_argument("--domain", default="schwefel.net")
    p.add_argument("--github-token")
    p.add_argument("--no-build", action="store_true")
    args = p.parse_args(argv)

    try:
        return build(args)
    except config.ConfigError as e:
        print(f"FATAL config error: {e}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
