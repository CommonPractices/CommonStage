# CommonStage — Design

**Status:** DRAFT — working document, not approved.
**Date:** 2026-07-21
**Owner:** jschwefel

The shared web presentation layer: the standard, templates, styling, config schema, and
eventually a generator for the public web pages of every Org and product.

---

## 1. Purpose

Seven Orgs have no public web presence. Built ad hoc, they would read as seven unrelated
projects. CommonStage makes them read as one set — a common look, a common page shape, and a
common way of declaring what a site contains.

**In scope:** every Org.

Current orgs in scope, with what each actually holds on GitHub (verified 2026-07-21 via
`gh api orgs/<org>/repos`):

| Org | Product repos today | Note |
|---|---|---|
| TestingAutoPilot | `autopilot-core`, `-macos`, `-ios`, `-android`, `-web`, `homebrew-autopilot` | The `product` proving site |
| CommonPractices | CommonMind, CommonFraming, CommonTongue | The `portfolio` proving site |
| SurfaceWorks | Lucidity, Palette, Codex | |
| ObservationPost | Oscura | Single-product `portfolio` |
| jschwefel-workshop | `esp-idf-ds3231`, `medit`, `kiln` | **First-class** — where projects the owner *wants in the public eye* are put (§8.7) |
| **StudioEnsemble** | **none — `.github` only** | CameraConductor + LiteController exist **locally, unpushed** |
| **DeckLibre** | **none — `.github` only** | |

⚠️ **Two of seven orgs would render an empty index today.** This is why §8.3 (what an empty or
single-repo `portfolio` org does) is a present-state question, not a hypothetical edge case. A
product repo appearing on either org changes that org's site with no config edit — which is the
flag's intended behaviour, but means those two sites are **not buildable as proof of anything yet**.

**Licence:** Apache-2.0. Per Licensing Doctrine (`CommonMind/licensing-doctrine.md`), Q1's
client-vs-service tie-breaker: a static-site generator an operator runs against their own repos is a
**client/local tool**, not a managed service others send data to — the same reading that puts Oscura
at Apache rather than BSL.

---

## 1a. North Stars

**Ratified by the owner, 2026-07-22. Corrected 2026-08-03** — the set as ratified was missing a
Doctrine-tier axiom; see §1a.4. This is CommonStage's **authoritative** statement of its own
ordered values; other mentions in this spec point here rather than re-listing them.

For what a North Star *is* — an axiom, not a conclusion; alignment near-non-negotiable while the
*means* of alignment stays negotiable — see the [North Stars
Doctrine](../../../../CommonMind/doctrines/north-stars-doctrine.md). That framework is **cited, not
re-derived** here.

**The four Doctrine-tier axioms bind this project** ([North Stars
§1.2](../../../../CommonMind/doctrines/north-stars-doctrine.md)): *a North Star cannot be refused;
no tier declines a star. What varies is a star's rank and its reach — never whether it binds.*
CommonStage states its **ranking** and its **reach**, and adds stars of its own on top — which
§2.3 expressly permits: **the four are a floor, not a ceiling.**

**These are the values of the visitor**, not of the build. CommonStage's job is the public face of
the **apps** — the product page is where someone decides whether to download DeckLibre or
AutoPilot. A technically-correct site nobody wants to use would satisfy a pipeline-shaped set
completely; that is the failure this ordering exists to prevent.

### 1a.1 The set

**Axioms, ranked and reached for this project.** Inherited, never declined.

| # | Star | Rank + reach here |
|---|---|---|
| 1 | **Honest** | The page never overstates what exists or how ready it is — **and the same prohibition binds the work**: a status, a "done", a claim about what was rendered or verified is itself a claim about a condition ([North Stars §2](../../../../CommonMind/doctrines/north-stars-doctrine.md)). Ranked first because a site's only real currency is that its claims hold. |
| 2 | **Accessibility** | Every visitor can use the page, across every modality it has. **A ranked star, not a floor** (§1.4's first form): a product page carrying screenshots, install flows and status indicators is a materially richer surface than doctrine-rendering, and accessibility genuinely decides outcomes there. |
| 3 | **Usability** | The default path is walkable: a visitor who has read nothing completes the primary flow — *understand what this is*, then *get it*. **§1a.2 splits this into the two stars that actually bite here** — Comprehension and Obtainability — which are Usability at this product's altitude, not replacements for it. |
| 4 | **Choice** | **Reach: narrow, and stated rather than assumed.** A visitor does not configure a web page, so the axiom has little surface to bind — but it is not moot. It binds where the site *does* offer alternatives: the **theme picker**, which honours the OS preference and lets the visitor override it; and download/install alternatives, where a page offers **every** route that exists rather than the one route the template found convenient. Per [§2.4](../../../../CommonMind/doctrines/north-stars-doctrine.md), any such alternative is **disclosed by a reveal, never a feature toggle**. |

**Project stars, added on top** ([§2.3](../../../../CommonMind/doctrines/north-stars-doctrine.md) —
a project may introduce stars of its own):

| # | Star | Gloss |
|---|---|---|
| 5 | **Comprehension** | A visitor learns what it does and whether it is for them, fast. |
| 6 | **Obtainability** | The visitor can actually get it and run it. |
| 7 | **Set coherence** | It visibly belongs with its siblings — one look across every Org and product page. |

### 1a.2 Why Comprehension and Obtainability are named separately

**Usability is the axiom; these two are what it decomposes into on a product page**, and they are
ranked separately because **they conflict with each other and with the axioms in different
directions** (§1a.3). Naming only "Usability" would hide those conflicts behind one word and leave
the ordering unable to resolve them.

They do **not** replace Usability, and the axiom is not discharged by them: a page that is
comprehensible and obtainable but hostile to walk through still fails #3.

### 1a.3 Where the ordering bites

An ordering earns its keep only where it resolves a real conflict:

- **Honest ▸ Comprehension.** A page is more compelling if you omit that something is alpha.
  Honesty wins — **even when it costs the download.**
- **Accessibility ▸ Comprehension, Set coherence.** If the shared look ever fails a contrast or
  focus requirement, **the look changes.** This is the one that will actually hurt someday; ranking
  it #2 is what makes it real.
- **Comprehension ▸ Set coherence.** If the shared template genuinely obscures what an app does,
  **the template bends.** Coherence is the founding requirement, not a straitjacket.
- **Obtainability ▸ Set coherence.** Install instructions that do not fit the template win; the
  template adapts.
- **Accessibility ▸ Choice.** Where the site offers an alternative, it is a **reveal**, never a
  toggle that makes capability conditionally absent
  ([§2.4](../../../../CommonMind/doctrines/north-stars-doctrine.md)).

### 1a.4 Correction of record — the ratified set was missing an axiom

**The set ratified 2026-07-22 listed five stars: Honest status · Accessibility · Comprehension ·
Obtainability · Family coherence. It contained no Choice, and no Usability.** Under [North Stars
§1.2](../../../../CommonMind/doctrines/north-stars-doctrine.md) that set was not a legal ranking —
an axiom cannot be declined, only re-ranked and re-reached.

**How it happened, because the mechanism matters more than the omission.** The section did not
forget Choice; it believed it had been *authorised* to drop it. §1a.3 as ratified read:

> *"**Not a doctrine-named set by reference.** §2.1 permits naming a set by reference as an
> explicit ratified choice; it was available and deliberately not taken — two of these five stars
> have no counterpart in it."*

**[§2.1](../../../../CommonMind/doctrines/north-stars-doctrine.md) says no such thing.** It is
titled *"Why the base set is ordered"*, and its content is that a project which has **not** stated
its own ranking **inherits** the doctrine's. There is no naming-by-reference permission there, and
nothing in it makes an axiom optional.

**One misread citation authorised the omission, and everything built on top of it was internally
consistent** — which is why a careful, well-reasoned section stayed non-conformant through a
ratification. The commit that retired `family` (`25b1443`) caught the symptom and recorded it as
owner-needed; this is the correction.

**What changed in this rewrite:**

| Was | Now | Why |
|---|---|---|
| "Honest status" | **Honest** (#1), reach widened | The axiom binds the builders, not only the build; "status" scoped away half of it |
| — | **Usability** (#3) | Inherited; §1a.2 states how Comprehension and Obtainability decompose it |
| — | **Choice** (#4), reach stated | Inherited. Narrow surface, but §1.2 forbids declining it — and it does bind the theme picker and install alternatives |
| Comprehension, Obtainability | Unchanged, renumbered as **project stars** | Legitimate additions under §2.3 |
| "Family coherence" | **Set coherence** | `family` is retired ([Terminology-Migration §5c](../../../../CommonMind/doctrines/terminology-migration-doctrine.md)); the star itself is untouched |
| §1a.3's naming-by-reference bullet | **Removed** | It cited a rule that does not exist |

### 1a.5 Deliberately excluded

- **Ease of authoring** and **Independence of content repos** — both real, both still true, both
  **means rather than values**
  ([§1.1](../../../../CommonMind/doctrines/north-stars-doctrine.md)). They serve the visitor by
  making a coherent site cheap enough to maintain. They remain design rationale in §4.1 and §4.5;
  freezing a means into a mandate is the scope-widening failure.
- **Speed** — present in the presentation-layer set, excluded here: build speed does not
  discriminate at this scale (§8.2, ~37 files vs. a ~500-page threshold), so it would be a slogan.

> **Provenance.** An earlier draft derived stars from the *build pipeline* (Truthfulness · Ease of
> authoring · Independence · Choice) and read as documentation values. The owner rejected it:
> *"They are great for documentation an all, but most of the repos are (will be) apps."* The
> ordering shape survived; the subjects did not. The error was **scope, not detail** — values
> derived from the machinery in front of us rather than from what the product is for. **Choice was
> in that draft and did not survive the rewrite** (§1a.4).

---

## 2. The shape flag

Each org declares its own shape as data, in a site config file in that org's `.github` repo.

| Flag | Means | Renders |
|---|---|---|
| `product` | **The org IS the product** | One product page. Repos are platforms/components behind the single product and are never enumerated as products. |
| `portfolio` | **Every repo IS a product** | An org index page, plus one product page per repo. |

The **same product-page template** serves both. `portfolio` adds an index above the product pages;
`product` is the case where the org itself is the single product.

**Why a declared flag and not an inferred one.** Repo count does not determine shape:
TestingAutoPilot has six repos and is one product; CommonPractices has four and is four products.
Only the org knows which it is, so the org states it. This is **data out of code** (Scripting
Philosophy: business data lives in an input file the code reads at runtime, never in the code) — the
generator branches on a declared fact, never on a heuristic it guessed.

**What the flag deliberately does NOT require.** No per-repo role taxonomy, no
release-implies-product heuristic, no maintained list of products. A `portfolio` org that gains a
repo gains a product page with no config edit — there is no currency obligation to forget. The
`.github` repo itself is excluded by a fixed rule in the generator, not by configuration.

### Worked pair

- **TestingAutoPilot** = `product`. One product (AutoPilot) across `autopilot-core`,
  `autopilot-macos`, `autopilot-ios`, `autopilot-android`, `autopilot-web`, plus
  `homebrew-autopilot`. Those five platform repos are implementation detail — surfacing them as five
  products would misrepresent the product entirely.
- **CommonPractices** = `portfolio`. Distinct products: CommonMind, CommonFraming, CommonTongue —
  and CommonStage itself once it exists.

These are two genuinely different kinds of multiplicity — *one product, many repos* versus *many
products, one org*. Conflating them is the failure this flag exists to prevent.

**CommonPractices as the `portfolio` half is deliberate, not incidental.** It carries by far the
the heaviest documentation (CommonMind alone is 37 files / ~7,250 lines with dense
inter-doctrine cross-linking), so it proves the expensive half of the apparatus — docs rendering —
in phase one rather than deferring it. It also makes CommonStage **self-hosting**: the apparatus
renders the org that contains it, so a docs-rendering regression is visible on the doctrine site the
set reads most.

Other orgs (SurfaceWorks, DeckLibre, StudioEnsemble, ObservationPost, jschwefel-workshop) are
in scope for the standard but are **not** proving sites; they adopt the shape once it is extracted.

---

## 3. Page kinds

1. **Org index** — `portfolio` orgs only. Org identity band, product cards, org-level prose.
2. **Product page** — what it does, screenshots, install, downloads, docs link, status, repo link.
3. **Docs pages** — rendered markdown with navigation, anchors, and search.

---

## 4. Configuration

A **full site config** file in each org's `.github` repo. It lives there because that is where
org-level facts already live (the profile README and the community health set), per
Org & Repo Bootstrap Doctrine (`CommonMind/org-and-repo-bootstrap-doctrine.md`).

Data out of code: the generator holds logic only. Changing what a site shows means editing the
config, never the code.

**Format: strict JSON** (RFC 8259), per
Data Format Doctrine (`CommonMind/data-format-doctrine.md`) — this is a format the projects themselves
defines, so the doctrine applies and JSONC/JSON5 are banned. Annotation goes in **data** (`_note`
fields), never comments.

### 4.1 The three tiers

Ease of use (few fields) and choice (many knobs) pull in opposite directions. **They are not traded
off against each other** — per North Stars Doctrine §5 (`CommonMind/north-stars-doctrine.md`), a
ranking says which star you may not lose, *not* which to sacrifice: *"don't trade; find the
construction that satisfies both."*

The three-tier shape **is** that construction, and it is the same one the doctrine cites as the
model (CameraConductor's accessibility-vs-choice clash, resolved with a floor — total freedom above
guarantees that cannot be overridden):

- **A tiny required set** (3 fields) — ease of use fully served; a minimum viable config is three
  lines.
- **Unlimited optional knobs above it**, each with a working default — choice fully served; nothing
  a reasonable org might want to vary is hardcoded.
- **An inviolable floor beneath** (§4.2) — no config may lower the accessibility floor, whatever
  else it sets.

Neither star is sacrificed. Add: **nothing display-facing is derived from a namespace** (§4.1's
`hostname` rule).

> ✅ **Resolved 2026-07-22 — CommonStage's own North Star set is ratified (§1a).** This paragraph
> previously carried a warning: the tiering had been justified by invoking the
> presentation-layer ordering without CommonStage having stated a set of its own — the silent
> inheritance §2.1 (`CommonMind/north-stars-doctrine.md`) forbids.
>
> **The warning is void, but note what the ratified set does *not* say.** Ease of authoring is
> **deliberately not a star** (§1a.3) — it is a *means*. So the satisfy-both construction below
> stands on its own engineering merits, and on serving the visitor by keeping a coherent site
> maintainable; it is **not** justified by a ranking of ease against choice. That justification was
> wrong twice over and is not reinstated here.

**Required — 3 fields.** A minimum viable config is three lines.

| Field | Example | Why |
|---|---|---|
| `org` | `jschwefel-workshop` | The source-host namespace. **Never rendered.** |
| `hostname` | `workshop` | Yields `workshop.schwefel.net`. |
| `shape` | `portfolio` | §2's flag. |

⭐ **`hostname` is NOT derived from `org`, and this is the ordinary case, not an edge case.** The org
name is a namespace on the git host; the hostname is a presentation choice. `jschwefel-workshop`
becomes `workshop.schwefel.net` — deriving it would produce `jschwefel-workshop.schwefel.net`, which
no one would choose. The same divergence applies to the display name. **Every identifier that can
diverge is its own field.**

#### 4.1.1 The hostname resolution chain

`hostname` resolves in three ordered steps. Each is overridable; none is a second copy of a fact
held elsewhere.

| Step | Source | Result for the worked case |
|---|---|---|
| 1. Default | the repo/org name | `jschwefel-workshop` |
| 2. Explicit `hostname` | authored, when the default is wrong — **the ordinary case** | `workshop` |
| 3. Variant affix | authored, defaults to none | `workshop-beta` |

⭐ **The affix applies to the *chosen* hostname (step 2), never to the namespace (step 1).** Setting
both yields `workshop-beta`, never `jschwefel-workshop-beta`. This falls out of applying the variant
at step 3 rather than folding it into the default.

**The affix is a value, not a boolean.** A `true`/`false` flag would hardcode `-beta` into the
generator; the first time a site wants `-staging` or `-preview`, the schema fights the author. A
field holding the affix itself — absent meaning none — costs the same to author and needs no
repaint. It also defers the choice of *what the affix should say* out of the tool entirely.

**The affix is independent of publication status.** It is deliberately not coupled to whether a repo
has reached the public host (§4.4). Coupling them would silently change a site's URL at the moment
the repo is first pushed — a broken-link event firing exactly when a project starts drawing
attention. The affix is turned on and off deliberately. The automatic coupling remains addable
later; the reverse would not be.

#### 4.1.2 The publish branch

**`branch` — configurable, defaulting to the repo's own default branch.** Absent, a repo renders
from `main`/`master` as today; nothing changes for repos that do not care.

This reads a maturity signal that **already exists in git** rather than inventing one — the same
infer-don't-declare position §4.4 takes on publication status. A repo with unreviewed commits
landing on `main` and reviewed content on a release branch can publish the latter without the
generator learning a new concept.

**Branch and variant are a pair, not two independent fields.** Set a pre-release `branch` *without*
a variant affix and unreviewed content publishes silently to the production hostname. That is a
plausible authoring mistake, not an exotic one, so the config expresses *"this branch publishes to
this hostname"* as a unit rather than as two fields that must happen to agree.

**A configured branch that does not exist is reported, never silently substituted.** Falling back to
the default branch without saying so renders `main` while the author believes they are seeing
`develop` — the §4.4 rule applied to branches: absence is information.

**Deliberately not built: multi-branch publishing.** One repo rendering *both* a stable and a beta
site simultaneously is the obvious next thought and a large jump — two outputs, two hostnames, a
doubled build, and a generator that must understand multiplicity. **One branch, one site, one
hostname.** Publishing both is expressible as two config entries; multiplicity falls out of
repetition rather than a feature.

**Authored — nothing else holds these facts.** `name` (display), `full_name`, `tagline`, `blurb`,
`status` (per User-Documentation Doctrine's honest-status rule), `links`, `exclude` (repos not to
surface — `portfolio` renders everything by default, so this is the escape hatch), `order`,
`featured`, `og_image`, `docs.*` (source, include/exclude globs, nav order, landing file),
`theme_default`.

Note that **no org currently sets a GitHub org description**, so taglines and blurbs cannot fall
back to GitHub metadata — they must be authored.

**Computed — never stored.** Storing these creates a second home for one fact
(Single-Source-of-Truth (`CommonMind/single-source-of-truth-doctrine.md`)):

| Value | Resolved from | Never |
|---|---|---|
| Canonical URL | `hostname` + domain | a stored `url` field that can diverge |
| Org colour + mark | the Identity-Mark asset in `.github/profile/` | a restated hex value |
| Licence | the repo's own `LICENSE` | a restated licence name |
| Repo list | the GitHub API | a hand-maintained product list |

### 4.2 Two hard exclusions

- **No analytics field of any kind.** Sites are hosted on a server the owner fully controls (§8.4);
  server-side analytics land there and are the owner's to surface. CommonStage introduces no
  third-party beacon and no client-side collector.
- **No field may lower the accessibility floor.** There is deliberately no way for a config to
  disable the contrast audit or override the `@layer` floor that
  `CommonMind/assets/foundation.css` establishes. Accessibility is the
  presentation layer's first North Star; a knob that can switch it off would make it advisory.

### 4.3 Publication signals are content — and they are optional

Download counts, clone/view traffic, and stars are **wanted on the page** — they are content, not
visitor measurement. Distinct from §4.2's exclusion, which concerns observing site visitors.

**Fetched at build time. Resolved.** This was previously left open between build-time and
client-side fetching; the CI build model (§4.4) settles it. The builder already holds host
credentials, the numbers land in static HTML, and **no visitor's browser ever contacts the git
host** — which client-side fetching would have required, contacting a third party from the reader's
browser against §4.2's spirit, and putting every reader against an API rate limit.

⭐ **Name the concept for what it is, not for today's host.** A `github` config block, a
`github_stars` field, or a `not_on_github` state would hardcode one host into the schema and make
any other primary awkward permanently. These are **publication signals from wherever a repo is
published** — one possible source among others. Identical behaviour today; no repaint later.

### 4.4 A repo may have no publication signals, and that is not an error

**A repo's presence on the public host is not a fact about the repo. It is a fact about its stage.**

A repo is worked and tested on the staging git host and reaches the public host only when it is
worth pushing — the *don't push until you have something worthy* rule, given somewhere to
actually live. **This is a permanent, recurring, intended lifecycle stage, not a transitional one.**

Consequently:

- **Absence of publication signals is never an error, never fatal, never a placeholder.** A
  generator that halted — or that rendered "coming soon" — would penalise exactly the discipline the
  staging stage exists to enforce.
- **Content never degrades.** The builder renders from the git host it runs on, which holds every
  repo including unpublished ones. Signals are garnish; **substance is always present.** The blast
  radius of a missing public repo is thin by construction.
- **The generator needs exactly one concept:** *signals are optional, and their absence is
  meaningful.* No error path, no maturity flag to maintain, no awareness of any host's rollout.

**Loud and fatal are not the same thing.** Non-fatal must not mean silent: a build that quietly
succeeds while repos are missing, saying nothing, is the failure to avoid. The build reports its
delta — rendered, unpublished, faulted — so the distinction between *not yet public* and *should be
there and isn't* survives. That report is a free progress signal from a system being built anyway.

> **Worked case: HappyPath.** A workshop repo, pre-public, proving the staging shape. Chosen as the
> proving repo precisely because **the interesting state is its default state** — it exercises the
> optional-signals path on day one rather than leaving it untested until something happens to be
> missing.

### 4.5 The build model — CI pulls, by identity

**A CI builder on the git host pulls repo content and config, and renders the sites.**
Source repos know nothing about CommonStage: no site config of their own, no build toolchain, no
webhook pointing back. One build produces the whole site, which is what a *common* look
requires.

This is coupling **by identity** — the builder names repos by remote coordinate, never by checkout
position — per Repository-Portability Doctrine (`CommonMind/repository-portability-doctrine.md`) §0.
Network and read access across repos, which would be a caveat elsewhere, is simply a CI runner's
normal operating condition.

**Where CI runs is deliberately out of scope here** and does not change this design. What matters to
the generator is only that *some* builder pulls by identity.

**Build trigger — DECIDED 2026-07-22: push-triggered.** A push to a source repo rebuilds its site.

⭐ **This costs nothing in coupling, because the git host and the web host are the same machine.**
An earlier draft recorded push-triggering as an optimisation to defer, on the grounds that it would
require *"every source repo to hold a webhook aimed at CommonStage — reintroducing, by a side door,
the coupling the pull model exists to avoid."* **That reasoning assumed CommonStage was a remote
consumer.** It is not: Forgejo runs on the same server as the web host, so it already observes every
push locally and fires the build itself.

**The trigger is therefore server-side and lives in exactly one place.** No source repo holds a
webhook, a workflow, or any knowledge of CommonStage — §4.5's independence claim holds **fully**,
and push-triggering is had for free. The two were never actually in tension; the tension was an
artefact of imagining a remote service.

### 4.6 The concrete config schema — CONCRETIZED 2026-07-23

§4.1 was provisional pending the tool and the proving sites. Both now exist, so the schema is
concretized **from what the two sites actually consumed**, not invented. Working examples ship at
`apparatus/schema/`. Strict JSON throughout (`CommonMind/data-format-doctrine.md`) — no comments,
`_note` for annotation.

**Two files, split by ownership (SSoT + the Independence finding):**

- **Org config — `site.json` at the org's `.github` repo root.** Org identity and shape. One per org.
- **Per-product config — `.commonstage.json` at each product repo's root.** That product's own
  facts. The org config **never restates** these — a repo owner edits their own page. (Ratified
  2026-07-23; the alternative — one central file listing every product — was rejected because it
  moves product facts away from the product.)

**Org config (`site.json`) fields:**

| Field | Req? | Notes |
|---|---|---|
| `org` | ✔ | Source-host namespace. Never rendered. |
| `hostname` | ✔ | Yields `<hostname>.schwefel.net`. Not derived from `org` (§4.1.1). |
| `shape` | ✔ | `product` \| `portfolio` (§2). |
| `name` | authored | Display name. |
| `tagline`, `blurb` | authored | Org index band + lead prose. No GitHub fallback (no org sets a description). |
| `status` | authored | `{kind, detail}` — see the enum below. |
| `hostname_variant`, `branch`, `exclude`, `order`, `featured` | optional | §4.1.1/§4.1.2 and the `portfolio` escape hatches. |

**Per-product config (`.commonstage.json`) fields:**

| Field | Req? | Notes |
|---|---|---|
| `name`, `tagline`, `role` | authored | Card + hero. |
| `status` | authored | `{kind, detail}` — the honest-status contract, below. |
| `description` | authored | Body prose. |
| `screenshots`, `install`, `featured_signals` | optional | Product-page content. |

**`status.kind` is an ENUM — this is what makes Honest (#1) enforceable rather than decorative.**
`detail` is free text that elaborates the kind (e.g. *"cold, not frozen"*), keeping nuance; `kind` is
a machine-checkable maturity claim that drives the status colour and can be validated:

| `kind` | Means | Example |
|---|---|---|
| `shipping` | Released, has versioned artifacts to download | AutoPilot (v3.5.0) |
| `active` | Usable and maintained, no formal release cadence | — |
| `living` | Mutable-by-design; evolves continuously, not versioned | CommonMind, CommonTongue |
| `beta` | Works, not yet stable | — |
| `draft` | Exists, pre-1.0, incomplete | CommonFraming |
| `wip` | Design/build stage; not yet usable | CommonStage |

The enum is **open to extension** (a new kind is added when a real product needs one), but a value
outside it is a config error, not a silent pass — so a page can never claim a maturity the set
has not defined.

**Computed, never stored** (§4.1's SSoT rule, now itemised per file): canonical URL, org colour +
mark, repo list (org); repo URL, licence, publication signals (product). Storing any of these creates
a second home for one fact.

✅ **Built 2026-07-23** — the generator that reads these two files and produces the pages now exists
(`generator/`, Python, stdlib-only). It generated the real CommonPractices portfolio site from
config alone, and the output passes the full a11y matrix. See §8b.3.

---

## 5. Relationship to existing shared assets

### 5.1 `foundation.css` is consumed, never copied

`CommonMind/assets/foundation.css` (507 lines) already exists,
is meant to be dropped into consuming projects **unchanged**, and owns colour, themes, personas, and
the two-layer accessibility floor — verified by
`CommonMind/assets/audit.js` and `CommonMind/assets/_verify.html`.

**CommonStage adds page structure only.** It must not restate or re-specify anything foundation.css
owns; that would be a second copy that drifts
(Single-Source-of-Truth Doctrine (`CommonMind/single-source-of-truth-doctrine.md`)).

**The dependency is by identity, never by checkout path.** Per
Repository-Portability Doctrine (`CommonMind/repository-portability-doctrine.md`), CommonStage names
what it needs by a coordinate that resolves on any machine — never `../CommonMind/assets/`.

> **Pre-existing violation to fix, noted here because this design surfaces it:**
> `CommonFraming/README.md` and `CommonTongue/README.md` both link to sibling repos via `../` paths
> (`../CommonMind/`, `../LiteController/`). These resolve only on a machine with that exact
> checkout layout and break for every off-machine consumer — including any rendered web view of
> those READMEs. This is the exact coupling Repository-Portability forbids. It is **out of scope for
> CommonStage** but must be fixed before those READMEs are rendered to the web.

### 5.2 CommonStage versions; CommonMind does not

CommonMind states plainly: *no releases and no version numbers — these documents are always
current by definition.* A generator that consumers pin **must** version. That asymmetry is the
cleanest proof the two are different kinds of thing and belong in different repos.

### 5.3 Profile README vs. site — two surfaces, two audiences

Both are authored; neither generates the other. This is an **accepted currency obligation**, not
drift — but it only stays honest if each surface's ownership is stated explicitly:

| Surface | Audience | Owns |
|---|---|---|
| `.github` profile README | Developers already on GitHub | Repo index (must match `gh api orgs/<org>/repos`, per Org & Repo Bootstrap), contributing, issues, org-internal facts |
| CommonStage site | People discovering the product | What it does, screenshots, install, downloads, docs, status |

The precedent is User-Documentation Doctrine (`CommonMind/user-documentation-doctrine.md`): two
audiences, two shapes. The risk it names is equally real — two half-maintained copies. The standard
must therefore state the split above as a rule, not leave it to judgement.

---

## 6. Where CommonStage lives — a fourth CommonPractices repo

**Decision: a new repo, `CommonStage`, in the CommonPractices org — a fourth repo beside
CommonMind, CommonFraming, and CommonTongue.**

(CommonPractices is a GitHub **Org**, not a grouping directory: it holds `.github` plus those three
repos. The local `~/repositories/CommonPractices/` is the on-disk org mirror per
Repository-Portability Doctrine (`CommonMind/repository-portability-doctrine.md`), which is why it is
not itself a git repository.)

### The Prime Directives analysis

Run per Decision Doctrine §11 (`CommonMind/decision-doctrine.md`).

**Lens 1 — North Stars.** *(Re-run 2026-07-22, once the set existed. It was previously recorded as
thin — CommonStage had no stated ordering, and manufacturing one to make the analysis look complete
is the failure §11 warns about. The set is now ratified in [§1a](#1a-north-stars).)*

**The ratified set supports a separate repo, and the strongest support comes from the top star.**
**Honest** (#1) requires the site to report its own delta — rendered, unpublished, faulted
(§4.4) — which means the apparatus must **release, version, and be verifiable**. CommonMind
explicitly has no releases and no version numbers, so hosting a thing that must version inside a
thing that must not is a direct clash. **Set coherence** (#7) argues the same way from the other
end: one apparatus producing one look is the founding requirement, and it needs a single home that
is neither a doctrine nor a wire contract. **Accessibility** (#2) is neutral on the *location*
question — the floor holds wherever the code lives — and is stated as such rather than stretched
into support.

**Lens 2 — Blueprints.** **No blueprint governs this shape.** Both existing blueprints are DRAFT and
hardware/service-shaped. Per the **CommonFraming Blueprint Charter §5** (in the `CommonFraming`
repo — named, not path-linked: a `../../../../` link escapes this repo and resolves only on a
machine with this exact checkout layout, the coupling
Repository-Portability (`CommonMind/repository-portability-doctrine.md`) §0 forbids and which §5.1
already flags in two sibling READMEs), the
charter is deliberately anemic about domain and explicitly anticipates a different genre — so a
*new* blueprint for a shared web presence would be legitimate. But Charter §2 is absolute: **a
blueprint ships no code you depend on.** Since the chosen scope is a full apparatus (generator,
templates, CSS, schema), CommonFraming cannot be its home. A blueprint could later describe the
*shape*; it can never hold the apparatus.

**Lens 3 — Best Practices.** The idiomatic answer is unambiguous: a shared theme/generator is its
own versioned package consumed by many sites — Hugo themes, Jekyll gems, Astro integrations, Sphinx
themes all ship this way. Nobody vendors a generator inside a prose-docs repo. This lens points at a
separate repo, and equally hard *away* from `CommonMind/assets/`.

**Lens 4 — Correctness / SSoT.** The decisive lens. **Every existing CP repo has a written charter
that this apparatus falsifies:**

| Repo | Its charter says | CommonStage would require |
|---|---|---|
| CommonFraming | "ships no code you depend on" | shipping code you depend on |
| CommonTongue | runtime wire contracts so independent *programs* interoperate | a build-time site tool — different consumers, lifecycle, failure mode |
| CommonMind | "no releases and no version numbers" | a versioned artifact consumers pin |

Three charter amendments to avoid one repo is the worse trade. CommonTongue's own README sets the
precedent for splitting on altitude rather than stretching a repo: *"this is why it is its own repo
and not part of blueprints."*

**Recommendation:** new repo. Its cost is one more repo; the alternative is weakening
three charters that are currently true.

---

## 7. Sequencing — two sites, then extract

**Build two sites concretely first. Extract the shared apparatus from proven duplication second.**

1. **Build TestingAutoPilot's site** (`product`) — real HTML/CSS, hand-assembled.
2. **Build CommonPractices' site** (`portfolio`) — likewise, including rendered docs.
3. **Extract** templates, config schema, and generator from what actually proved invariant across
   the two shapes.

**Why not design the generator up front.** A shape derived from a single instance is a hypothesis —
the discipline behind Held-Out-Oracle Doctrine (`CommonMind/held-out-oracle-doctrine.md`) and Blueprint
Charter §5's warning against over-abstracting from one instance. The proving pair already earned its
keep before either site exists: it surfaced the *one product, many repos* vs *many products, one
org* distinction, which a single-org design would have missed entirely.

---

## 8. Open questions

These are **not decided.** Recorded per Decision Doctrine §8 (record what is NOT decided).

### 8.1 Docs rendering — RESOLVED by the choice of proving pair

Scope includes rendered documentation sites. Navigation generation, anchors, search, cross-document
linking, and code highlighting are most of the engineering — far more than landing pages.

An earlier draft paired TestingAutoPilot with SurfaceWorks and flagged that **neither is the hard
docs case**, leaving the expensive half of the apparatus unproven. **Resolved 2026-07-21 by the
owner: the `portfolio` half of the pair is CommonPractices, not SurfaceWorks.** CommonMind alone is
37 files / ~7,250 lines with dense inter-doctrine cross-linking and a README whose Documents table
is ~35 substantial paragraphs in markdown table cells — the hardest docs target.

Docs rendering is therefore proven in phase one rather than deferred, and CommonStage is
self-hosting (see §2, *Worked pair*).

**What remains open** is not *whether* to render docs but *how far*: search, per-doctrine navigation,
anchor stability across renames, and how the CommonMind README's dense table renders on the web are
all unspecified. Those are implementation questions for the plan, not design questions.

### 8.2 Stack — DECIDED 2026-07-22: **Zola**

**Zola** — a single Rust binary, Tera templating.

**Why, against the ratified stars.** The product pages are **app** pages — screenshots, install
flows, status indicators, download counts — which is bespoke layout, not docs chrome. That is
precisely where a batteries-included docs theme helps least, and **Comprehension** (#3) and
**Obtainability** (#4) both live on exactly those pages. Zola gives templating control without a
Node toolchain; Tera is the middle ground between Hugo's Go templates and a full JS stack.

✅ **Web UI §2 conformance — VERIFIED, not assumed (2026-07-22).** The constraint that can
disqualify a candidate outright is whether the build leaves CSS as editable, replaceable files.
Zola's documented behaviour: files in `static/` are *"copied, without modification, to the public
directory"* — verbatim, no processing, no minification. Sass compilation is **opt-in** (prompted at
`zola init`), not forced. So `CommonMind/assets/foundation.css` ships as the
drop-in editable asset Web UI §2 (`CommonMind/web-ui-doctrine.md`) requires.
*Source: Zola docs, content overview + getting-started.*

⚠️ **Still unverified and owed by the plan** — conformance of the *artifact*, which no amount of
tool-choice settles:
- The **hostile-stylesheet attack** (Web UI §2.1 (`CommonMind/web-ui-doctrine.md`),
  Visual Identity §6 (`CommonMind/visual-identity.md`)): the `@layer floor-hard` / `floor-soft` floor is
  trusted **only once a stylesheet genuinely trying to break it has been watched to fail** against
  the unprotected version. Watching it fail is the test; a passing run alone proves nothing.
- **Sibling-content pulling** (§4.5) — Hugo has native submodules/mounts; Zola's mechanism for
  assembling content from many repos is unproven here and is a first-phase risk.

> **Correction — the earlier framing was a false binary.** This section previously offered only Hugo
> and Astro/Starlight, presented as the choice. Those are the two *conventional* answers, not the
> flexible ones, and the middle of the range was never shown: **Eleventy** (maximum templating
> control, choose your own template language) and **Zola** itself both went unmentioned until the
> owner asked directly for options giving more flexibility. **Presenting two options as "the choice"
> when five were live is a failure to survey, and it nearly decided the stack by omission.**

**Superseded reading, kept for provenance:** build speed does not discriminate at this scale
(~37 files against a ~500-page threshold), which is why **Speed is not a star** (§1a.3). The
deciding axis was templating control and toolchain weight, not throughput.

### 8.3 Empty `portfolio` org — DECIDED 2026-07-22

**Withdrawn as originally written.** An earlier draft claimed DeckLibre existed both as its own Org
and as a SurfaceWorks product, and raised a nesting/SSoT question. **That premise was false**,
asserted from a stale memory rather than checked: verified 2026-07-21 against
`gh api orgs/{DeckLibre,SurfaceWorks}/repos` — SurfaceWorks holds exactly `.github`, Lucidity,
Palette, Codex, and **DeckLibre is a separate org that does not appear in it.** No product is
currently nested in two orgs, so there is no nesting question to answer.

The real open item the check surfaced instead: **DeckLibre is an org holding only `.github` — no
product repos.** Under `portfolio` (every repo is a product, with `.github` excluded by rule) it
renders an index with **zero** product cards. Two of seven orgs are in this state today
(StudioEnsemble and DeckLibre), so this is present-state behaviour, not an edge case.

**DECIDED 2026-07-22: render the org page, omit the product list.** Org identity, tagline, and
blurb render normally; the product section is simply absent — no cards, no placeholder, no
"coming soon", and the site is **not** skipped.

**Why this is the Honest (#1) answer.** The org genuinely exists and has an identity worth
showing; what does not exist is a published product. Rendering the org while omitting the product
list states exactly that and nothing more. The alternatives each say something false or unhelpful:
skipping the site entirely implies the org does not exist, and a placeholder card advertises a
product that has not been published — the same overstatement §4.4 forbids for pre-public repos.

**This is §4.4's rule applied at org scale:** absence is rendered as absence, never dressed up and
never hidden. A product repo appearing later adds cards with **no config edit**, which is the shape
flag working as intended.

### 8.4 Hosting — DECIDED: the owner's own server

**Resolved 2026-07-21 by the owner: sites are hosted on a server the owner fully controls**, not
GitHub Pages. The VPS already serves other sites, so the marginal cost per site is near zero, and
`schwefel.net` is owner-controlled DNS.

**Server-side analytics are explicitly OUT OF SCOPE for CommonStage.** Access logs land on the
owner's server and the owner surfaces them by their own means. CommonStage neither configures,
collects, nor reports them, and **the site config carries no analytics field.** No third-party
beacon and no client-side collector is introduced by the standard.

What remains open is only the **deploy path** (Actions→rsync over a deploy key, a pull-based hook,
or otherwise) — an implementation question for the plan, not a design question.

### 8.5 North Star set — RESOLVED 2026-07-22

**Closed. CommonStage's own ordered set is ratified and lives in [§1a](#1a-north-stars)**, which is
the authoritative statement per North Stars Doctrine §2 (`CommonMind/north-stars-doctrine.md`).

Honest · Accessibility · Usability · Choice · Comprehension · Obtainability · Set coherence (§1a).

**What the gap actually was.** Not invented values — the borrowed ordering was real and
ratified (verified 2026-07-21 in `SurfaceWorks/.github/profile/README.md`). The defect was
**silent inheritance**: CommonStage invoked a sibling's set without stating one of its own, which
§2.1 (`CommonMind/north-stars-doctrine.md`) permits only as an explicit ratified choice. That route was
available and **deliberately not taken** (§1a.3).

**How it closed, and the error worth keeping.** A first draft derived stars from the build pipeline
and produced documentation values for a product whose repos are **apps**. The owner rejected it;
the ordering shape survived, the subjects did not. The owner also **promoted Accessibility from a
floor to a ranked star**, correcting the spec's claim that CommonStage's modality surface was too
narrow to make it decide anything. Full provenance in §1a.

**Doctrine §6 checklist — all met:** 3–5 ordered stars with glosses in the project's own docs ·
framework cited, not re-derived · no silent inheritance · each star shown forcing an outcome (§1a.1,
with `Obtainability` flagged as thinnest) · accessibility accounted for as a ranked star (§1.4's
first form) · one authoritative statement, others pointing to it.

⚠️ **Remaining:** the set is stated in this spec, which still lives in CommonMind's `_working/`.
It must travel with the spec into the CommonStage repo, and be **pinned to a decision log** with
provenance greppable — the one checklist item that cannot be completed until the repo exists.

### 8.6 Which config holds deployment-shaped facts

Three things now resolve to a hostname: the org namespace, the explicit `hostname`, and the variant
affix (§4.1.1). The first two are **identity** facts — what this org *is*. The affix is a different
kind: a fact about **this deployment**, not about the org or the repo. `branch` (§4.1.2) is the
same kind.

§4.1 established that `hostname` is not derived from `org` precisely because they are different
kinds of fact. By that same reasoning, deployment-shaped fields may not belong in the identity
config at all.

**Not decided, and deliberately not resolved by default.** Deployment mechanics are out of scope for
now, so putting these fields in the identity config *provisionally* risks calcifying a placement
nobody chose. Recorded here so the placement stays a decision rather than an accident.

> **Status 2026-07-23:** §4.6 places `hostname_variant` and `branch` in the org `site.json` under
> `_optional` — **provisionally**, exactly as this section warns. Convenient for now (one file), but
> **still not ratified as their home.** If a deployment-shaped config emerges later, they move there.
> The placement is marked, not settled.

### 8.7 Workshop is first-class — render-everything **retained** (owner ruling, 2026-07-22)

**`jschwefel-workshop` is a first-class org**, and — the owner's framing, which corrects this spec's
premise — **workshop is where projects the owner *wants in the public eye* are put.** §9 previously
said only *"check before applying `portfolio` to it"*, and §8a A4 treated it as *sui generis*. Both
underestimated it. HappyPath, a **workshop repo**, is the worked case proving the pre-public pattern
(§4.4), so workshop is load-bearing.

**Ruling: `portfolio` keeps rendering everything, with `exclude` as the escape hatch.** No opt-in
inversion, no third shape, no per-repo maturity field.

**Why this is correct, not merely accepted.** This spec initially argued for an opt-in inversion on
the grounds that a workshop holds *"repos not intended for public presentation"* which
render-everything would surface, colliding with **Honest (#1)**. **That premise was wrong.**
Workshop's purpose *is* public visibility — so render-everything is the behaviour that matches the
org's intent, and an opt-in list would suppress exactly what the org exists to show.

**What Honest actually demands here** is narrower than the earlier reading, and it is a
**presentation** requirement rather than an inclusion one: a workshop project must not be **dressed
up as a shipping product.** Star #1 forbids overstating readiness; it does not forbid showing
unfinished work. Showing an experiment, plainly labelled as an experiment, satisfies it fully —
whereas rendering that same experiment with a polished product card and a download button would
violate it while including exactly the same repos.

**Consequently §4.1's *"no hand-maintained product list"* stays true** — a new repo appears with no
config edit, which is the flag's whole point.

**What the plan owes** — moved from *"review the exclude list"* (the earlier, wrong-premise task) to
the real one: **the product-page template must render an unfinished project honestly.** Status is
not decoration on that page; it is what keeps star #1 satisfied for the whole workshop org. This is
the same gap §8a A2 flags — a product template fitted to shipping products — and workshop is where
it bites first and hardest. `exclude` remains available for the occasional genuinely-private repo,
but it is **not** the mechanism protecting star #1.

> ⭐ **PD dependency, recorded 2026-07-22.** This decision (render-everything) satisfies Honest
> status **only if** the template renders an unfinished repo *as* unfinished — never dressed as a
> shipping product. That guarantee lives entirely in **§8b F2** (the template must distinguish
> maturity honestly). **Render-everything is therefore conditional on F2**; if the template does not
> visibly distinguish shipping from unfinished, render-everything violates star #1. The dependency
> is made explicit here so it cannot be lost when the template is built.

---

## 8a. Adversarial review — 2026-07-21

The design was attacked deliberately (owner-requested) and each finding dispositioned by the owner
the same day. **Recorded so the attacks are not re-derived, and so a dismissal is visible as a
judgement rather than an oversight.**

> **Framing the owner set, which governs every row below:** *"All of the PDs will be satisfied. This
> is EARLY stage."* Several attacks below applied a maturity bar this work has not reached — an
> unratified North Star set and an unchosen stack are **not yet**, not **defects**. They are recorded
> in §8 and do not gate design.

| # | Attack | Disposition |
|---|---|---|
| **A1** | The pair proves `portfolio` twice and `product` once (n=1); `product` may be "an index with one card minus the index" — a boolean inflated into an architecture. | **REJECTED.** `product` is a genuine shape with its own content, not a degenerate index. |
| **A2** | `portfolio` renders repos, but products aren't repos: CommonMind (37 doctrine files), CommonFraming (ships no code), CommonTongue (a package) would each get a product page whose install/downloads/screenshots fields are empty. | **ACCEPTED, deferred.** "We will deal with it." Most of the set is WIP and CP is the closest thing to a full repo set that exists — which is *why* it is the proving site. Surface the template mismatch when the build hits it. |
| **A3** | Config in `.github` splits product identity across two repos and creates an unnamed currency obligation. | **MOOT — attack was misaimed.** The org is a **suite** (M365 : Word/Excel). Org-level identity belongs in `.github`; product facts belong to the product repo. Two tiers, not one split. |
| **A4** | "No maintained product list" is false once `exclude`/`order`/`featured` are used; jschwefel-workshop (unrelated one-offs) is the live counterexample. | **NOTED, bounded** at the time. ⚠️ **Superseded 2026-07-22 (§8.7):** "workshop is *sui generis*" was the owner's framing then, but workshop is now **first-class** — the org for projects meant for the public eye. The attack lands even more weakly than recorded: render-everything matches that org's intent, so `exclude` is incidental rather than load-bearing. |
| **A5** | Docs rendering is claimed proven, but the design has no position on the hardest artifact — CommonMind's 47 KB README whose Documents table is ~35 paragraphs in markdown cells. | **ACCEPTED as work, not defect.** "Then we prove it." This is exactly what the CP proving site is for. |
| **A6** | Self-hosting is stated only as an upside; it is also a circular dependency — if CommonStage breaks, the doctrine site breaks with it. | **ACCEPTED, executive decision.** Bounded: a static generator can render CommonMind from anywhere, so the coupling is deployment-time only, not structural. |

**One finding survives as a spec correction rather than a design change** — see §1: two of the seven
in-scope orgs (**StudioEnsemble**, **DeckLibre**) currently have *no pushed product repos*, only
`.github`. A `portfolio` render of either produces an empty index today. This makes §8.3's
"empty/single-repo `portfolio` org" not a hypothetical edge case but **the present state of 2 of 7
orgs** — verified 2026-07-21 via `gh api orgs/<org>/repos`. StudioEnsemble's CameraConductor and
LiteController exist **locally but unpushed**.

---

## 8b. Findings from the first hand-built page (2026-07-22)

The first product page (TestingAutoPilot, hand-written before any template) surfaced findings that
belong in the design, not just in that page's CSS. It was built from real repo content and driven to
**pass the full accessibility matrix by measurement** — 48 text elements × 5 themes × colour-blind
on/off, 10/10 cells, zero failures, with a self-testing contrast checker that rejects a known-bad
pair each run.

**F1 — the canonical theme set is `CommonMind/visual-identity.md §1a`, not `foundation.css`.** The
five required themes are **daylight · dark · warm · paper · maxcontrast**, plus the **colour-blind
modifier** (`data-cb`), which §1a is explicit is *not* a theme and cannot be dropped. `foundation.css`
*implements* this; the doctrine *defines* it. A CommonStage template **must** ship all five in one
picker plus a separate colour-blind toggle (the §-checklist requirement), and the generator should
treat the theme set as coming from the doctrine, never hard-code its own list.

**F2 — `product.css` must not be free to place arbitrary ink-on-surface combinations. This is the
strongest template-contract signal so far.** Every contrast failure came from the page CSS choosing a
foundation ink for a surface foundation did not calibrate it against:

- Page-ground inks (`--ink-dim`, `--ink-faint`) placed on a **coloured band** — bands carry their own
  `--band-ink`, calibrated per theme.
- An **accent fill** behind light text — foundation deliberately never fills with `--accent` (dark
  `--accent` = `#FF4438` gives white only ~3.4:1); its primary button is `--ink` on `--ground`, and
  accent is used for **borders/text**, never a fill.

**⭐ HARD REQUIREMENT (PD-ratified 2026-07-22): the template MUST constrain which foundation tokens
are legal on which surface** — band text → `--band-ink`; primary action → `--ink`/`--ground`; body →
page inks — so a page author *cannot* reintroduce these failures. This is Web UI §2.1's
(`CommonMind/web-ui-doctrine.md`) *"cosmetic freedom over a floor the stylesheet cannot break"*
applied to the **template layer**, not just the CSS cascade. It is the concrete form of §8a A2's
warning that the product template is the untested part.

> **Why HARD, per the PD run.** Accessibility is North Star #2. An unconstrained `product.css` is
> *how all ~20 contrast failures happened*, and the page passes today only because it was hand-fixed
> and measured. "The template is safe" is therefore **true of one page by hand, not true of the
> system** — the §11 Correctness trap (a claim that holds for the instance asserted as if it holds
> for the system). Leaving the palette free would rest stars #2 and #4 on manual vigilance. The
> constraint is not a nicety; it is what makes the accessibility claim true at the template layer.

**F3 — the hostile-stylesheet acceptance test (Web UI §2.1) — DONE, PASSED 2026-07-22.** F2 keeps a
*well-meaning* author safe; F3 proves the floor holds against a *hostile* one. Executed as a true
negative control:

- **Attack** (`sites/testingautopilot/static/hostile.css`, **never shipped**): four weaponised
  real-world a11y catastrophes — `outline:none !important` on `:focus-visible`, `display:none` on
  `[aria-live]`, buttons collapsed below min size, `.sr-only` un-hidden then hidden from all.
- **Control** (`f3-control.html`, hostile.css with **no** foundation): **all four attacks landed** —
  focus killed, live region muted, button 1px, sr-only broken. The attack is proven lethal.
- **Protected** (`f3-protected.html`, foundation.css **then** hostile.css): **floor held on all
  four** — focus `solid 3px`, live region visible, button `24px`, sr-only reachable. The
  `@layer floor-hard`/`floor-soft` construction beats `!important` by layer order alone.

The floor is trusted because it was **watched to fail on the control before holding on the
protected page** — not asserted. The three files stay in the repo as a permanent, re-runnable
acceptance test. **`hostile.css` is a test fixture and must never be linked from a shipped page.**

**F4 — build-time signals confirmed reachable.** Real release/download data (`gh api` on the org's
repos) rendered as page content without any browser-side call — the §4.3 build-time-fetch decision is
implementable as specified.

**Stack conformance, measured (supersedes §8.2's doc-only check):** `foundation.css` placed in Zola's
`static/` arrived in `public/` **byte-for-byte identical** (23,813 bytes, `cmp` clean). Web UI §2's
editable-replaceable-CSS requirement is verified against the real shipped file, not just Zola's docs.

### 8b.1 The product-page shape is NOT a CommonFraming blueprint

Considered and **rejected 2026-07-22.** A blueprint describes a recurring *shape that others build
instances of* (`CommonFraming/CHARTER.md` §1). The product-page shape is not that: **CommonStage is
the builder of these pages — the shape is its own output, not a pattern anyone reimplements.**
Abstracting it into CommonFraming would describe CommonStage's job back to it. The shape lives where
it is produced: in CommonStage. (Owner's read; the earlier "future blueprint candidate" note was
wrong on this and is withdrawn.)

### 8b.2 Findings from the second site (CommonPractices `portfolio`, 2026-07-22)

The `portfolio` proving site — org index + one product page per repo (CommonMind, CommonFraming,
CommonTongue, CommonStage), built from real `gh api` data.

**F5 — the F2 discipline is validated by evidence, not just argued.** The first site (AutoPilot)
needed ~20 contrast fixes. The second reused the same F2-disciplined `product.css` (band text →
`--band-ink`, badge text → `--ink` on a status `-bg`) and **passed the full matrix — index and
product page, 10/10 cells each — on the *first* build.** Building to the token-on-surface rule from
the start is what made it pass first-try. This is the measured payoff of §8b F2 being a hard
requirement, and it is the strongest single argument for extracting that rule into the template.

**F6 — the portfolio product pages are already data-driven, not hand-copied.** One shared
`product-page.html` template + four content files carrying per-repo front-matter (role, tagline,
status, repo link). This proves the **config → page** generation the spec calls for — a step beyond
the first site's hand-written HTML — and shows the extracted apparatus's shape: a template consuming
per-product data.

**F7 — honest status is load-bearing and works.** Each product carries a plain status
(living / draft / design stage) on its card and page; CommonStage's own page says *"design stage · no
code yet … never dressed up as finished."* This is North Star #1 and the §8.7 workshop dependency in
practice — the site states maturity, never inflates it.

**Zola mechanics learned (for the plan):** section pages expose `section.*`, regular pages expose
`page.*`; a per-product page is a **colocated page** (`content/<slug>/index.md`, *not* `_index.md`)
so `page.title`/`page.extra.*` resolve. `zola init` writes `zola.toml` (not `config.toml`) and needs
a full URL with scheme.

### 8b.3 The generator — built and verified 2026-07-23

The config-driven generator (`generator/`, Python, stdlib-only) now exists. It reads the §4.6 config
files, computes the derived facts, fetches optional signals, assembles a Zola site from `apparatus/`,
runs `zola build`, and prints the delta report. Thin orchestrator over `generator/lib/` per the
the scripting doctrine.

**What building it confirmed:**

- **F5 held at generator scale.** The generator emits the same apparatus CSS + templates, so the
  generated CommonPractices portfolio (index + 4 product pages, from config alone) **passes the full
  a11y matrix — 10/10 cells, index and product page, zero failures.** The F2 token-on-surface
  contract, extracted into `stage.css`, carries through to generated output for free. This is the
  payoff of making F2 a hard requirement: it holds without per-site vigilance.

- **§4.4 "loud ≠ fatal" works as specified.** A **negative control** — one repo given an off-enum
  `status.kind` — faulted that repo with a mapped error (file, bad value, allowed set, spec ref),
  **still rendered the other three**, and exited non-zero. A broken or forgotten repo can never read
  as success.

- **The honest-status enum is enforced, not decorative.** `status.kind` outside the defined set is a
  fatal config error. The validating test was **watched to fail with the check disabled**, then pass
  restored — the fix-isn't-fixed gate. A page cannot claim a maturity the set has not defined.

- **Apparatus templates parameterized by config.** `product-page.html` and `portfolio-index.html`
  moved into `apparatus/` and read the org name from `config.extra`, so **one template set drives any
  org** — no per-org template. The apparatus is now the complete rendering source.

- **A real bug, caught by the delta report, not a silent bad build.** First run serialized `signals`
  as JSON `null` into TOML front-matter, which Zola rejects; the report **faulted** rather than
  emitting a broken site. Fixed by omitting absent signals entirely (absence rendered as absence,
  never a fabricated zero).

**Both shapes now verified end-to-end.** The `product`-shape path (org IS the product) was closed the
same day: regenerating AutoPilot from config surfaced a real bug — the single product is the site's
index *section*, which exposes `section.*`, not `page.*`, so `product-page.html` failed. Fixed with
`product-index.html` (the section-variable variant), and the regenerated `product` site **passes the
full a11y matrix, zero failures**. A regression test guards it. So **both shapes generate from config
and both pass the matrix.**

**Still open (honestly):** deployment (getting output onto the server behind `*.schwefel.net`) and
the Forgejo push-trigger wiring remain out of scope, as before. Publication signals are exercised
only without a token (so they read as absent-but-expected); a token'd run against live counts is
untested.

---

## 9. What this design does not cover

- The visual design itself — CommonStage owns page *structure*; foundation.css owns the *look*.
- Per-product content (copy, screenshots) — authored per product, not by this standard.
- The visual design itself is covered above; workshop's shape is **no longer** an uncovered item —
  see §8.7. It was previously listed here as *"check before applying `portfolio` to it"*, which is
  insufficient now that the org is first-class.
