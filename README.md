# Leonida Casebook - GTA VI Trophy Guide & Tracker

[![Competition](https://make.fun/badge/gta6-trophy-guide-01.svg)](https://make.fun/c/gta6-trophy-guide-01)
[![Rank](https://make.fun/badge/gta6-trophy-guide-01/xplaynode/makefun-gta6-trophy-guide-01-v4/rank.svg)](https://make.fun/c/gta6-trophy-guide-01)
[![Reward](https://make.fun/badge/gta6-trophy-guide-01/xplaynode/makefun-gta6-trophy-guide-01-v4/reward.svg)](https://make.fun/c/gta6-trophy-guide-01)

An offline, static guide and tracker for all 55 PlayStation 5 trophies of
Grand Theft Auto VI, built for the make.fun gta6-trophy-guide-01 bounty.
Open `app/index.html` from any static server (or `node serve.ts`) - it works
with the network off and loads nothing from outside `app/`.

What is inside:

- **Guide & Tracker (three panes):** the full trophy list with official
  names, descriptions and grades (1 platinum, 2 gold, 6 silver, 46 bronze,
  28 hidden, 1,350 PSN points), filters by kind / grade / status, a search
  box, and a spoiler shield that hides story trophies until they are earned.
  The centre guide gives a short cited answer first, then a missable box,
  a YOUR COUNT counter for every counted trophy, and numbered steps that
  each carry their source citations. The right rail shows NEXT UP in
  roadmap order and the sources behind the open guide, with claim counts.
- **Claim-level audit:** 562 claims, 562/562 cited, 562 backed by 2 or more
  sources; 385 guide steps, 385/385 cited; 28 sources read on 2026-11-21
  (142 pages) with an honest scope note and independence label per source;
  44 disagreements shown both ways, each with an explicit "our call".
- **Roadmap:** every headline claim (hours, difficulty, playthroughs,
  replay, online count, missable count) individually cited, with stage
  hours and a missable watch rail.
- **Missables:** a point-of-no-return chapter-window grid (Ch1-Ch5/Post)
  plus the story gates in chapter order. One trophy is reported possibly
  missable: Positive Mental Attitude, whose first meditation is a
  Chapter 1-only scene at Jason's house.
- **Sources & Save:** progress is kept in localStorage and can be exported
  to `leonida-casebook-save.json` and imported back, with a saved-state
  panel, the real exported save JSON, by-grade and by-kind progress bars,
  the full source registry and the disagreements register.

All guide wording is original to this entry; facts are cited to the
numbered sources rather than copied from them. Trophy names and
descriptions are shown as PlayStation publishes them. No Rockstar logos
or artwork are used. `TOURNAMENT.md` records the 24 candidate angles and
the pairwise tournament that selected this design. `build_data.py` is the
data builder that produced `app/data/trophies.json` and
`app/data/guide.json` from the official list and the source registry.
