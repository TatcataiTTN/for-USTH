# -*- coding: utf-8 -*-
"""Build the JSON data of both courses: question banks, quiz sets (3 per chapter), midterm sets (3 per course),
sprint sets (30 questions / 20 minutes), past papers and source notes."""
import json, os, random, sys
from collections import Counter, defaultdict
import qlib

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

def jsonable(o):
    """Plain-JSON version of nested data (sympy integers -> int, rationals -> 'p/q' strings the JS lab can parse)."""
    import sympy as sp
    if isinstance(o, dict):
        return {k: jsonable(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)):
        return [jsonable(v) for v in o]
    if isinstance(o, sp.Integer):
        return int(o)
    if isinstance(o, sp.Rational):
        return "%d/%d" % (o.p, o.q)
    if isinstance(o, sp.Basic):
        return str(o)
    return o

CAL_CHAPTERS = [
    ("c1", "Functions, limits and continuity", "Lectures 1–3 · Tutorials 1–3"),
    ("c2", "Derivatives", "Lectures 3–4 · Tutorials 3–4"),
    ("c3", "Applications of derivatives and antiderivatives", "Lectures 5–6 · Tutorials 5–6"),
    ("c4", "Definite integrals and their applications", "Lectures 7–8 · Tutorials 7–8"),
    ("c5", "Techniques of integration and improper integrals", "Lectures 9–10a · Tutorials 9–10"),
    ("c6", "Sequences, series, power series and Taylor series", "Lectures 10b–12 · Tutorials 11–12"),
]
LA_CHAPTERS = [
    ("c1", "Systems of linear equations", "Lecture 1 · Exercise Sheet 1 · Elementary Linear Algebra ch. 1"),
    ("c2", "Matrices", "Lecture 2 · Exercise Sheet 2 · Elementary Linear Algebra ch. 2"),
    ("c3", "Determinants", "Lecture 3 · Exercise Sheet 3 · Elementary Linear Algebra ch. 3"),
    ("c4", "Vector spaces", "Lecture 4 · Exercise Sheet 4 · Elementary Linear Algebra ch. 4"),
    ("c5", "Inner product spaces", "Lecture 5 · Exercise Sheet 5 · Elementary Linear Algebra ch. 5"),
    ("c6", "Linear transformations", "Lecture 6 · Exercise Sheet 6 · Elementary Linear Algebra ch. 6"),
    ("c7", "Eigenvalues and eigenvectors", "Lecture 7 · Exercise Sheet 7 · Elementary Linear Algebra ch. 7"),
]

def stratified_sets(items, n_sets, size, rng, avoid=()):
    """Disjoint sets, interleaving topics so each set is diverse; mixes levels."""
    pool = [i for i in items if i["id"] not in avoid]
    rng.shuffle(pool)
    by_topic = defaultdict(list)
    for it in pool:
        by_topic[it["topic"]].append(it)
    topics = list(by_topic)
    rng.shuffle(topics)
    order = []
    while any(by_topic[t] for t in topics):
        for t in topics:
            if by_topic[t]:
                order.append(by_topic[t].pop())
    sets = [[] for _ in range(n_sets)]
    k = 0
    for it in order:
        # place in the set with the fewest items that still needs more
        cand = [s for s in sets if len(s) < size]
        if not cand:
            break
        s = min(cand, key=lambda z: (len(z), sum(1 for q in z if q["level"] == it["level"])))
        s.append(it)
    return [[q["id"] for q in s] for s in sets]

def pick_balanced(by_ch, quotas, rng, used, size):
    chosen = []
    for ch, q in quotas.items():
        pool = [i for i in by_ch[ch] if i["id"] not in used]
        rng.shuffle(pool)
        # prefer a mix of levels 1,2,3
        pool.sort(key=lambda z: z["level"] if rng.random() < .0 else rng.random())
        chosen += pool[:q]
    ids = [c["id"] for c in chosen]
    rng.shuffle(ids)
    return ids[:size]

def build_course(slug, B, chapters, midterm_quota, midterm_title, seed, mid_min=50, sprint_quota=None):
    rng = random.Random(seed)
    items = [i for i in B.items if "extension" not in i.get("tags", [])]
    by_ch = defaultdict(list)
    for it in items:
        by_ch[it["ch"]].append(it)
    sets = {"chapter": {}, "midterm": [], "sprint": []}
    used_chapter = set()
    for ch, title, _ in chapters:
        trio = stratified_sets(by_ch[ch], 3, 12, rng)
        sets["chapter"][ch] = [dict(id=f"{ch}-{'ABC'[i]}", title=f"{title} · Set {'ABC'[i]}", ids=ids) for i, ids in enumerate(trio)]
    used = set()
    for i in range(3):
        ids = pick_balanced(by_ch, midterm_quota, rng, used, sum(midterm_quota.values()))
        used.update(ids)
        sets["midterm"].append(dict(id=f"midterm-{'ABC'[i]}", title=f"{midterm_title} · Mock {'ABC'[i]}", ids=ids, minutes=mid_min, forward_only=True))
    spq = sprint_quota
    used = set()
    for i in range(3):
        ids = pick_balanced(by_ch, spq, rng, used, sum(spq.values()))
        used.update(ids)
        sets["sprint"].append(dict(id=f"sprint-{'ABC'[i]}", title=f"Speed exam · 30 questions in 20 minutes · Mock {'ABC'[i]}", ids=ids, minutes=20, forward_only=False))
    return sets

def write_course(slug, B, extra, chapters, sets, meta_extra):
    d = os.path.join(ROOT, slug, "data")
    os.makedirs(d, exist_ok=True)
    n, e = B.dump(os.path.join(d, "bank.json"))
    meta = dict(course=slug, chapters=[dict(id=c, title=t, src=s) for c, t, s in chapters], sets=sets, counts=Counter(i["ch"] for i in B.items))
    meta.update(meta_extra)
    json.dump(meta, open(os.path.join(d, "meta.json"), "w", encoding="utf-8"), ensure_ascii=False, separators=(",", ":"))
    for name, obj in extra.items():
        json.dump(jsonable(obj), open(os.path.join(d, name), "w", encoding="utf-8"), ensure_ascii=False, separators=(",", ":"))
    return n

def main():
    import gen_cal, gen_la
    from la_papers import build_papers
    qlib.NOTES.clear()
    BC = gen_cal.build(); rc = BC.finalize()
    BL = gen_la.build(); rl = BL.finalize()
    print("CAL", rc); print("LA ", rl)
    # Calculus: midterm = chapters 1-3 (20 questions / 50 min, forward only); sprint = 30 questions across 6 chapters
    sc = build_course("Calculus-1", BC, CAL_CHAPTERS, {"c1": 7, "c2": 7, "c3": 6}, "Calculus I Midterm (Ch. 1–3, 20 questions, 50 min, no going back)", 11,
                      sprint_quota={"c1": 5, "c2": 5, "c3": 5, "c4": 5, "c5": 5, "c6": 5})
    # Linear Algebra: midterm assumed to cover chapters 1-4 (the course page does not state it)
    sl = build_course("Linear-Algebra", BL, LA_CHAPTERS, {"c1": 5, "c2": 5, "c3": 5, "c4": 5}, "Linear Algebra Midterm (Ch. 1–4, 20 questions, 50 min)", 12,
                      sprint_quota={"c1": 4, "c2": 4, "c3": 4, "c4": 5, "c5": 4, "c6": 4, "c7": 5})
    # Calculus notes (document errors found) and LA notes are shared in qlib.NOTES (filled while generating)
    notes_all = [dict(src=a, note=b) for a, b in qlib.NOTES]
    cal_extra = dict(midterm_quota={"c1": 7, "c2": 7, "c3": 6}, midterm_minutes=50, midterm_title="Calculus I Midterm (Ch. 1–3, 20 questions, 50 min, no going back)",
                     sprint_quota={"c1": 5, "c2": 5, "c3": 5, "c4": 5, "c5": 5, "c6": 5})
    la_extra = dict(midterm_quota={"c1": 5, "c2": 5, "c3": 5, "c4": 5}, midterm_minutes=50, midterm_title="Linear Algebra Midterm (Ch. 1–4, 20 questions, 50 min)",
                    sprint_quota={"c1": 4, "c2": 4, "c3": 4, "c4": 5, "c5": 4, "c6": 4, "c7": 5})
    n1 = write_course("Calculus-1", BC, {"notes.json": [n for n in notes_all if n["src"].startswith(("Tutorial", "Computation", "Mock Test"))]}, CAL_CHAPTERS, sc, cal_extra)
    papers = build_papers()
    n2 = write_course("Linear-Algebra", BL, {"papers.json": papers, "notes.json": [n for n in notes_all if n["src"].startswith(("Exercise", "Final"))]}, LA_CHAPTERS, sl, la_extra)
    print("written", n1, "Calculus questions;", n2, "Linear Algebra questions;", len(papers), "past papers;", len(notes_all), "document notes")
    for slug, sets in (("Calculus-1", sc), ("Linear-Algebra", sl)):
        print(slug, "chapter sets:", sum(len(v) for v in sets["chapter"].values()), "midterm:", [len(s["ids"]) for s in sets["midterm"]], "sprint:", [len(s["ids"]) for s in sets["sprint"]])

if __name__ == "__main__":
    main()
