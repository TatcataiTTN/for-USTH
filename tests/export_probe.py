"""Writes tests/probe_questions.json: the stems (English and Vietnamese, with the options) of every Moodle review item, for the analyser's held-out test.
These questions were never used to mine keywords, so the test measures how well the keyword system generalises to new wording."""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path[:0] = [os.path.join(HERE, "..", "build")]
import moodle_pages
out = []
for course in moodle_pages.COURSE_SETS:
    for sid, items in moodle_pages.load_items(course).items():
        for it in items:
            opts = " ".join("(%s) %s" % ("abcd"[i], c) for i, c in enumerate(it.choices or []))
            out.append(dict(id=it.id, course=course, en=it.q[0] + " " + opts, vi=it.q[1] + " " + opts))
json.dump(out, open(os.path.join(HERE, "probe_questions.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=0)
print(len(out), "probe questions")
