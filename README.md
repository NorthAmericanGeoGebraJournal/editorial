# NAGJ Editorial

The editorial office of the **North American GeoGebra Journal** (ISSN 2162-3856).

Submissions and peer review happen here, in the open, as GitHub Issues. The
published journal lives at [geogebrajournal.com](https://geogebrajournal.com)
([website repo](https://github.com/NorthAmericanGeoGebraJournal/website)).

> **Status: draft.** Every checklist and policy in this repo is a placeholder for
> the editorial board to revise. Nothing here is in force yet.

---

## For authors

1. Read [the review process](policies/review-process.md) and
   [publication ethics](policies/publication-ethics.md).
2. Prepare your manuscript from the
   [article template](https://github.com/NorthAmericanGeoGebraJournal/article-template).
3. Open a **[submission issue](../../issues/new?template=submission.yml)**.

There are no submission fees and no publication fees.

## For reviewers

Everything you need is in the review issue itself: the editor posts your
checklist there, you work through it in the open, and the conversation is the
review. See [the reviewer checklist](checklists/reviewer.md).

Reviews are **signed and public**. Your name appears on the review record, and it
is permanently citable — that is the point. If you would rather not review in the
open, tell the editor; that is a legitimate answer and not held against you.

## For editors

See [the editor checklist](checklists/editor.md).

---

## How review works here

```
Author opens a submission issue
        |
        | editor checks scope and conflicts
        v
Editor assigns reviewers, posts checklists in the issue
        |
        | reviewers work in the open; author revises
        v
Editor accepts
        |
        | bot opens a PR against the website repo
        v
Published, with a permanent link back to this review issue
```

The issue **is** the review record. There is no separate file to maintain, and
nothing is deleted — a published article links back to the thread that produced
it.

## What NAGJ reviews

The **paper** is the object of review. NAGJ publishes work on the use of GeoGebra
in mathematics education (K–16), not GeoGebra software itself.

A GeoGebra resource is **welcome and encouraged, but not required**. A paper that
gives the construction commands, or shows figures a reader can follow, is
complete without one. Where a resource does exist, it is hosted by the author —
normally on [geogebra.org](https://www.geogebra.org/) — and the journal records
its permanent URL. **We do not host applets.**

The question a reviewer is really answering is *can a reader recreate this?* An
applet is one good answer. Commands are another. Figures can be a third.

---

## Repository layout

```
.github/ISSUE_TEMPLATE/   submission and correction forms
.github/workflows/        automation (@nagjbot commands)
checklists/               what editors and reviewers actually check
policies/                 review process, ethics, conflicts, conduct
templates/                editor boilerplate: decisions, requests
scripts/                  the logic the workflows call
```

## A note on the bot

Automation here does **process**, not judgement: it validates metadata, builds
PDFs, creates review issues, tracks assignments, and prepares publication. It
does not evaluate mathematics, assess pedagogy, or recommend decisions. Those are
the reviewers' job and the editor's.

The bot runs as GitHub Actions rather than a hosted service — deliberately. At
this journal's volume, a deployed application would be more to maintain than it
would ever save.
