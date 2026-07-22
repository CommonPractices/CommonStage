# CommonStage

The family's shared web presentation layer: the standard, templates, styling, config schema, and
generator for the public web pages of every family Org and product.

**Status: design stage. No code yet.**

## What it is

Seven family Orgs have no public web presence. Built ad hoc, they would read as seven unrelated
projects. CommonStage makes them read as one family — a common look, a common page shape, and a
common way of declaring what a site contains.

Each org declares its own shape as data, in a site config in that org's `.github` repo:

- **`product`** — the org *is* the product. One product page; repos are platforms behind it.
- **`portfolio`** — every repo is a product. An org index, plus a product page per repo.

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
