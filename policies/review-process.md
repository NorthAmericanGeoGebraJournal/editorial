# Review process

> **DRAFT — for the editorial board to revise.** Placeholder wording; every
> timing is invented. Nothing here is in force yet.

---

## What NAGJ reviews

The **paper**. NAGJ publishes work on the use of GeoGebra in mathematics
education, K–16 — not GeoGebra software.

A GeoGebra resource is **encouraged but not required**. Where one exists it is
hosted by the author, normally on [geogebra.org](https://www.geogebra.org/); the
journal records its permanent URL and does not host applets.

The question review turns on is **can a reader recreate this?** A working applet
is one good answer; construction commands are another; figures and a described
procedure can be a third. A paper needs one of them. It does not need all three,
and it does not need an applet.

## Open review

Review is **public and signed**:

- The review conversation is a **public GitHub issue**.
- **Reviewers are named.** So are authors. There is no anonymity in either
  direction.
- The thread is **permanent and citable**, and published articles link back to it.
- It stays public **whether the paper is accepted or rejected**.

We do this because it makes reviewers accountable for what they write, lets
authors see who wrote it, gives reviewers public credit for unpaid work, and
makes the reasoning behind a decision inspectable rather than a mystery.

The cost is real and worth stating plainly: **a rejection remains visible.**
Authors should weigh that before submitting. Reviewers who would rather not
review in the open should say so — it is a legitimate answer.

## The stages

**1. Submission.** The author opens a submission issue and confirms the
[author checklist](../checklists/author.md).

**2. Editor triage** *(target: board to set)*. An editor checks scope and
conflicts. Out-of-scope work is declined quickly — a fast no beats a slow one.

**3. Reviewers.** The editor assigns *(number: board to confirm)* reviewers,
covering mathematics and pedagogy between them, and posts
[the checklist](../checklists/reviewer.md) in the issue.

**4. Review.** Reviewers work in the open. **Authors may respond as it goes** —
this is a conversation, not a verdict delivered at the end. Reviewers are
encouraged to post partial reviews rather than one final block.

**5. Revision.** The author revises in their own repository. The bot can rebuild
the PDF on request.

**6. Decision.** The editor decides — accept, minor revision, major revision, or
reject — and says why in the thread. Reviewers advise; the editor decides.

**7. Publication.** The bot opens a PR against the website repo. An editor checks
the metadata and merges. The article links back to its review issue.

## What the bot does

Process, not judgement. It validates metadata, builds PDFs, creates review
issues, tracks assignments, and prepares publication.

It does **not** evaluate mathematics, assess pedagogy, recommend decisions, or
review anything. **No AI evaluates submissions.** Those are human judgements and
they stay that way.

## Fees

None. No submission fee, no publication fee, no page charges, no colour charges.
Ever.

## Appeals

*(Board to write.)* Who hears an appeal, on what grounds, and how.

## Withdrawal

An author may withdraw before a decision by saying so in the issue. The issue
remains public — it is part of the record — and is closed as withdrawn.

## Corrections after publication

See [publication ethics](publication-ethics.md). Open a correction issue.
