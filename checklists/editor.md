# Editor checklist

> **DRAFT — for the editorial board to revise.** Placeholder wording, and the
> timings below are invented. Nothing here is in force yet.

---

## On a new submission

Aim to do this within *(board to set — JOSS targets days, not weeks)*.

- [ ] **Scope.** GeoGebra in mathematics education, K–16? If not, say so kindly
      and quickly — a fast, clear rejection is a kindness compared to a slow one.
- [ ] **Conflicts.** Do you have one with these authors? If so, hand off to
      another editor and say so in the thread.
- [ ] **The author checklist is genuinely complete**, not just ticked.
- [ ] **The manuscript is reachable** and contains what it should.
- [ ] **`@nagjbot check`** — metadata validates, the PDF builds, links resolve.
- [ ] **Reproducibility.** Applet, commands, or figures — at least one route
      exists. If none, that is a revision request *before* review, not something
      to hand reviewers.
- [ ] Label `pre-review` → `under-review` once reviewers are on.

## Assigning reviewers

- [ ] Two reviewers *(board to confirm the number)*
- [ ] Between them they cover **mathematics** and **pedagogy** — those are
      different skills and rarely the same person
- [ ] Neither has a conflict (see [the policy](../policies/conflicts-of-interest.md))
- [ ] Each has **agreed** — never assign someone who hasn't said yes
- [ ] Each understands the review is **public and signed**
- [ ] Post [the reviewer checklist](reviewer.md) in the issue for each

> If a paper has no GeoGebra resource, say so when you invite reviewers, so they
> don't treat its absence as a defect. It isn't one.

## During review

- [ ] Check in *(board to set a cadence)* — silence is the main way review dies
- [ ] Keep it civil and specific. You own the tone of the thread.
- [ ] Step in if a reviewer strays into "not how I'd do it" as though it were
      "wrong"
- [ ] If a reviewer goes quiet, chase once, then replace them and say so publicly
- [ ] Make sure the author knows they can respond as it goes

## Deciding

You decide — reviewers advise. Say why, in the thread.

- [ ] **Accept** — `@nagjbot accept`
- [ ] **Minor revision** — author revises, you check, no second round
- [ ] **Major revision** — back to reviewers after revision
- [ ] **Reject** — be clear about which: out of scope, or not repairable. Say
      whether a resubmission would be welcome.

## Publishing

- [ ] `@nagjbot publish` opens a PR against the website repo
- [ ] Check the record: authors' names **spelled correctly, with diacritics**;
      affiliations; pages; ORCIDs
- [ ] `review_issue` points back to this thread
- [ ] Merge; confirm it renders
- [ ] Thank the reviewers in the thread. Their names are on this permanently —
      that is the only payment they get.

---

## Notes for editors

**Reject fast, accept slowly.** An out-of-scope paper should hear back in days.

**The names matter.** The legacy corpus has diacritics stripped throughout —
`Jan Guncaga` for `Ján Gunčaga` — because it was imported from a source that had
already flattened them. Don't add to it. Check names against the manuscript.

**Public review is a commitment you make to reviewers too.** They put their name
on their judgement. Back them when they're right; correct them in the open when
they're not.

**"No applet" is not a deficiency.** The paper is the object of review. Watch for
reviewers reaching for a software-review posture that doesn't apply here.
