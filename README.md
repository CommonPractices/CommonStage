# CommonStage

The family's shared web presentation layer: the standard, templates, styling, config schema, and
generator for the public web pages of every family Org and product.

**Status: working. Two proving sites, the extracted apparatus, and a config-driven generator that
builds a family site from config alone — verified: generated output passes the full accessibility
matrix. Deployment to the server is the remaining piece.**

## What it is

Seven family Orgs have no public web presence. Built ad hoc, they would read as seven unrelated
projects. CommonStage makes them read as one family — a common look, a common page shape, and a
common way of declaring what a site contains.

Each org declares its own shape as data, in a site config in that org's `.github` repo:

- **`product`** — the org *is* the product. One product page; repos are platforms behind it.
- **`portfolio`** — every repo is a product. An org index, plus a product page per repo.

## Layout

```
apparatus/
  css/stage.css        shared page structure + the token-on-surface contract (F2)
  css/portfolio.css    portfolio-only module (cards, badges)
  templates/…          shared template partials (head, theme picker, sync)
sites/
  testingautopilot/    the `product` proving site (Zola)
  commonpractices/     the `portfolio` proving site (Zola) — org index + a page per repo
docs/_working/specs/   the design spec (working draft)
```

**`apparatus/` is the source of truth.** Each site consumes it — it is never copied per-site. The
two `sites/` are concrete proofs, built before the generator so the generator encodes what they
taught (see the spec's §8b findings).

## Generating a site from config

The generator turns an org's `site.json` + each product's `.commonstage.json` into a finished site:

```
python3 generator/build_site.py \
  --org-config path/to/site.json \
  --repos-dir  path/to/product-repos \
  --out        build/<org> \
  --foundation CommonMind/assets/foundation.css \
  [--github-token TOKEN]        # optional: publication signals
```

It validates configs (an off-enum `status.kind` is a fatal error), computes derived facts, fetches
optional publication signals, assembles a Zola site from `apparatus/`, runs `zola build`, and prints
a **delta report** distinguishing rendered / unpublished / faulted. Exit 0 = clean, 1 = faults,
2 = fatal config error. Python, stdlib-only — no dependencies beyond `zola` on PATH.

Tests: `python3 generator/tests/test_config.py && python3 generator/tests/test_endtoend.py`.

## Building a single site by hand (dev)

```
brew install zola          # or your platform's package
cd sites/<name>
zola serve                 # dev, live-reload, http://127.0.0.1:1111
zola build                 # → public/
```

## Accessibility — a hard floor, verified by measurement

Every page passes the full contrast matrix — **5 themes × colour-blind on/off = 10 cells, zero
failures** — measured with a self-testing checker, not asserted. The five themes
(`daylight · dark · warm · paper · maxcontrast`) and the colour-blind modifier are the required
baseline from `CommonMind/visual-identity.md` §1a.

The **token-on-surface contract** (`apparatus/css/stage.css`) makes this hold by construction: a page
author cannot place an arbitrary ink on an arbitrary surface. Band text uses `--band-ink`; a primary
action uses `--ink` on `--ground`; badges use `--ink` on a status fill. This is why the second site
passed on its first build.

The `@layer` accessibility floor is proven against a **hostile stylesheet** that actively tries to
break it (`sites/testingautopilot/static/hostile.css`, a test fixture, never shipped): the attack is
watched to succeed on an unprotected control, then watched to fail against the floor.

## North Stars

In order, ratified 2026-07-22. The authoritative statement is
[§1a of the design spec](docs/_working/specs/2026-07-21-commonstage-design.md); this is a pointer,
not a second copy.

1. **Honest status** — the page never overstates what exists or how ready it is.
2. **Accessibility** — every visitor can use the page, across every modality it has.
3. **Comprehension** — a visitor learns what it does and whether it's for them, fast.
4. **Obtainability** — the visitor can actually get it and run it.
5. **Family coherence** — it visibly belongs with its siblings.

For what a North Star *is*, see the North Stars Doctrine (`CommonMind/north-stars-doctrine.md`).

## Stack

**Zola** — a single Rust binary, Tera templating. Chosen 2026-07-22 because the product pages are
**app** pages (screenshots, install flows, status, download counts), which is bespoke layout rather
than docs chrome. Verified before selection: Zola copies `static/` files without modification, so
styling ships as the editable, replaceable asset the Web UI Doctrine (`CommonMind/web-ui-doctrine.md`)
requires.

## Design

[`docs/_working/specs/2026-07-21-commonstage-design.md`](docs/_working/specs/2026-07-21-commonstage-design.md)
— a **working draft**, not sealed.

Doctrine is referenced by identity (`CommonMind/<file>.md`) rather than by checkout path, per the
Repository-Portability Doctrine: a `../CommonMind/` link resolves only on a machine with that exact
layout.

## Licence

Apache-2.0.
