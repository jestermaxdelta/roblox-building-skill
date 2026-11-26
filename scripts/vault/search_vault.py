#!/usr/bin/env python3
"""Search the Roblox Game Dev Playbook.

Usage (from the playbook folder or anywhere):
    python "99 Meta/search_vault.py" "phone hud too cluttered"
    python "99 Meta/search_vault.py" "datastore session lock" -n 15
    python "99 Meta/search_vault.py" "pet hatching odds" --tag topic/monetization

Ranks notes by matches in title, aliases, tags, headings and summary (from
vault-index.json), plus full-text hits, and prints the path and the headings
that match. Standard library only.
"""
import argparse, json, re, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
WEIGHTS = {"title": 6.0, "aliases": 4.0, "triggers": 6.0, "tags": 3.0, "headings": 2.0, "summary": 2.0}
STOP = set("a an and are as at be by for from how i in is it my of on or the to what with why do does my me game games roblox".split())


def tokens(s):
    return [t for t in re.findall(r"[a-z0-9+]+", s.lower()) if t not in STOP]


def stem(t):
    if len(t) <= 3:
        return t
    if t.endswith("ies"):
        t = t[:-3] + "y"
    elif t.endswith(("sses", "xes", "ches", "shes")):
        t = t[:-2]
    elif t.endswith("s") and not t.endswith("ss"):
        t = t[:-1]
    for suf in ("ing", "ed"):
        if len(t) > len(suf) + 3 and t.endswith(suf):
            return t[: -len(suf)]
    return t


def main():
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
    ap = argparse.ArgumentParser()
    ap.add_argument("query")
    ap.add_argument("-n", type=int, default=10)
    ap.add_argument("--tag", help="only notes with this tag, e.g. topic/ui or type/genre")
    ap.add_argument("--no-archive", action="store_true", help="skip the 90 Archive notes")
    a = ap.parse_args()

    idx = json.loads((HERE / "vault-index.json").read_text(encoding="utf-8"))
    q = [stem(t) for t in tokens(a.query)]
    if not q:
        sys.exit("empty query")
    phrase = a.query.lower().strip()
    results = []
    for n in idx["notes"]:
        if a.tag and a.tag not in n["tags"]:
            continue
        if a.no_archive and n["folder"].startswith("90"):
            continue
        fields = {"title": n["title"], "aliases": " ".join(n["aliases"]), "tags": " ".join(n["tags"]),
                  "headings": " ".join(n["headings"]), "summary": n["summary"], "triggers": n.get("triggers", "")}
        score = 0.0
        for f, text in fields.items():
            toks = {stem(t) for t in tokens(text)}
            score += WEIGHTS[f] * sum(1 for t in q if t in toks)
            if len(q) > 1 and phrase in text.lower():
                score += WEIGHTS[f] * 2
        try:
            body = (ROOT / n["path"]).read_text(encoding="utf-8").lower()
        except OSError:
            body = ""
        hits = sum(min(body.count(t), 20) for t in q)
        covered = sum(1 for t in q if t in body)
        score += 0.15 * hits + 1.5 * covered
        if len(q) > 1 and phrase in body:
            score += 4
        if n["folder"].startswith("90"):
            score *= 0.6  # archive ranks below the guides
        if score > 0:
            heads = [h for h in n["headings"] if any(t in {stem(x) for x in tokens(h)} for t in q)][:4]
            results.append((score, n, heads))
    results.sort(key=lambda r: -r[0])
    for score, n, heads in results[: a.n]:
        print(f"{score:6.1f}  {n['path']}")
        if n["summary"]:
            print(f"        {n['summary'][:160]}")
        for h in heads:
            print(f"        # {h}")
    for im in idx.get("images", []):
        if all(t in {stem(x) for x in tokens(im["title"])} for t in q[:2]):
            print(f"   img  {im['file']}")
    if not results:
        print("no matches; try fewer or different words, or open '00 Start Here/Task Router.md'")


if __name__ == "__main__":
    main()
