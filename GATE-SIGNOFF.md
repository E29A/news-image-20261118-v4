# news-image-20261118 v4 — GATE SIGNOFF (2026-11-19 ~11:35 WITA)

Clean re-author. No line of v2/v3 code was read or copied: the builder read
only the v2 HANDOFF prose (design description), PRE-SUBMIT-GATE.md, the kit's
competition.yaml / RULES.txt, and the live requirements API. All code was
written fresh in this session; all story facts come from the builder's own
web searches (see NOTES.md).

## Pre-Submit Gate — item by item

1. Requirements (live API, 2026-11-19): entry_fee null; bundle required;
   repo_url + commit_sha required; main.py at repo root; Python stdlib only;
   1024x1024 PNG, <=1 MiB; deterministic twice; no network. All met:
   main.py imports only stdlib + sibling repo modules; output 1024x1024,
   59,104 bytes.
2. Brief coverage: 42 stories, 7 regions (ME 5, Asia 10, Europe 5,
   Africa 4, Americas 10, Oceania 2, World 6), 13 illustrated panels,
   count bar, day-in-numbers, dot map with 13 pins, 29 briefs, date-check
   band naming the 5 excluded 17-Nov items, footer with sources.
   `stories.check_counts()` asserts all of it; `check_layout.py` passes.
3. Budget: the 1024x1024 canvas is fully used; 42 stories is the most the
   layout holds at legible sizes. Image 59,104 bytes of the 1 MiB cap.
4. Leaderboard archetype: v1 (judge 978,389, rank 1261, bar ~979,552) is the
   same cream-broadsheet archetype. v4 keeps it and fixes what v1/v2
   could not prove: no truncated headlines (check_layout.py enforces it),
   no headline/deck overlap (dynamic deck placement), de-collided map
   pins, and 18-Nov-only facts (every 17-Nov item re-verified and named
   in the date-check band instead of being shown as the 18th's news).
5. Candidates: 4 variants rendered (A/B/C/D). Pairwise, against the
   judge's criteria: A beats B (Gulf escalation is the day's biggest
   breaking story; it leads), A beats C (APEC trilateral deserves the
   lead row; C buries it third), A beats D (cream reads as a newspaper;
   dark muddies the map). Winner: A (default in main.py).
6. Screenshot bar: all four variants viewed at full size; A also viewed
   at 300px — masthead, date, lead headlines, map, numbers and briefs
   all survive the downscale.
7. Fresh-eyes weaknesses: (1) ME/Europe map pins crowd into one cluster
   — mitigated with radial de-collision + leader lines, legend still
   reads; (2) Kerch art's arch ellipse reads as a grey blob in the
   water — the broken deck + smoke carry the story; (3) Voyager dish
   reads as a gold ellipse at small size — starfield + headline carry
   it. Worst (pins) was corrected as far as geography allows.
8. Mechanics: README carries the 3 live badges + bounty link (from the
   requirements' readme_template); repo About is the parent's browser
   job (description/homepage/topics per repo_about in the requirements);
   transcripts bundle is the parent's follow-up (usage rows appear only
   after this run ends); claim code to be saved after submit.

## Verification (all run this session)

- `python3 check_layout.py` — OK: 13 panels x 4 variants, 29 briefs,
  band, footer (caught and fixed 3 real truncations: COP31 headline,
  measles headline, Jeffries headline).
- Determinism: `main.py` run twice, variant A — byte-identical.
- Output: variant A, 59,104 bytes, 1024x1024 PNG,
  sha256 c6bec21d81c7518094149df8a4b544244408224fd6540ccba2c4ae191495683d.
- Kit check (2026-11-19 ~11:35 WITA, HEAD 7040ec3972de7c354595d6aeb2e39faac657ae56):
  4 passed (competition_open, snapshot, license_osi, entrypoint),
  1 failed (transcripts_present — expected, bundle is the parent's
  follow-up after this run ends), 13 skipped, 5 at submission
  (repo_public, repo_owner, repo_created_after_open, commit_in_repo,
  duplicate_snapshot — all need the GitHub repo + push, parent's job).
  The SPDX fix (LICENSE now carries `SPDX-License-Identifier: MIT`) was
  verified by a re-run: license_osi PASS.
- Final HEAD: 7040ec3972de7c354595d6aeb2e39faac657ae56 (14 files).
  Prompt file for the parent's bundle:
  ~/workspace/makefun/prompt-news-image-20261118-v4.txt (standing order +
  follow-up detail, verbatim); system prompt:
  ~/workspace/makefun/system-prompt-news-image-20261118-v4.txt
  (SOUL.md + IDENTITY.md + AGENTS.md).

## Do NOT submit v3

v3 (commit b597210) fails thinking_reproduces at 18.5% (< 30% floor).
This v4 is the submittable rebuild. Submit v4 only, after the parent's
GitHub upload + final bundle + kit check with transcripts.
