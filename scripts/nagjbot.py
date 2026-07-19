#!/usr/bin/env python3
"""nagjbot -- the NAGJ editorial bot command handler.

Invoked by .github/workflows/nagjbot.yml when an editor comments `@nagjbot
<command>` on a submission issue. This script does the work and prints a
Markdown report to stdout; the workflow posts that back as an issue comment.

It automates PROCESS, never judgement: it validates and reports, it does not
decide whether a paper is any good.

Commands:
  help                 list the commands
  check                validate the manuscript linked in the submission issue

Usage (from the workflow):
  python scripts/nagjbot.py <command> --body-file <issue-body.md>

Local testing (skip the clone, point at a manuscript directory):
  python scripts/nagjbot.py check --local ../article-template
"""

from __future__ import annotations

import argparse
import os
import re
import subprocess
import sys
import tempfile

try:
    import yaml
except ImportError:
    sys.exit("missing dependency: pyyaml (pip install pyyaml)")

ARTICLE_TYPES = {
    "Research Article", "Teaching Note", "Classroom Activity",
    "Technical Note", "Proceedings Article",
}

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Commands that change editorial state run ONLY for listed editors. Everything
# else (check, build, help) is open to anyone with repo write access, which the
# workflow's `if:` guard already enforces.
EDITOR_ONLY = {"accept", "publish", "create-review", "assign"}

FRONT_MATTER = re.compile(r"\A---\s*\n(.*?)\n---\s*(?:\n|\Z)", re.DOTALL)


# --------------------------------------------------------------------------
# Parsing the submission issue (GitHub issue-form body)
# --------------------------------------------------------------------------

def load_editors() -> list[str]:
    """GitHub usernames allowed to run privileged commands, from editors.yml."""
    path = os.path.join(REPO_ROOT, "editors.yml")
    try:
        data = yaml.safe_load(open(path, encoding="utf-8")) or {}
    except (OSError, yaml.YAMLError):
        return []
    return [str(u).lower() for u in (data.get("editors") or [])]


def is_editor(actor: str | None) -> bool:
    return bool(actor) and actor.lower() in load_editors()


def parse_issue_form(body: str) -> dict[str, str]:
    """Turn a GitHub issue-form body into {heading: value}.

    Issue forms render as `### Heading\n\nvalue` blocks. A field the author left
    blank renders as the literal `_No response_`, which we treat as empty.
    """
    fields: dict[str, str] = {}
    for heading, value in re.findall(r"^###\s+(.+?)\s*\n(.*?)(?=^###\s|\Z)", body, re.DOTALL | re.MULTILINE):
        value = value.strip()
        if value == "_No response_":
            value = ""
        fields[heading.strip()] = value
    return fields


def find_repo_url(fields: dict[str, str]) -> str | None:
    """Pull the manuscript repository URL out of the parsed fields."""
    raw = fields.get("Manuscript repository", "")
    match = re.search(r"https?://github\.com/[^\s)]+", raw)
    if match:
        return match.group(0).rstrip("/").removesuffix(".git")
    return None


# --------------------------------------------------------------------------
# Validating the manuscript
# --------------------------------------------------------------------------

def read_front_matter(path: str) -> tuple[dict | None, str]:
    with open(path, encoding="utf-8") as handle:
        text = handle.read()
    match = FRONT_MATTER.match(text)
    if not match:
        return None, text
    try:
        data = yaml.safe_load(match.group(1))
    except yaml.YAMLError as exc:
        raise ValueError(f"paper.md front matter is not valid YAML -- {exc}") from exc
    return (data if isinstance(data, dict) else {}), text


def check_manuscript(root: str) -> list[tuple[bool, str]]:
    """Return a list of (ok, message) checks for a manuscript directory."""
    results: list[tuple[bool, str]] = []

    def ok(cond, msg):
        results.append((bool(cond), msg))
        return bool(cond)

    paper = os.path.join(root, "paper.md")
    if not ok(os.path.isfile(paper), "`paper.md` is present"):
        return results  # nothing else is checkable without it

    try:
        fm, text = read_front_matter(paper)
    except ValueError as exc:
        ok(False, str(exc))
        return results

    if not ok(fm is not None, "`paper.md` has YAML front matter"):
        return results

    ok(fm.get("title"), "front matter has a `title`")

    authors = fm.get("authors")
    if ok(isinstance(authors, list) and len(authors) >= 1, "front matter lists at least one author"):
        ok(all(isinstance(a, dict) and a.get("name") for a in authors), "every author has a `name`")
        ok(any(isinstance(a, dict) and a.get("corresponding") for a in authors),
           "one author is marked `corresponding: true`")

    ok(fm.get("abstract"), "front matter has an `abstract`")
    ok(fm.get("keywords"), "front matter has `keywords`")

    at = fm.get("article_type")
    ok(at in ARTICLE_TYPES, f"`article_type` is one of {', '.join(sorted(ARTICLE_TYPES))}"
       if at else "front matter has an `article_type`")

    # Bibliography, if referenced, must exist.
    bib = fm.get("bibliography")
    if bib:
        ok(os.path.isfile(os.path.join(root, bib)), f"bibliography `{bib}` exists")

    # Figures referenced in the body must exist.
    missing = []
    for rel in re.findall(r"!\[[^\]]*\]\(([^)]+)\)", text):
        rel = rel.split()[0].strip()
        if rel.startswith(("http://", "https://")):
            continue
        if not os.path.isfile(os.path.join(root, rel)):
            missing.append(rel)
    ok(not missing, "all referenced figures exist" + (f" (missing: {', '.join(missing)})" if missing else ""))

    # Reproducibility signal: a GeoGebra link, construction commands, or figures.
    has_ggb = bool(fm.get("geogebra"))
    has_fig = bool(re.search(r"!\[[^\]]*\]\(", text))
    has_code = bool(re.search(r"^```", text, re.MULTILINE))
    ok(has_ggb or has_fig or has_code,
       "reproducibility: has a GeoGebra link, figures, or a code/commands block")

    return results


# --------------------------------------------------------------------------
# Commands
# --------------------------------------------------------------------------

def clone(url: str, dest: str) -> None:
    subprocess.run(
        ["git", "clone", "--depth", "1", "--quiet", url, dest],
        check=True, capture_output=True, text=True,
    )


def cmd_check(args) -> str:
    if args.local:
        root, source = args.local, f"local path `{args.local}`"
    else:
        body = open(args.body_file, encoding="utf-8").read() if args.body_file else ""
        fields = parse_issue_form(body)
        url = find_repo_url(fields)
        if not url:
            return (":x: **Check failed.** I couldn't find a manuscript repository URL in the "
                    "submission. It should be a `https://github.com/...` link under "
                    "**Manuscript repository**.")
        tmp = tempfile.mkdtemp(prefix="nagj-check-")
        root, source = os.path.join(tmp, "manuscript"), f"[`{url}`]({url})"
        try:
            clone(url, root)
        except subprocess.CalledProcessError:
            return (f":x: **Check failed.** I couldn't clone {source}. Is the repository public "
                    "and the URL correct?")

    results = check_manuscript(root)
    passed = sum(1 for ok, _ in results if ok)
    total = len(results)
    lines = [f"### `@nagjbot check` — {source}", ""]
    for ok, msg in results:
        lines.append(f"- {':white_check_mark:' if ok else ':x:'} {msg}")
    lines.append("")
    if passed == total:
        lines.append(f"**All {total} checks passed.** Ready for an editor to assign reviewers.")
    else:
        lines.append(f"**{passed}/{total} checks passed.** Please fix the items above and comment "
                     "`@nagjbot check` again.")
    return "\n".join(lines)


def _resolve_url(args) -> str | None:
    if args.local:
        return None
    body = open(args.body_file, encoding="utf-8").read() if args.body_file else ""
    return find_repo_url(parse_issue_form(body))


def cmd_repo_url(args) -> str:
    """Internal: print just the manuscript repo URL, for the workflow to clone."""
    return _resolve_url(args) or ""


def cmd_build(args) -> str:
    url = _resolve_url(args)
    if not url and not args.local:
        return (":x: **Build failed.** I couldn't find a manuscript repository URL in the "
                "submission.")
    where = f"[`{url}`]({url})" if url else f"`{args.local}`"
    return (f"### `@nagjbot build` — {where}\n\n"
            "Building the PDF in the journal's style. The compiled PDF will be attached to this "
            "run as an artifact, linked below when it finishes.")


def cmd_accept(args) -> str:
    url = _resolve_url(args)
    where = f"[`{url}`]({url})" if url else "this submission"
    return (f"### `@nagjbot accept` — {where}\n\n"
            f":white_check_mark: Recorded as **accepted** by @{args.actor}. Building the final PDF; "
            "it will be attached below.\n\n"
            "Next: an editor runs `@nagjbot publish` to open the publication PR against the "
            "website repository.")


def cmd_stub(name: str, note: str):
    def handler(args) -> str:
        return f"### `@nagjbot {name}`\n\n{note}"
    return handler


def cmd_help(_args) -> str:
    return (
        "### `@nagjbot` commands\n\n"
        "- `@nagjbot check` — validate the manuscript linked in this submission\n"
        "- `@nagjbot build` — compile the manuscript PDF in the journal's style\n"
        "- `@nagjbot accept` — _editors only_ — record acceptance and build the final PDF\n"
        "- `@nagjbot help` — show this message\n\n"
        "_On the way: create-review, publish._"
    )


COMMANDS = {
    "check": cmd_check,
    "build": cmd_build,
    "accept": cmd_accept,
    "help": cmd_help,
    "repo-url": cmd_repo_url,
    "create-review": cmd_stub("create-review", "Coming soon: open the review issue and post the reviewer checklist."),
    "publish": cmd_stub("publish", "Coming soon: open the publication PR against the website repository."),
}


def main() -> int:
    parser = argparse.ArgumentParser(description="NAGJ editorial bot command handler.")
    parser.add_argument("command", help="the @nagjbot command")
    parser.add_argument("--body-file", help="file containing the submission issue body")
    parser.add_argument("--actor", help="GitHub username of the commenter (for authorization)")
    parser.add_argument("--local", help="validate a local manuscript directory (testing; skips clone)")
    parser.add_argument("--authz-only", action="store_true",
                        help="exit 0 if the actor may run the command, 1 if not; print nothing")
    args = parser.parse_args()

    # Authorization gate, shared by the report step and the build step.
    allowed = not (args.command in EDITOR_ONLY and not is_editor(args.actor))
    if args.authz_only:
        return 0 if allowed else 1

    handler = COMMANDS.get(args.command)
    if not handler:
        print(f"### `@nagjbot` — unknown command `{args.command}`\n\n"
              f"Try `@nagjbot help`.")
        return 0

    # Privileged commands are editors-only. The workflow already blocks the
    # public; this narrows the write-access team down to the editorial board.
    if not allowed:
        who = f"@{args.actor}" if args.actor else "You"
        print(f":lock: **`@nagjbot {args.command}` is for editors only.** {who} is not on the "
              f"editorial board ([`editors.yml`](../../blob/main/editors.yml)). If this is wrong, "
              f"an editor can add you there.")
        return 0

    print(handler(args))
    return 0


if __name__ == "__main__":
    sys.exit(main())
