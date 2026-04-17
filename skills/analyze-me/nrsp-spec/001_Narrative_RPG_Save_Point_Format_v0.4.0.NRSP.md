# Narrative_RPG_Save_Point_Format_v0.4.0.NRSP.md

**Narrative RPG Save Point Format – Specification v0.4.0**

The Narrative RPG Save Point Format (NRSP) defines a deterministic representation of a narrative state that can be reloaded to continue a story.

NRSP files are organized into named sections using Markdown headers. Section headers define the semantic meaning of the content that follows.

Subheadings within sections are optional unless otherwise specified.

Emoji used in section headers are OPTIONAL and do not affect semantic meaning or document validity.

Examples intentionally omit emojis to demonstrate minimal, valid syntax.

This file format reflects the full modular vision of NRSP v0.4.0. Everything can be in one file, or split as needed.

---

## 💾 Header Metadata in YAML

Each `.NRSP.md` Save Point MUST begin with a YAML frontmatter block that defines its identity and position within a narrative timeline.

| Field         | Required | Description |
|---------------|----------|-------------|
| Title         | ✅        | Human-readable name of the Save Point |
| System | ❌ | Optional mechanical or narrative system used |
| PreviousSavePoint | ❌   | Optional filename of the immediately preceding Save Point |
| NextSavePoint     | ❌   | Optional filename of the subsequent Save Point |
| AlternateNext     | ❌   | Optional list of filenames representing alternate or forked next Save Points |
| TimelineType  | ❌        | Optional One of: `Mainline`, `Branch`, or `WhatIf` (defaults to `Mainline`) |
| ArcID         | ❌        | Optional identifier for the Save Point within a campaign or story |
| TimelineNote  | ❌        | Optional note describing timeline context or significance |
| SLD           | ❌        | Optional list of filenames of associated Session Log Documents |
| Tags | ❌ | Optional list of semantic tags for categorization or retrieval |
| NRSPFormat | ❌ | Optional (but recommended) format version string (e.g., `0.4.0`). Ensures explicit versioning for validation and tooling |

Field order is not significant; however, the ordering above is recommended for readability.

### Example

```markdown
---
Title: The Conflict at the Broken Bridge
NRSPFormat: 0.4.0
PreviousSavePoint: ArrivalAtGreyford.NRSP.md
NextSavePoint: CrossingTheRavine.NRSP.md
AlternateNext:
  - RetreatToTown.NRSP.md
  - NegotiateWithBandits.NRSP.md
TimelineType: Mainline
ArcID: GB-02
TimelineNote: First major player choice affecting regional control
SLD:
  - Session_2025-03-14.SLD.md
---
```

### Minimal Example

```markdown
---
Title: The Conflict at the Broken Bridge
---
```

---

## 🗓 Narrative Context

The Narrative Context captures the distilled story state at this Save Point.

This section summarizes what matters going forward, such as major outcomes, unresolved threads, emotional shifts, and narrative consequences. It is intentionally concise and does not attempt to record everything that occurred during play.

Detailed moment-to-moment events, dialogue, and rolls SHOULD be captured in the associated Session Log Document (if present).

The structure of this section is intentionally flexible. Authors MAY use headings, bullet points, or prose as appropriate for their story.

### Example

```markdown
## Narrative Context

### Summary
The party confronted bandits controlling the Broken Bridge. After a tense standoff, negotiations failed and violence erupted. Control of the crossing is now uncertain, and word of the conflict is spreading to nearby settlements.

### Notable Moments
- The bridge captain was defeated but not killed
- One party member spared a fleeing bandit
- The bridge structure was damaged during the fight
```

### Minimal Example

```markdown
## Narrative Context

The party reached the Broken Bridge and learned it is controlled by hostile forces.
```

---

## 🧑‍🎤 Character Snapshots

Captures the state of characters at this Save Point.

This section MAY include player characters, companions, recurring NPCs, or other entities.

### Character Subsection

Character Snapshots MAY serve as the complete representation of a character if the author chooses not to maintain separate Character Sheet files.

Each Character defined in this section MUST start with a subsection in the form:
`### Character: [Name]`

This requirement does not apply when Characters are listed exclusively under a
`### Character Sheets` subsection.

If a Character Sheet is linked within an individual character’s subsection, it MUST be labeled in the form:
`Character Sheet: [Name].CS.md`

The structure of this section is intentionally flexible. Authors MAY include as much or as little detail as is necessary to convey character state.

This section MAY include tabular data to represent character stats, inventory, or other structured information.

### Character Sheets Subsection

Alternatively, Character Sheets MAY be listed collectively under a `### Character Sheets` subsection.

### NPC Sheet concept (no new section required)

Some characters MAY have an associated NPC Sheet (.NPC.md) containing extended or restricted details (e.g., secrets, hidden motives, future plot hooks, GM-only context).

NPC Sheets SHOULD NOT duplicate publicly observable details already present in the Character Sheet, except where repetition improves retrieval or reduces ambiguity.

NPC Sheet files (.NPC.md) MAY be linked from a character’s subsection.

If present, the link MUST be labeled in the form:
NPC Sheet: [Name].NPC.md

A character MAY link to both a Character Sheet and an NPC Sheet. In that case:

.CS.md is the shared/public-facing representation of the character.

.NPC.md is the extended/GM-orchestrator representation.

Alternatively, NPC Character Sheets MAY be listed collectively under a `### Character Sheets` subsection.

### Example

```markdown
## Character Snapshots

### Character: Elara
- Role: Reluctant leader
- Level: 3
- Current State: Wounded but resolute
- Notable Traits: Cautious, principled
- Inventory:
  - Broken signet ring
  - Healing draught (1 remaining)
  - The Black Thorn
- Key Relationships:
  - Tomas (trusted ally)
  - Captain Vorn (strained truce)

#### Core Stats
- WITS: 16
- LUCK: 14
- RESOLVE: 17
- EMPATHY: 11
- HP: 15 / 20

### Character Sheets
- Captain_Vorn.CS.md
- Tomas.CS.md
```

### Minimal Example

```markdown
## Character Snapshots

### Character: Elara
Injured during the bridge skirmish, but committed to seeing the party through.
```

### Linking Example

```markdown
## Character Snapshots

### Character: Elara
- Role: Reluctant leader
- Current State: Wounded but resolute
- Key Relationships:
  - Tomas (trusted ally)
  - Captain Vorn (strained truce)

Character Sheet: Elara_Post_Bridge.CS.md
```

### Only Character Sheets Example
```markdown
## Character Snapshots

### Character Sheets
- Elara_Post_Bridge.CS.md
- Captain_Vorn.CS.md
- Tomas.CS.md
```

### NPC Character Sheet Example

```markdown
## Character Snapshots

### Character: Captain Vorn
- Current State: Cooperative, but calculating
- Visible Disposition: Cold professionalism

Character Sheet: Captain_Vorn.CS.md
NPC Sheet: Captain_Vorn.NPC.md
```

### Only Character Sheets and NPCs Example
```markdown
## Character Snapshots

### Character Sheets
- Elara_Post_Bridge.CS.md
- Captain_Vorn.CS.md
- Captain_Vorn.NPC.md
- Tomas.CS.md
```

---

## 🧑‍🤝‍🧑 Party State

The Party State provides a consolidated, situational view of the active group at this Save Point.

Party State is OPTIONAL and MAY be omitted if the Character Snapshots sufficiently describe the current group state.

This section summarizes which characters are currently active, or otherwise unavailable, and captures group-level or comparative information relevant to the immediate narrative or gameplay context.

Party State is intentionally ephemeral and may change frequently between Save Points. It does not replace Character Snapshots or Character Sheets.

This section MAY include tabular data to represent comparative or group-scoped information such as party composition, readiness, formation, temporary conditions, or system-specific stats.

### Example

```markdown
## Party State

Elara and Tomas are traveling together under strain.

| Name   | Status   | Role in Party       | Condition              | Key Notes                                   |
|--------|----------|---------------------|------------------------|---------------------------------------------|
| Elara  | Active   | Reluctant Leader    | Wounded but resolute   | Carrying The Black Thorn; morale holding    |
| Tomas  | Active   | Trusted Ally        | Uninjured              | Defers to Elara’s judgment                  |
| Vorn   | Adjacent | Uneasy Associate    | Physically fit         | Truce in effect; trust remains fragile      |
```

### Minimal Example

```markdown
## Party State

Elara and Tomas are traveling together under strain. Captain Vorn remains nearby under a fragile truce.
```

---

## 🗺️ Location Snapshots

Captures the state of locations at this Save Point.

This section MAY include towns, cities, hubs, regions, planes, galaxies, worlds, or other locations.

### Location Subsection

Location Snapshots MAY serve as the complete representation of a location if the author chooses not to maintain separate Location files.

Each Location defined in this section MUST start with a subsection in the form:
`### Location: [Name]`

This requirement does not apply when Locations are listed exclusively under a
`### Location Sheets` subsection.

If a Location Sheet is linked within an individual location’s subsection, it MUST be labeled in the form:
`Location Sheet: [Name].LS.md`

The structure of this section is intentionally flexible. Authors MAY include as much or as little detail as is necessary to convey location information and state.

This section MAY include tabular data to represent shops, taverns, governmental hierarchy, or other structured information.

### Location Sheets Subsection

Alternatively, Location Sheets MAY be listed collectively under a `### Location Sheets` subsection.

### Example

```markdown
## Location Snapshots

### Location: Bramblebend
- Type: Riverside town
- Current State: Partially destroyed
- Population: ~50 (down from ~150)
- Threat Level: Unstable
- Control: No active authority

#### Notable Features
- The Iron Bridge (50% structural integrity)
- Burned North Gate
- Abandoned marketplace

#### Points of Interest
| Location        | Status        | Notes                                     |
|-----------------|---------------|-------------------------------------------|
| The Lazy Dragon | Closed        | Safe for rest, no services                |
| Blacksmith     | Abandoned     | Forge still warm; owner missing           |
| River Docks    | Damaged       | Unsafe for cargo transport                |
```

### Minimal Example

```markdown
## Location Snapshots

### Location: Bramblebend
A damaged bridge town struggling to recover after recent violence.
```

### Linked Location Sheet Example

```markdown
## Location Snapshots

### Location: Bramblebend
- Current State: Half-ruined, fearful
- Control: Power vacuum

Location Sheet: Bramblebend.LS.md
```

### Location Sheets Only Example
```markdown
## Location Snapshots

### Location Sheets
- Bramblebend.LS.md
- Grey_Marches.LS.md
```

---

## 📝 Session Log

This section represents an OPTIONAL embedded Session Log and is semantically equivalent to a standalone Session Log Document [.SLD.md](./002_Narrative_RPG_Save_Point_Format_v0.4.0.SLD.md).

If both embedded Session Log content and Session Log Document links are present, the embedded section is the primary source for Session Log information for this Save Point.

Authors SHOULD prefer external .SLD.md files for long or detailed session logs.

Subsections MAY include one or more of the following: Opening Scene, Major Events, Important Interactions, Session Narrative, Legendary Acknowledgments, Closing Image, Detailed Transcript

If no subsections are present, the content under `## Session Log` is assumed to be `### Session Narrative`.

### Example

```markdown
## Session Log

### Opening Scene

The fog hangs low over the Broken Bridge as the party approaches at dawn. The river below churns loudly, masking distant voices on the far side. Weathered banners hang from the stone pylons, their colors faded by rain and neglect. Even before words are exchanged, it is clear this crossing is not unguarded.

### Session Narrative

What began as a tense standoff quickly spiraled into chaos. The narrow stone span offered little room for maneuvering, and every misstep threatened to send combatants tumbling into the river below. Amid the clash of steel and shouted orders, the party was forced to decide whether control of the crossing was worth the cost in blood.

By the time the fighting ended, the bridge itself bore the scars of the conflict. Trust was broken, alliances strained, and word of the confrontation was already beginning to spread beyond the ravine.

### Closing Image

As night falls, the broken silhouette of the bridge stands stark against the moonlit river. Fires burn on both banks, but no one dares cross. The path forward remains open—but at a cost.
```

### Minimal Example

```markdown
## Session Log

What began as a tense standoff quickly spiraled into chaos. The narrow stone span offered little room for maneuvering, and every misstep threatened to send combatants tumbling into the river below. Amid the clash of steel and shouted orders, the party was forced to decide whether control of the crossing was worth the cost in blood.

By the time the fighting ended, the bridge itself bore the scars of the conflict. Trust was broken, alliances strained, and word of the confrontation was already beginning to spread beyond the ravine.
```

---

## 🔗 Linked Files

Linked Files is an OPTIONAL section that provides a consolidated index of relevant files that are not semantically owned by another section.

This section SHOULD NOT duplicate links already present in Character Snapshots, Location Snapshots, or Header Metadata unless repetition improves discoverability.

Linked Files is intended for:
- Reference material
- World rules
- Artifacts
- External documents
- System notes


### Example

```markdown
## Linked Files

| File                         | Purpose                                      |
|------------------------------|----------------------------------------------|
| World_Rules_v1.md            | Core setting rules                           |
| Faction_Overview.md          | Political groups active in the region        |
| Map_Grey_Marches.png         | Regional map reference                       |
| Prophecy_Of_The_Thorn.md     | Lore document referenced indirectly          |
```

---

## NRSP Example

```markdown
---
Title: The Day the Gears Fell Silent
NRSPFormat: 0.4.0
PreviousSavePoint: Arrival_At_FortTier.NRSP.md
NextSavePoint: The_Final_Torse.NRSP.md
AlternateNext:
  - Sabotage_At_Dawn.NRSP.md
  - Flight_From_The_Tier.NRSP.md
TimelineType: Mainline
ArcID: FT-07
TimelineNote: The Torse Championship begins as political tensions surface beneath FortTier.
SLD:
  - Session_2025-09-18.SLD.md
---

## Narrative Context

### Summary
FortTier stands at full steam as the Grand Torse Championship begins. Crowds flood the iron terraces, gearworks hum at maximum output, and banners of rival houses hang uneasily beside one another. While the city celebrates, fractures beneath the surface widen.

The party has arrived as honored guests of House Calder, but evidence suggests the final Torse match may be used as cover for a coordinated act of sabotage aimed at the city’s core pressure engine.

Victory in the arena could grant the party influence and access. Failure—or exposure—could plunge FortTier into chaos.

### Unresolved Threads
- The origin of the altered Torse field schematics remains unknown
- House Calder’s true involvement is unclear
- A pressure spike has been detected beneath the Grand Tier

---

## Character Snapshots

### Character: Elara Vance
- Role: Field Captain and Strategist
- Level: 5
- Current State: Focused, burdened by expectation
- Notable Traits: Tactical, principled, relentless
- Inventory:
  - Steam-etched Signet of FortTier
  - Reinforced Torse Gauntlet
  - Personal Chronometer (damaged)
- Key Relationships:
  - Korrin Hale (trusted teammate)
  - Magistrate Calder (political patron)

#### Core Stats
| Stat      | Value |
|-----------|-------|
| WITS     | 17    |
| RESOLVE  | 18    |
| AGILITY  | 14    |
| EMPATHY  | 12    |
| HP       | 28 / 32 |

Character Sheet: Elara_Vance.CS.md

---

### Character: Korrin Hale
- Role: Power Striker
- Level: 5
- Current State: Energized, masking nerves
- Notable Traits: Bold, loyal, impulsive
- Inventory:
  - Pneumatic Torse Harness
  - Shock-lined Greaves
- Key Relationships:
  - Elara Vance (team captain)
  - Ressa Quill (rival striker)

Character Sheet: Korrin_Hale.CS.md

---

### Character: Magistrate Aldric Calder
- Current State: Publicly supportive, privately guarded
- Visible Disposition: Measured confidence

Character Sheet: Aldric_Calder.CS.md  
NPC Sheet: Aldric_Calder.NPC.md

---

## Party State

The team is registered for the Torse semifinals and operating under public scrutiny.

| Name   | Status | Party Role        | Condition            | Key Notes                                      |
|--------|--------|-------------------|----------------------|------------------------------------------------|
| Elara  | Active | Team Captain      | Focused              | Tactical control of the field                  |
| Korrin | Active | Primary Striker   | Adrenalized          | Overclocked harness (temporary boost)          |
| Calder | Adj.   | Political Sponsor | Uninjured            | Influence may shield the party if leveraged    |

---

## Location Snapshots

### Location: FortTier
- Type: Vertical industrial city-fortress
- Current State: Operational at peak capacity
- Population: ~80,000
- Control: Council of Houses
- Threat Level: Rising

#### Notable Features
- The Grand Tier (central arena and civic hub)
- Steam Spine Elevators
- Core Pressure Engine (restricted)

#### Torse Infrastructure
| Facility              | Status     | Notes                                              |
|-----------------------|------------|----------------------------------------------------|
| Grand Torse Arena     | Active     | Modified field layout detected                     |
| Training Annex        | Restricted | Guarded by House Calder sentries                   |
| Gearworks Sublevel C  | Unstable   | Pressure readings exceeding safe thresholds        |

Location Sheet: FortTier.LS.md

---

## Session Log

### Opening Scene

Steam hisses from pressure vents along the Grand Tier as dawn breaks over FortTier. The iron terraces fill with early crowds, banners snapping in the wind as vendors and officials scramble into position. Far below the arena floor, unseen mechanisms churn, their rhythms slightly out of sync with the city’s usual heartbeat.

From their assigned gallery, the party can see the full expanse of the Grand Torse Arena — and the unusually dense guard presence surrounding the restricted access corridors beneath it.

### Major Events

- **Arena Arrival:** The team is formally announced as semifinal contenders, drawing attention from rival houses and the press.
- **Anomalous Readings:** Elara detects irregular pressure fluctuations during pre-match inspection.
- **Restricted Access Denied:** Attempts to enter the Gearworks Sublevel are blocked by House Calder sentries citing emergency protocols.
- **Rival Interference:** Korrin spots Ressa Quill conferring with an unknown engineer near the service lifts.
- **Pressure Spike:** Sensors register a brief surge from beneath the arena moments before the match begins.

### Important Interactions

- Magistrate Calder publicly reassures the party while privately urging discretion.
- A junior engineer quietly confirms that the Torse field layout was altered overnight without full council approval.
- Ressa Quill exchanges a tense glance with Korrin before disappearing into the lower tiers.

### Session Narrative

As the city roars in anticipation of the semifinal match, the party finds itself balancing spectacle and subterfuge. Every cheer from the stands is matched by the hiss of unstable machinery beneath their feet. What should have been a straightforward competition now feels like a distraction — a carefully staged cover for something far more dangerous.

Elara must decide whether to push for influence through victory or risk exposure by pressing deeper into FortTier’s underbelly. Meanwhile, Korrin wrestles with the realization that the match itself may be weaponized against both the team and the city.

### Legendary Acknowledgments

As the Torse field activates, ancient resonance glyphs embedded in the arena walls pulse briefly out of sequence. The phenomenon lasts only a heartbeat, but long enough for those watching closely to sense that FortTier’s foundations are responding to forces beyond politics or sport.

### Closing Image

The match horn sounds and the crowd erupts as the Torse semifinals begin. Above, banners billow proudly in the steam-filled air. Below, unseen pressure continues to build. FortTier celebrates — unaware of how close it stands to catastrophe.

## Linked Files

| File                          | Purpose                                      |
|-------------------------------|----------------------------------------------|
| Torse_Rules_Standard.md       | Official Torse match regulations             |
| FortTier_Political_Map.md     | Power blocs within the Council of Houses     |
| House_Calder_Overview.md      | Background and known alliances               |
| Pressure_Engine_Schematic.png | Partial diagram recovered by the party       |

---
```
