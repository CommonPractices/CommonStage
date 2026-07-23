"""Assemble a Zola site from configs + the shared apparatus.

The generator does NOT render HTML itself. Zola is the stack (spec §8.2), and
the hand-built proving sites already carry the F2-disciplined, a11y-verified
templates. So the generator's job is to ASSEMBLE a Zola site directory —
apparatus CSS into static/, shared partials + page templates into templates/,
and one content file per product carrying that product's data — then let Zola
build it. This keeps the proven templates as the single rendering layer.
"""

import json
import shutil
from pathlib import Path


def _write(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text)


def _toml_escape(s):
    """Minimal TOML string escaping for front-matter values."""
    return s.replace("\\", "\\\\").replace('"', '\\"').replace("\n", " ")


def scaffold(site_dir, org_cfg, canonical):
    """Create the Zola skeleton: zola.toml (with org facts in [extra]), static/,
    templates/. The org's identity facts go in config.extra so the shared
    templates can read them (org_name, tagline, blurb, status) without any
    per-org template — one template set, driven by config."""
    site = Path(site_dir)
    if site.exists():
        shutil.rmtree(site)
    (site / "content").mkdir(parents=True)
    (site / "static").mkdir(parents=True)
    (site / "templates").mkdir(parents=True)

    status = org_cfg.get("status") or {}
    extra = {
        "org_name": org_cfg["name"],
        "tagline": org_cfg["tagline"],
        "blurb": org_cfg["blurb"],
        "status_kind": status.get("kind", ""),
        "status_detail": status.get("detail", ""),
    }
    lines = [f'base_url = "{canonical}"', "compile_sass = false",
             "build_search_index = false", "", "[extra]"]
    for k, v in extra.items():
        lines.append(f'{k} = "{_toml_escape(str(v))}"')
    _write(site / "zola.toml", "\n".join(lines) + "\n")
    return site


def install_apparatus(site, apparatus_dir, foundation_css, shape):
    """Copy shared CSS + template partials into the site.

    stage.css is always installed; portfolio.css is appended only for a
    portfolio site (it carries the card/badge module).
    """
    apparatus = Path(apparatus_dir)
    static = site / "static"

    shutil.copy(foundation_css, static / "foundation.css")

    stage = (apparatus / "css" / "stage.css").read_text()
    if shape == "portfolio":
        stage += "\n" + (apparatus / "css" / "portfolio.css").read_text()
    _write(static / "stage.css", stage)

    # Every apparatus template — partials AND page templates. The apparatus is
    # the single source; the generator installs it, never copies by hand.
    tmpl_dir = apparatus / "templates"
    for src in tmpl_dir.glob("*.html"):
        shutil.copy(src, site / "templates" / src.name)


def _product_frontmatter(product, derived, template):
    """Shared front-matter for a product page (portfolio member or standalone).

    Absence is rendered as absence: a None signal simply does not appear; no
    placeholder, no fabricated number.
    """
    # Scalar extras first (TOML requires scalars before any sub-table).
    scalars = {
        "role": product["role"],
        "tagline": product["tagline"],
        "status": product["status"]["detail"] or product["status"]["kind"],
        "status_kind": product["status"]["kind"],
        "repo": derived["repo_url"],
        "licence": derived.get("licence") or "",
    }
    lines = ["+++",
             f'title = "{_toml_escape(product["name"])}"',
             f'template = "{template}"']
    if template == "product-page.html" and "weight" in derived:
        lines.append(f'weight = {derived["weight"]}')
    lines.append("[extra]")
    for k, v in scalars.items():
        lines.append(f'{k} = "{_toml_escape(str(v))}"')

    # Signals as a TOML sub-table. Absence is rendered as absence: a None value
    # is OMITTED (not written as null, which TOML rejects and which would also
    # be a fabricated zero). An absent field simply is not there.
    sig = derived.get("signals", {}) or {}
    lines.append("[extra.signals]")
    lines.append(f'available = {"true" if sig.get("available") else "false"}')
    if sig.get("stars") is not None:
        lines.append(f'stars = {int(sig["stars"])}')
    if sig.get("latest_release"):
        lines.append(f'latest_release = "{_toml_escape(str(sig["latest_release"]))}"')
    if sig.get("downloads") is not None:
        lines.append(f'downloads = {int(sig["downloads"])}')

    lines.append("+++")
    lines.append("")
    lines.append(product["description"])
    return "\n".join(lines) + "\n"


def write_portfolio_index(site, products_meta):
    """The section _index.md that portfolio-index.html renders. Its .pages are
    the product pages written by write_portfolio_product."""
    _write(site / "content" / "_index.md",
           '+++\ntemplate = "portfolio-index.html"\nsort_by = "weight"\n+++\n')


def write_portfolio_product(site, slug, product, derived, weight):
    """A product page inside the portfolio section. weight controls card order
    (respects the org config's `order`)."""
    derived = dict(derived, weight=weight)
    fm = _product_frontmatter(product, derived, "product-page.html")
    _write(site / "content" / slug / "index.md", fm)


def write_single_product(site, product, derived):
    """A `product`-shape org: one product page AS the site index."""
    fm = _product_frontmatter(product, derived, "product-page.html")
    _write(site / "content" / "_index.md", fm)
