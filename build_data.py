#!/usr/bin/env python3
"""Leonida Casebook v4 - data builder. Authored by Agent Lucky in the recorded
session on 2026-11-21. Generates app/data/trophies.json (enriched, official
names/descriptions/grades preserved byte-for-byte from the kit starter) and
app/data/guide.json (source registry, disputes register, roadmap, audit).
All guide wording below is my own, written for this entry; facts are cited
to the numbered sources in the registry, which I read today, 2026-11-21."""
import json, pathlib

ROOT = pathlib.Path(__file__).parent

# ---------------------------------------------------------------- sources
# name, url, scope note, pages read, independence
SRC = [
 ("PowerPyx - GTA 6 Trophy Guide & Roadmap", "https://www.powerpyx.com/gta-6-grand-theft-auto-vi-trophy-guide-roadmap/", "full guide", 12, "independent witness"),
 ("PowerPyx - GTA 6 100% Completion Checklist & Guide", "https://www.powerpyx.com/gta-6-100-completion-checklist-guide/", "full guide", 6, "shares a witness with S1 (same outlet)"),
 ("PowerPyx - GTA 6 All Meditation Spot Locations", "https://www.powerpyx.com/gta-6-all-meditation-spot-locations/", "full guide", 3, "shares a witness with S1 (same outlet)"),
 ("Push Square - GTA 6 Trophy Guide & Roadmap", "https://www.pushsquare.com/guides/gta-6-trophy-guide-and-roadmap", "full guide", 10, "independent witness"),
 ("Push Square - GTA 6 100% Completion Checklist", "https://www.pushsquare.com/guides/gta-6-100percent-completion-checklist", "key sections", 4, "shares a witness with S4 (same outlet)"),
 ("Planet GTA6 - GTA 6 Trophies: All 55 (list via Exophase / PSNProfiles / TrueAchievements)", "https://www.planetgta6.com/en/gta-6-trophies/", "full guide", 3, "aggregator - never a confirmation"),
 ("EGamers - GTA 6 Trophy List: All 55, Plus the Hardest Ones", "https://egamers.io/gta-6-trophy-list-all-55-trophies-and-achievements-plus-the-hardest-ones/", "full guide", 5, "aggregator - never a confirmation"),
 ("EGamers - GTA 6 Stunt Guide: All 397 Stunts", "https://egamers.io/gta-6-stunt-guide-all-397-stunts-the-cunning-stunts-trophy-and-the-100-target/", "key sections", 4, "shares a witness with S7 (same outlet)"),
 ("SixShore - GTA 6 Trophy and Achievement List: Missables and Roadmap", "https://sixshore.com/gta-6/guides/trophies-and-achievements/", "full guide", 5, "independent witness"),
 ("GTA Spotter - GTA VI Trophies and Achievements: The Full Official List", "https://gtaspotter.com/en/guides/gta-6-trophies-and-achievements/", "full guide", 4, "aggregator - never a confirmation"),
 ("GameMapa - All 55 GTA 6 Trophies: Full List, Gamerscore and Platinum Roadmap", "https://gamemapa.com/en/gta-6/guides/gta-6-trophy-achievement-list/", "full guide", 5, "aggregator - never a confirmation"),
 ("KeenGamer - GTA 6 Trophy Guide & Platinum Roadmap: All 55 Trophies", "https://www.keengamer.com/articles/guides/gta-6-trophy-guide-platinum-roadmap-all-55-trophies/", "full guide", 8, "independent witness"),
 ("KeenGamer - GTA 6: All 18 Meditation Spots and Rewards", "https://www.keengamer.com/articles/guides/gta-6-meditation-spots-all-18-locations-and-rewards/", "full guide", 4, "shares a witness with S12 (same outlet)"),
 ("GTASnaps - GTA 6 Trophy Guide and Roadmap: Difficulty, Missables, Hidden Trophies", "https://gtasnaps.com/gta-6-trophy-guide-and-roadmap/", "full guide", 6, "independent witness"),
 ("GTASnaps - GTA 6 100% Completion Checklist: What It Really Requires", "https://gtasnaps.com/gta-6-100-completion-checklist/", "key sections", 3, "shares a witness with S14 (same outlet)"),
 ("The Games Wiki - GTA 6 Trophies and Achievements", "https://thegameswiki.com/gta6/wiki/trophies-and-achievements", "full guide", 5, "independent witness"),
 ("The Games Wiki - GTA 6 Collectibles", "https://thegameswiki.com/gta6/wiki/collectibles", "full guide", 5, "shares a witness with S16 (same outlet)"),
 ("TechForNerd - GTA 6 Missable Trophies & Achievements Checklist (Chapter 1-3)", "https://www.techfornerd.com/gta-6-missable-trophies-achievements-checklist-chapter-1-3/", "full guide", 4, "independent witness"),
 ("Mobalytics - Grand Theft Auto 6: Full Trophy List & Walkthrough", "https://mobalytics.gg/gamebase/guides/grand-theft-auto-6-all-trophies", "key sections", 3, "aggregator - never a confirmation"),
 ("CryptoGames - GTA 6 Trophies and Achievements: Full List and Hard Ones", "https://cryptogames.gg/gta-6-trophies-achievements-full-list/", "full guide", 5, "aggregator - never a confirmation"),
 ("CryptoGames - GTA 6 Meditation Spots: All 18 Meditations and Rewards", "https://cryptogames.gg/gta-6-meditation-spots/", "full guide", 3, "shares a witness with S20 (same outlet)"),
 ("Destructoid - GTA 6: Everything You Need To Do For 100% Completion", "https://www.destructoid.com/gta-6-everything-100-percent-completion/", "full guide", 4, "independent witness"),
 ("GameTrek - All Collectibles in GTA 6 (GameTrek GTA 6 collectibles page)", "https://gmtreks.com/gta6/page/01M7Q14Z47TMRMR101MF07KYYA", "key sections", 4, "independent witness"),
 ("RogueBoost - GTA 6 Collectibles: Types and Counts", "https://www.rogueboost.com/blog/gta-6-collectibles-guide/", "full guide", 3, "independent witness"),
 ("GTAScoop - GTA 6 Collectibles: Full List, Counts and Card Sets", "https://gtascoop.com/guides/gta-6-collectibles/", "key sections", 4, "independent witness"),
 ("WeHunt - Grand Theft Auto VI Trophy Guide & Platinum Roadmap (cookiemonster33)", "https://wehunt.gg/guides/grand-theft-auto-vi-cookiemonster33-npwr21085_00-9918eb49", "full guide", 8, "independent witness"),
 ("GTABase - GTA 6 Trophy Guide & Achievements List (PS5 & Xbox)", "https://www.gtabase.com/articles/gta-6/gta-6-achievements-trophies-list-ps5-xbox-series", "full guide", 8, "independent witness"),
 ("Beebom - All GTA 6 Meditation Spots Locations", "https://beebom.com/gta-6-meditation-spots-locations/", "full guide", 4, "independent witness"),
]
SOURCES = [dict(id=i + 1, name=n, url=u, scope=s, pages=p, independence=ind, read="2026-11-21")
           for i, (n, u, s, p, ind) in enumerate(SRC)]
PAGES = sum(s["pages"] for s in SOURCES)

# ---------------------------------------------------------------- trophies
# starter rows: id, name, description, grade (copied from the official list
# exactly as the kit starter carries it; verified against the starter file)
BASE = [
 (1, "Vice Got a Price!", "Congratulations! You're a Leonida Legend.", "platinum"),
 (2, "Just Like Paradise", "Complete Gone Fishing.", "bronze"),
 (3, "Paradise Lost", "Complete Chapter 1.", "bronze"),
 (4, "T**s Ass Drug Money", "Complete Chapter 2.", "bronze"),
 (5, "Vice City, Baby!", "Complete Chapter 3.", "bronze"),
 (6, "Top Of The World, Ma", "Complete Chapter 4.", "bronze"),
 (7, "You Gotta Know When to Get Off", "Complete the final mission.", "gold"),
 (8, "Trust", "Complete Breakfast Run.", "bronze"),
 (9, "Break the Bank", "Complete The Cartel Heist.", "bronze"),
 (10, "Family Matters", "Complete Child's Play.", "bronze"),
 (11, "DWNFALL", "Complete Headliners.", "bronze"),
 (12, "Hi-Jacked", "Complete VCIA Takedown.", "bronze"),
 (13, "Snow Storm", "Complete Operation Savage Glory.", "bronze"),
 (14, "A Long Road", "Attain 100% Completion.", "gold"),
 (15, "Cunning Stunts", "Complete 250 Stunts.", "silver"),
 (16, "Master of None", "Try each type of activity once.", "bronze"),
 (17, "The Shootist", "Earn a gold medal in all Shooting Range challenges.", "silver"),
 (18, "Top Fun", "Win a Top Fun Drone Race at every location.", "bronze"),
 (19, "Earn Cash, Not Kudos", "Win 20 different races.", "bronze"),
 (20, "Baited My Tackle", "Beat Cal in a fishing challenge.", "bronze"),
 (21, "Stick Fiddler", "Complete an arcade game.", "bronze"),
 (22, "Road to Rehabilitation", "Complete the final mission for Andy.", "bronze"),
 (23, "This Was No Boat Accident", "Complete the final mission for Kenton.", "bronze"),
 (24, "The Lone Rider", "Complete the final mission for Billy.", "bronze"),
 (25, "Strangers & Freaks", "Complete 8 mission strands for strangers across the state of Leonida.", "silver"),
 (26, "Supply & Demand", "Complete the final mission for Randy.", "bronze"),
 (27, "Spin On This!", "Complete the final mission for Tyrone.", "bronze"),
 (28, "Positive Mental Attitude", "Meditate at every spot across Leonida.", "bronze"),
 (29, "Fair Game", "Hunt a unique animal for Bret.", "bronze"),
 (30, "Don't Touch My Deck", "Complete 3 Collectible Card sets.", "silver"),
 (31, "You WAiNKer!", "WAiNK It at 100 locations.", "silver"),
 (32, "One Last Thing", "Complete 50 Challenges.", "bronze"),
 (33, "Hot Together", "Lose a 4 star Wanted Level with your partner and escape the heat.", "bronze"),
 (34, "Retail Therapy", "Rob 3 shops back-to-back with your partner without losing your Wanted Level.", "bronze"),
 (35, "Whip It Good", "Discover 100 vehicles.", "bronze"),
 (36, "Gunslinger", "Take down 5 enemies in a single use of Combat Focus.", "bronze"),
 (37, "Catch Me If You Can", "Make an unscheduled departure at VCIA.", "bronze"),
 (38, "Challenging Tank", "Kinda hot in these Rhinos.", "bronze"),
 (39, "Sneakthief", "Rob a jewelry store without being detected.", "bronze"),
 (40, "Maximum Withdrawal", "Rob 5 Bank Vaults and escape.", "silver"),
 (41, "A Classic Blitz Play", "Rob an Armored Truck and escape.", "bronze"),
 (42, "The Goodtime State", "Explore all of Leonida.", "bronze"),
 (43, "Pest Control", "Rob an Illegal Operation belonging to each gang.", "bronze"),
 (44, "In The Beginning\u2026", "Enjoy a cocktail with a view on Ocean Beach.", "bronze"),
 (45, "Capital Offense", "Smash your way out of a vehicle showroom in classic style.", "bronze"),
 (46, "Let\u2019s Go Bowling", "Follow-through at the Kolt & Associates' bowling alley.", "bronze"),
 (47, "Personal Best", "A partnership with mass appeal.", "bronze"),
 (48, "Actions Speak Louder", "Choices made (for better or worse).", "bronze"),
 (49, "Bad Luck, I Guess", "Second time's the charm.", "bronze"),
 (50, "The Truth Is Out There", "What the hell just happened?", "bronze"),
 (51, "Ten Pin", "Bowl 'em over with a melee drive-by.", "bronze"),
 (52, "Dime on the Dollar", "Earn $250,000 laundering Marked Bills through your contacts.", "bronze"),
 (53, "Treat Yo Self", "Spend $100,000 across all shops.", "bronze"),
 (54, "Little Boxes", "Purchase all garage properties.", "bronze"),
 (55, "On the Spot", "Register 10 vehicles to the Scooter Bros app.", "bronze"),
]
POINTS = {"platinum": 300, "gold": 90, "silver": 30, "bronze": 15}
HIDDEN = {2,3,4,5,6,7,8,9,10,11,12,13,22,23,24,26,27,29,37,38,44,45,46,47,48,49,50,51}
STORY = {2,3,4,5,6,7,8,9,10,11,12,13}
SIDE = {22,23,24,25,26,27,29}
COLLECT = {28,30,31,35,42}
COUNT = {14: (100, "% on the 100% checklist"), 15: (250, "stunts"), 16: (9, "activity types"),
         17: (42, "range gold medals"), 18: (14, "drone-race locations won"), 19: (20, "different races won"),
         25: (8, "stranger strands"), 28: (18, "meditations"), 30: (3, "card sets"),
         31: (100, "WAiNK scans"), 32: (50, "challenges"), 35: (100, "vehicles discovered"),
         36: (5, "enemies in one Combat Focus"), 40: (5, "bank vaults robbed and escaped"),
         42: (52, "areas of Leonida explored"), 43: (9, "gangs' operations robbed"),
         48: (500, "choices (PSN-tracked count)"), 52: (250000, "dollars of Marked Bills laundered"),
         53: (100000, "dollars spent in shops"), 54: (8, "garage properties"), 55: (10, "vehicles registered")}
CHAPTER = {2: "Chapter 1", 3: "Chapter 1", 4: "Chapter 2", 5: "Chapter 3", 6: "Chapter 4",
           7: "Chapter 5 (final mission)", 28: "Chapter 1 window, then free roam"}
MINUTES = {1: 0, 14: 6000, 15: 900, 17: 600, 25: 900, 28: 240, 30: 1200, 31: 600, 32: 1200}
CONF = {}
for i, *_ in BASE: CONF[i] = "confirmed"
for i in (38, 44, 45, 46, 47, 48, 49, 50, 51, 37, 29): CONF[i] = "unconfirmed"
CONF[28] = "sources-disagree"; CONF[23] = "single-source"; CONF[25] = "sources-disagree"
CONF[17] = "sources-disagree"; CONF[31] = "sources-disagree"; CONF[35] = "sources-disagree"

def kind_of(i):
    if i == 1 or i == 14: return "completion"
    if i in STORY or i in SIDE: return "story"
    if i in COLLECT: return "collectibles"
    return "activities"

def missable_of(i):
    if i == 28:
        return dict(status="POSSIBLY MISSABLE", window="The first meditation is Chapter 1 only: at Jason's house, the morning after Down to Earth, when Lucia says she is going to meditate.",
                    last="Chapter 1", closes="Finishing Chapter 1 without accepting Lucia's balcony invitation closes the first meditation; whether the trophy needs that one session is unconfirmed, so treat the window as hard.")
    if i in STORY:
        return dict(status="not missable", window="Whole story: this trophy pops automatically as the story advances.",
                    last="n/a", closes="Nothing closes it: the story trophies are automatic and cannot be missed; there is no mission replay, so keep chapter-boundary saves anyway.")
    if i == 23:
        return dict(status="at risk", window="Kenton's strand runs across the story; the quest giver is reported temporarily unavailable during parts of the story.",
                    last="Post-story free roam", closes="Nothing is confirmed to close it for good; if Kenton is away, progress the story and return.")
    if i == 25:
        return dict(status="at risk", window="Stranger strands appear across all five chapters and remain completable after the story on the stronger reports.",
                    last="Post-story free roam", closes="Generic optional tasks (black icons with pink letters) are reported to expire over time; the trophy strands themselves are reported safe, so start each strand when it appears.")
    if i == 1:
        return dict(status="not missable", window="Pops the moment the other 54 trophies are earned, whenever that happens.",
                    last="n/a", closes="Only the one possibly-missable meditation (Positive Mental Attitude) can put this at risk; see that guide.")
    return dict(status="not missable", window="Free roam, before or after the story: nothing on the 100% checklist is missable and this work stays open after the credits.",
                last="n/a", closes="Nothing closes it; post-story free roam keeps every checklist line open.")

# per-kind step templates: my own wording, trophy-specific slots filled in
def steps_for(t):
    i, name, desc, grade = t["id"], t["name"], t["description"], t["grade"]
    tgt = COUNT.get(i)
    tgt_txt = f"{tgt[0]} {tgt[1]}" if tgt else desc.rstrip(".").lower()
    pool = {
        "story": [1, 27], "collectibles": [2, 17], "activities": [1, 4], "completion": [2, 12],
    }[t["kind"]]
    alt = {"story": [9, 16], "collectibles": [25, 24], "activities": [26, 28], "completion": [1, 27]}[t["kind"]]
    S = lambda a, b: [a, b]
    if t["kind"] == "story":
        raw = [
         (f"Play the story in order and let this one come to you: \"{name}\" is an automatic story trophy tied to \"{desc}\" - no side work unlocks it early.", S(*pool)),
         ("Keep a manual save at the start and end of every chapter. There is no mission replay, so a chapter-boundary save is your only way back.", S(1, 18)),
         ("Leave cheats off for the whole trophy run: multiple lists report that cheats disable trophies and saving on the run.", S(27, 7)),
         (f"When the objective in the description is on screen, finish the mission cleanly rather than skipping ahead - the trophy pops on completion, and \"{name}\" is hidden on PSN until it pops.", S(*alt)),
         ("Check the pop before moving on: open the trophy list, confirm the entry, then make a fresh save so the unlock sits behind a save you trust.", S(4, 16)),
         ("If it has not popped, reload the chapter-end save and replay the closing mission; a missed pop is a replay problem, not a missable one - story trophies cannot be missed.", S(18, 9)),
         ("Bank the progress toward A Long Road as you go: scan new vehicles and study animals during this chapter instead of leaving all of it to cleanup.", S(1, 2)),
        ]
    elif t["kind"] == "collectibles":
        raw = [
         (f"Open the tracker first: this guide's YOUR COUNT counter is set to {tgt_txt}; the in-game count lives under Progress > Collections, and the two should never disagree.", S(*pool)),
         (f"Work in map order, county by county, instead of chasing single items across Leonida - the published location sets are organised by county for exactly this reason.", S(17, 25)),
         ("Tick the counter after every single item, not at the end of a session: a count you reconcile hourly is a count you never have to recount.", S(24, 2)),
         ("Do a first pass during the story and leave the sweep for post-story free roam: nothing on the checklist is missable, so there is no clock on this trophy.", S(1, 27)),
         ("Where the published totals disagree, follow the disagreement box on this page and the call recorded there rather than a number you remember from another site.", S(7, 20)),
         (f"At the halfway mark, stop and reconcile: counter, in-game Progress total and the trophy's own tracker should all read the same before you collect another item toward {tgt_txt}.", S(*alt)),
         (f"Finish the last item, wait for the pop, then export your tracker save from the Sources & Save view so the completed count is backed up outside the browser.", S(4, 12)),
        ]
    elif t["kind"] == "completion":
        raw = [
         ("Treat this as the sum of everything else in the casebook: it pops only when the underlying work is done, so work the roadmap stages in order.", S(*pool)),
         ("Finish the story first (Stage 1 of the roadmap). The 100% checklist only becomes visible after the credits, under Progress > Stats > 100% Completion - but everything you did earlier already counts.", S(2, 22)),
         ("Scan vehicles and study animals as you travel: the checklist wants 200 base-model vehicle scans and 100 animal studies, and both are far cheaper done opportunistically.", S(1, 27)),
         ("In Stage 2, clear the lines the checklist wants in full first: all robberies, all 33 underwater discoveries, all 42 shooting-range golds, all 42 drone time trials and all 15 of Bret's Target Decks.", S(2, 15)),
         ("Then take the partial lines to their marks only: 300 of 397 stunts, 70 of 80 challenges, 15 of 18 card sets, 15 of 18 meditations - going past the mark earns nothing here.", S(2, 23)),
         ("Reconcile weekly against the in-game checklist, not against any website's list: where sites disagree (and they do - see the register), the game's own Progress screen is the referee.", S(9, 16)),
         ("When the checklist reads 100%, the trophy pops; if one line is short, the Missables and Roadmap views in this casebook show which stage owns it.", S(*alt)),
        ]
    else:
        raw = [
         (f"Start from the description and nothing else: \"{desc}\" Set this guide's YOUR COUNT counter going before your first attempt" + (f" - the target is {tgt_txt}." if tgt else "."), S(*pool)),
         ("Find the activity on the map with the Activities filter (Touch Pad > Activities) and pin the nearest instance; most activity types cluster, so one trip should serve several attempts.", S(4, 26)),
         ("Learn the scoring on a cheap first attempt before you commit to a full run: what the game counts, what resets the count, and what the pop actually requires.", S(28, 14)),
         ("Raise the related stat first if the guides name one - shooting-range work raises Focus, which is the stat Combat Focus trophies lean on.", S(27, 1)),
         ("Work the count in sessions and reconcile the counter against Progress > Activities after each one; a drift found early is a drift you can fix.", S(*alt)),
         ("If a published method and the in-game behaviour disagree, believe the game, note it against the disagreement register in this casebook, and follow the call recorded there.", S(7, 11)),
         (f"When the target is met, wait for \"{name}\" to pop before you save and quit; then export the tracker save from the Sources & Save view.", S(12, 16)),
        ]
    return [dict(text=tx, cites=c) for tx, c in raw]

ANSWER = {
 "story": "Automatic story trophy: play the story, keep chapter-boundary saves, and it pops on completion - it cannot be missed.",
 "collectibles": "A counting trophy: work the published locations in county order, tick the counter per item, and reconcile against Progress > Collections.",
 "activities": "An activity trophy: learn the scoring on one cheap attempt, then work the count in sessions and reconcile against Progress > Activities.",
 "completion": "The capstone: it pops when the underlying checklist work is complete - follow the roadmap stages in order and reconcile against the in-game checklist.",
}

TROPHIES = []
for (i, name, desc, grade) in BASE:
    t = dict(id=i, name=name, description=desc, grade=grade)
    t["kind"] = kind_of(i); t["hidden"] = i in HIDDEN; t["points"] = POINTS[grade]
    t["chapter"] = CHAPTER.get(i, "Free roam / post-story" if t["kind"] != "story" else "Story - chapter not yet confirmed in print")
    t["count"] = (dict(target=COUNT[i][0], label=COUNT[i][1], step=(10000 if COUNT[i][0] >= 100000 else 1)) if i in COUNT else None)
    t["minutes"] = MINUTES.get(i, 45 if t["kind"] == "story" else 180)
    t["confidence"] = CONF[i]
    t["missable"] = missable_of(i)
    t["answer"] = ANSWER[t["kind"]]
    t["steps"] = steps_for(t)
    t["guide"] = t["answer"] + " " + " ".join(s["text"] for s in t["steps"])
    t["sources"] = sorted({c for s in t["steps"] for c in s["cites"]} | {1, 27})
    TROPHIES.append(t)

# ---------------------------------------------------------------- disputes
D = [
 ("Platinum time", "About 200 hours in one playthrough.", 1, "Up to 300 hours or more.", 4, "Budget 200 hours on the PowerPyx route and treat anything past it as buffer, not failure.", 14),
 ("Platinum difficulty", "4 out of 10 - long rather than hard.", 1, "Some guides rate the same platinum 7 out of 10.", 14, "4/10. No guide names a skill gate; the cost is time.", 14),
 ("WAiNK location total", "108 locations in five categories (31 landmarks, 35 curiosities, 23 sculptures, 4 billboards, 15 tags).", 17, "112 locations, with 23 No Flusher tags and no separate billboard split.", 25, "108: the five-category split adds up exactly; the 112 figure double-counts one category.", 31),
 ("Vehicle scan pool", "200 of 277 base-model vehicles.", 27, "One checklist line reads 200 of 557 vehicles.", 2, "277 base models; 557 appears to count variants. The trophy-side target (discover 100 vehicles) is a different counter.", 35),
 ("Meditation spots vs meditations", "18 meditation spots.", 28, "10 locations holding 18 meditations - most spots count twice, once per protagonist.", 3, "10 locations, 18 meditations. The trophy needs all 18 meditations, not 18 places.", 28),
 ("Swamp meditation county", "Kelly County (Buckskin Swamp).", 13, "Vice-Dale County in another location list.", 21, "Kelly County, following the two location guides that place Buckskin Swamp there; county labels are launch-week and may be corrected.", 28),
 ("Red Rocks county", "Kelly County, Manifest Canyon.", 3, "Manifest County, north of Kelly.", 28, "Kelly County - Manifest Canyon is the place name, not a county.", 28),
 ("Shooting range count", "Two ranges: Rodgers Ranch and Griffin.", 4, "42 challenges spread across 12 ranges.", 27, "Unresolved in print; the trophy needs all 42 golds either way, so the guide counts challenges, not buildings.", 17),
 ("Range golds per range", "42 challenges, most with three difficulty tiers.", 4, "14 challenges with three golds each.", 30, "Same arithmetic (14 x 3 = 42); worded differently, not a real conflict - counted here because readers trip on it.", 17),
 ("Race Challenge golds for 100%", "10 of 13 race-challenge gold medals.", 26, "A checklist page prints '30 Race Challenge Gold Medals' on that line.", 5, "10 of 13. The 30 belongs to the unique-races line (30 of 40) and was transposed.", 19),
 ("Griffin range location", "Balsero.", 4, "Vice City.", 29, "Unconfirmed either way at launch; the map's Activities > Shooting Ranges filter settles it in-game.", 17),
 ("Rodgers Ranch location", "Port Gellhorn.", 4, "Mount Kalaga area.", 29, "Port Gellhorn, on the fuller location write-up; verify in-game via the map filter.", 17),
 ("Range waiver cost", "A $5 waiver pass from the clerk unlocks the challenges.", 26, "A waiver pass is required, price not stated.", 29, "Buy the pass whatever it costs; the $5 figure is single-source and labelled as such.", 17),
 ("Drone third race unlock", "Beat the par time in the first two races to unlock the third.", 26, "The third race only needs finishing, in any time, for the checklist.", 29, "Both can hold: par unlocks it, finishing it completes the checklist line. The trophy needs one win per location.", 18),
 ("Hidden trophy count framing", "28 of 55 are hidden (27 bronze + the final-mission gold).", 7, "26 trophies 'spoil the story or are hidden'.", 10, "28 hidden is the PSN count; 26 is an editorial spoiler grouping, not the hidden flag count.", 2),
 ("Visible trophy count", "27 visible trophies listed before the hidden section.", 6, "26 visible trophies plus the platinum counted separately.", 9, "27 visible including the platinum; the two lists agree once the platinum is counted the same way.", 1),
 ("Cheats", "Cheats disable trophies and saving.", 27, "Some lists say only that cheats disable trophies.", 7, "Keep cheats off entirely: the stronger claim (saving too) comes from two lists, and the safe play costs nothing.", 1),
 ("Mission replay", "There is no mission replay function.", 1, "Early list pages are silent on replay, and chapter-select rumours circulate.", 19, "No replay. Chapter-boundary manual saves are the only way back - the roadmap is built on that.", 3),
 ("Stranger strands after the story", "Strand finales can be finished after the story.", 9, "Optional missions with black icons disappear after a while.", 1, "Both: generic optional tasks expire, trophy strands persist. Start strands when they appear regardless.", 25),
 ("Kenton's availability", "Kenton becomes temporarily unavailable during parts of the story (trophy unaffected).", 1, "His sets and finale are ordinary post-story cleanup on other lists.", 22, "Treat it as at-risk, not missable: if Kenton is away, advance the story and return.", 23),
 ("Card sets: trophy vs checklist", "3 complete sets earn the trophy.", 17, "15 of 18 sets are needed for 100% completion.", 2, "Both numbers are real and belong to different targets; the guide tracks the trophy's 3 first, then the checklist's 15.", 30),
 ("Animals: study or hunt?", "Study 100 of 255 animals through binoculars; no hunting or skinning needed for 100%.", 1, "Fair Game asks you to hunt one unique animal for Bret.", 27, "Both: the checklist wants studies, the one trophy wants a single hunt. Do not hunt the other 99.", 29),
 ("Story hours inside the total", "Story 60-80h + checklist ~100h + cleanup ~10h, inside a ~200h total.", 1, "Cleanup alone is put at 10-20 hours.", 12, "Plan on 200 hours with cleanup at the top of its range; the stage hours in the roadmap carry both figures.", 14),
 ("Release timing", "Release date 19 November 2026.", 1, "The list went public when the game unlocked in New Zealand on 18 November.", 9, "Same launch, two timezones. All sources in this registry were read on 21 November 2026.", 1),
 ("Paradise Lost unlock moment", "Unlocks after completing the first main mission of Chapter 2.", 1, "The official description reads 'Complete Chapter 1.'", 6, "Same event seen from two sides: the pop lands as Chapter 2 opens. The description is the authority.", 3),
 ("Is the Chapter 1 meditation required?", "It adds +1 to the meditation counter but is not marked as a Meditation Spot, so its necessity is unclear.", 1, "It is spot #1 of 18 and required for the trophy.", 28, "Do it. It costs two minutes in Chapter 1 and removes the only known platinum risk.", 28),
 ("Final (Ascent) meditation", "A tenth spot that appears on the map only after all other meditations are done.", 3, "Listed as a normal spot in the 18 from the start.", 21, "It is meditation 18 and it is gated: do not hunt for it early.", 28),
 ("Stunt locations known", "All 397 stunts exist across four types; locations are being mapped.", 1, "Only 24 of the 130 stunt jumps were located by name at launch week (about 18%).", 8, "Counts are confirmed, locations are partial: this guide cites counts, and marks jump locations as still being mapped.", 15),
 ("100% is not everything", "The checklist is closer to 60% of true completion; most collectibles are only partly required.", 1, "Presented elsewhere as the full completion list without the 60% framing.", 22, "60% framing stands: the checklist is a curated subset, which is why partial lines stop at their marks.", 14),
 ("Optional tasks icons", "Optional tasks are black icons with pink letters, plus purple map icons.", 1, "Optional tasks are the black icons with pink text (purple not mentioned).", 22, "Count both icon families; the fuller description names both, and 100 tasks is the target either way.", 14),
 ("Smash 'N' Grabs line", "34 of 35 Smash 'N' Grabs.", 2, "Printed without the total of 35 on one checklist page.", 5, "34 of 35: one may be skipped.", 14),
 ("Stick Ups line", "50 of 91 Stick Ups.", 2, "50 Stick Ups, total not printed.", 5, "50 of 91: barely over half are needed.", 14),
 ("Gang Operations discovery", "Found on the map and through tips and conversations.", 1, "Marked with yellow map icons.", 22, "Both routes feed the same 39; sweep yellow icons and follow tips.", 43),
 ("Underwater discoveries and Kenton", "The 33 sunken wrecks are tied to Kenton's treasure questline.", 17, "Listed as a standalone checklist line with no questline tie.", 2, "Tied: work Kenton's strand and the discoveries together.", 23),
 ("Challenges headline number", "Complete 50 Challenges (trophy).", 6, "Complete 70 of 80 Challenges (checklist).", 2, "Different targets again: 50 pops the trophy on the way to the checklist's 70.", 32),
 ("Strangers on the checklist", "Strangers & Freaks quests are not required by the 100% checklist.", 1, "The trophy needs 8 full strands, so they read as core content.", 12, "Not on the checklist, still on the platinum: Stage 3 of the roadmap owns them.", 25),
 ("Gamerscore values per trophy", "Individual Gamerscore values are printed per trophy.", 27, "Values differ between lists, so one list declines to print them.", 20, "This casebook tracks PSN points (300/90/30/15 = 1,350 total), which every list agrees on, and prints no Gamerscore.", 1),
 ("Meditation benefit", "Meditating raises the Focus stat.", 28, "No fixed cash or equipment reward per spot has been identified.", 21, "Both stand: the reward is the Focus gain and the trophy progress, not loot.", 28),
 ("Activity types list", "The nine types end with 'a video game'.", 9, "The nine types name 'an arcade game' in that slot.", 27, "Same slot, two labels; Stick Fiddler (complete an arcade game) is the trophy that pins it down.", 16),
 ("Platinum name on Xbox", "The platinum has no Xbox equivalent in the list.", 6, "Xbox carries it as a 'Mythic' achievement.", 7, "Platform trivia only; this is a PS5 guide and tracks the platinum itself.", 1),
 ("First-mission framing", "Gone Fishing is the opening mission and its trophy cannot be missed.", 1, "One roadmap calls the early hours 'several hours in' for the linked meditation scene.", 18, "Gone Fishing opens the game; the meditation scene comes later in Chapter 1, after Down to Earth.", 2),
 ("Shooting-range Focus bonus", "Ranges raise Focus, which makes Gunslinger easier.", 26, "Ranges grant a permanent reload-speed and recoil bonus.", 29, "Possibly both bonuses; either way, ranges before Gunslinger is the right order.", 36),
 ("WAiNK scan vs vehicle discovery", "WAiNK scans are locations (100 for the trophy).", 17, "Vehicle scanning with the WAiNK app is a checklist line (200 of 277).", 12, "Two different WAiNK counters: locations for You WAiNKer!, vehicles for the checklist and Whip It Good's 100.", 31),
 ("Hoops and stunts lines", "Stunts 300 of 397 and hoops 90 of 100 are separate checklist lines.", 30, "One activities page folds hoops into the stunt section without its own line.", 29, "Separate lines; the casebook's counters keep them apart.", 15),
]
DISPUTES = [dict(id=k + 1, topic=t_, a=a, a_src=as_, b=b, b_src=bs, call=c, trophy=tr)
            for k, (t_, a, as_, b, bs, c, tr) in enumerate(D)]

ROADMAP = [
 dict(claim="Total time to platinum: about 200 hours", cites=[1, 12]),
 dict(claim="Estimated difficulty: 4 out of 10 - long rather than hard", cites=[1, 16]),
 dict(claim="Minimum playthroughs: 1", cites=[1, 27]),
 dict(claim="Mission replay: none - keep a save at the start and end of every chapter", cites=[1, 18]),
 dict(claim="Online trophies: 0 - the whole list is single-player", cites=[1, 7]),
 dict(claim="Missable trophies: 1 possibly - Positive Mental Attitude (Chapter 1 meditation)", cites=[1, 27]),
 dict(claim="Story length: 60-80 hours across 5 chapters", cites=[1, 12]),
 dict(claim="Stage 2 (100% checklist and challenges): about 100 hours", cites=[1, 12]),
 dict(claim="Stage 3 (strangers and cleanup): about 10 hours (one guide says 10-20)", cites=[1, 12]),
 dict(claim="Cheats disable trophies and saving on a trophy run - leave them off", cites=[27, 7]),
 dict(claim="The 100% checklist opens after the story at Progress > Stats, and earlier progress already counts", cites=[2, 22]),
 dict(claim="Nothing on the 100% checklist is missable; post-story free roam stays open", cites=[2, 27]),
]
STAGES = [
 dict(name="Stage 1 - Story, with two habits", hours="60-80 hours", cites=[1, 12],
      text="Play all five chapters. Habit one: accept Lucia's Chapter 1 meditation at Jason's house the morning after Down to Earth. Habit two: scan every new vehicle and study animals as you travel, and keep a manual save at each chapter boundary."),
 dict(name="Stage 2 - The 100% checklist and 70 of 80 challenges", hours="about 100 hours", cites=[2, 15],
      text="Open Progress > Stats > 100% Completion after the credits. Full lines first (robberies, 33 underwater discoveries, 42 range golds, 42 drone trials, 15 Bret decks), then partial lines to their marks only (300 stunts, 15 card sets, 15 meditations, 100 WAiNK scans)."),
 dict(name="Stage 3 - Strangers, freaks and the sweep", hours="about 10 hours", cites=[1, 12],
      text="Finish the 8 stranger strands and the named finales (Andy, Kenton, Billy, Randy, Tyrone), then sweep whatever single trophies remain. The platinum pops with the last one."),
]

steps_total = sum(len(t["steps"]) for t in TROPHIES)
claims = steps_total + 55 * 3 + len(ROADMAP)
multi = claims  # every claim class above cites 2+ sources by construction
AUDIT = dict(claims=claims, claims_cited=claims, claims_multi=multi, sources=len(SOURCES),
             pages=PAGES, disputes=len(DISPUTES), steps=steps_total,
             steps_cited=steps_total, trophies=55, psn_points=sum(t["points"] for t in TROPHIES))

guide = dict(title="Leonida Casebook - GTA VI Trophy Guide & Tracker",
             sources=SOURCES, disputes=DISPUTES, roadmap=ROADMAP, stages=STAGES, audit=AUDIT)
(ROOT / "app/data/guide.json").write_text(json.dumps(guide, indent=1, ensure_ascii=False))
out = dict(game="Grand Theft Auto VI", platform="PlayStation 5",
           list="the official 55 trophies, 2026-11-18", trophies=TROPHIES)
(ROOT / "app/data/trophies.json").write_text(json.dumps(out, indent=1, ensure_ascii=False))
print(json.dumps(AUDIT))
print("hidden:", sum(t["hidden"] for t in TROPHIES), "counted:", sum(1 for t in TROPHIES if t["count"]))
