# Narrative_RPG_Location_Sheet_Format_v0.4.0.LS.md

**Narrative RPG Location Sheet – Specification v0.4.0**

The Location Sheet (LS) of the Narrative RPG Save Point Format (NRSP) is the detailed information and narrative state of a location with ongoing narrative significance.

Locations MAY evolve over time and multiple `.LS.md` files MAY exist for the same location to represent changes in state, role, or narrative phase.

LS files are organized into named sections using Markdown headers.  Section headers define the semantic meaning of the content that follows.  A LS MAY contain any number of named sections but MUST contain at least one named section to be valid.  A LS MAY describe the location in prose, bullet points, tables, or mixed formats.

Each Location Sheet MAY reference multiple Save Points.

When present, referenced Save Points indicate narrative states for which this Location Sheet is valid.

Subheadings within sections are optional unless otherwise specified.

The LS sections and subsections defined here are suggestions and MAY be extended by the author.

This file format reflects the modularity of NRSP v0.4.0 splitting out the Location Sheet.

---

## 💾 Header Metadata in YAML

Each `.LS.md` Location MUST begin with a YAML frontmatter block that defines the location and the Save Points that it is a part of.

| Field | Required | Description |
|------|----------|-------------|
| Name | ✅ | Canonical name of the location |
| Type | ❌ | Optional descriptive type (e.g., `Point of Interest`, `Town`, `Village`, `Region`, `Structure`, `World`, `Galaxy`; defaults to `Town`) |
| GMSheet | ❌ | Optional filename of the LGM.md containing extended or restricted details |
| System | ❌ | Optional mechanical or narrative system used to interpret location information |
| IntroducedIn | ❌ | Optional filename of the Save Point or Module where the location first appears |
| CurrentAsOf | ❌ | Optional list of filenames of Save Points for which this Location Sheet is valid |
| Supersedes | ❌ | Optional filename of a prior Location Sheet this file replaces |
| SupersededBy | ❌ | Optional filename of a later Location Sheet that replaces this one |
| Status | ❌ | Optional narrative status (e.g., `Active`, `Abandoned`, `Destroyed`, `Hidden`, `Inaccessible`) |
| Tags | ❌ | Optional list of semantic tags for categorization or retrieval |

Field order is not significant; however, the ordering above is recommended for readability.

### Example

```markdown
---
Name: Broken Bridge
Type: Point of Interest
IntroducedIn: ArrivalAtGreyford.NRSP.md
CurrentAsOf:
  - Conflict_At_The_Broken_Bridge.NRSP.md
Status: Damaged
Tags:
  - Crossing
  - Strategic
  - Contested
---
```

### Minimal Example
```markdown
---
Name: Broken Bridge
---
```

## 🌍 Location Sheet Sections

The following sections are recommendations only and are not required for validity.

These sections MAY include tabular data to represent points of interest, political structures, infrastructure, or other structured information.

### 📖 Location Overview

A high-level description of the location’s identity and purpose within the narrative.

This section SHOULD establish what the location *is*, why it matters, and how it is generally perceived by those who encounter it. Historical context, reputation, and common usage MAY be included here.

This section SHOULD remain relatively stable across Save Points unless the location undergoes a fundamental transformation.

#### Example

```markdown
### Location Overview

The Broken Bridge spans the narrow Ravine of Greyford, serving as the only reliable crossing for miles in either direction. Once a maintained trade route, it has fallen into disrepair following years of neglect and recent violence.

The bridge is narrow, exposed, and unforgiving—any conflict here is immediately dangerous.
```

### 🧩 Current State Narrative

The present narrative condition of the location as of the Save Points referenced in the YAML frontmatter.

This section captures recent changes, damage, instability, occupation, secrecy, or evolving significance. It SHOULD reflect the *current reality* rather than the location’s intended or historical role.

This section is expected to change frequently across Save Points and MAY supersede prior Location Sheets.

#### Example

```markdown
The bridge has been partially damaged during the recent confrontation between travelers and bandits. Several stones have collapsed along the eastern parapet, and temporary barricades litter the span.

Control of the crossing is unclear. Word of the skirmish is spreading, and nearby settlements are already reacting to the instability.
```

### 🏗️ Notable Features

Key physical, structural, environmental, or magical features that define the location.

This section MAY include landmarks, terrain features, architectural elements, hazards, defenses, or unusual properties that affect interaction, travel, or encounters.

Features MAY be described narratively or as a structured list.

#### Example

```markdown
- Cracked stone pylons anchoring the bridge
- Narrow walking surface with minimal guardrails
- Temporary wooden barricades and debris
- Ravine drop of approximately 80 feet on either side
```

### 🏛️ Governmental Structure / Hierarchy

The authority, control, or power structures that claim influence over the location.

This section MAY describe formal governance, informal control, contested authority, factions, councils, occupying forces, or the absence of leadership.

For locations without governance, this section MAY explicitly state that no authority is recognized.

#### Example

```markdown
No formal authority currently claims jurisdiction over the bridge.

Historically maintained by Greyford’s council, responsibility has lapsed due to funding disputes and political infighting.
```

### 📍 Points of Interest

Distinct sub-locations within the broader location that are narratively or mechanically relevant.

This section MAY include buildings, districts, rooms, routes, access points, or hidden areas. Points of Interest MAY be presented as prose, bullet points, or tables with status and notes.

#### Example
```markdown
| Location Area      | Status        | Notes                                   |
|--------------------|---------------|-----------------------------------------|
| Central Span       | Damaged       | Unsafe footing; risk of collapse        |
| East Parapet       | Breached      | Stonework destroyed during the fight    |
| Ravine Access Path | Unmonitored   | Used by bandits for ambush positioning  |
```

### 🔗 Location Connections

Narrative or geographic connections between this location and others.

This section SHOULD describe roads, paths, portals, trade routes, political ties, or story-relevant relationships that link this location to surrounding areas or factions.

Connections MAY change over time and SHOULD reflect the Current State Narrative when relevant.

#### Example
```markdown
- **Greyford** – Nearest town relying on the bridge for trade
- **Northern Trade Road** – Severely disrupted by bridge instability
- **Ravine Undercross** – Potential hidden route beneath the bridge
```

---

## LS Example
```markdown
---
Name: FortTier
Type: City-Fortress
IntroducedIn: Arrival_At_FortTier.NRSP.md
CurrentAsOf:
  - The_Day_The_Gears_Fell_Silent.NRSP.md
Status: Active
Tags:
  - Fortress
  - Industrial
  - Political
  - VerticalCity
---

## Location Overview

FortTier is a massive walled city-fortress constructed in ascending stone and steel tiers, each ring reinforcing the one below it. Designed for defense, industry, and spectacle in equal measure, FortTier dominates the surrounding landscape both physically and politically.

The city functions as a hub of governance, competition, and mechanical innovation, drawing travelers, merchants, and power-seekers alike.

Time within FortTier is not spoken in hours, but in *orbs*.

---

## Current State Narrative

FortTier appears orderly and controlled, its gates open and its terraces filled with activity. Beneath the surface, however, political tension and mechanical strain are mounting.

Pressure systems beneath the upper tiers have begun to behave unpredictably, and several internal access routes have been quietly restricted. Public confidence remains high, but decision-making within the ruling houses has grown cautious and fragmented.

As the Torse season reaches its climax, FortTier’s attention is fixed on the arena. Matches draw unprecedented crowds, and House banners hang heavier with expectation than celebration.

Behind the spectacle, several Torse field configurations have been quietly altered, and access to arena sublevels has been restricted under Council authority. Officially, this is attributed to crowd safety and maintenance. Unofficially, whispers suggest Torse itself may be leveraged as a political instrument, or a distraction from deeper instability within the city.

---

## Notable Features

- **Tiered Wall Structure:** Concentric fortified tiers rise inward toward the Grand Tier, each serving a defensive and civic function.
- **Outer Wall Time Ring:** A continuous band of illuminated orbs crowns the outer wall.
- **Orb-Time System:** A streak of light circles the wall; each full circuit illuminates one orb. When all orbs are lit, they flare briefly before dimming and restarting the cycle.
- **Directional Timekeeping:** Time is referenced by gate and ball count (e.g., “three orbs past East Gate”).
- **Gate Network:** Major cardinal gates anchor commerce, security, and time references.
- **The Grand Torse Arena:** A massive central stadium capable of hosting tens of thousands, engineered for spectacle, sound amplification, and controlled chaos.

---

## Governmental Structure / Hierarchy

FortTier is governed by a **Council of Houses**, each controlling a specific tier or function within the city.

While the Council presents a unified public front, internal rivalries and competing priorities influence policy, enforcement, and information flow.

House Calder currently holds significant operational authority.

Torse is formally regulated by the Council but informally weaponized by it. Annual and seasonal Torse matches—particularly the **Tournament of Houses** are used to:
- Display dominance
- Settle rivalries without open war
- Shift public sentiment
- Justify political decisions under the guise of sport

House Calder currently exerts disproportionate influence over Torse scheduling, officiation, and arena access.

---

## Points of Interest

| Location | Description | Status |
|--------|------------|--------|
| Grand Tier | Central arena and civic hub | Active |
| Grand Torse Arena | Primary venue for Torse matches and tournaments | Active |
| Arena Sublevels | Training halls, holding chambers, and restricted access tunnels | Restricted |
| East Gate | Trade and public ingress | Open |
| South Gate | Industrial access and freight | Restricted |
| Lower Gearworks | Mechanical infrastructure | Partially sealed |
| Upper Wall Ring | Timekeeping orbs and light track | Active |

---

## Location Connections

- Connected to surrounding regions via gated trade roads
- Political influence extends beyond city limits through House alliances
- Internal access between tiers is tightly controlled and time-regulated
```

## Minimal LS Example
```markdown
---
Name: FortTier
Type: City-Fortress
Status: Active
---

## Location Overview

A massive tiered fortress-city where time is measured by illuminated orbs circling the outer wall.
```

## Superseding LS Example
```markdown
---
Name: FortTier
Supersedes: FortTier_Pre_Championship.LS.md
CurrentAsOf:
  - The_Day_The_Gears_Fell_Silent.NRSP.md
Status: Active
Tags:
  - Instability
  - PoliticalStrain
---

## Current State Narrative

Following irregular pressure events beneath the Grand Tier, several internal corridors have been sealed and guard presence has increased. Official statements cite maintenance, but the Council has begun operating under emergency protocols.
```

## Multiple Save Points LS Example

```markdown
---
Name: FortTier
IntroducedIn: Arrival_At_FortTier.NRSP.md
CurrentAsOf:
  - The_Day_The_Gears_Fell_Silent.NRSP.md
  - After_The_Semifinals.NRSP.md
Status: Active
Tags:
  - Transitional
---

## 🧩 Current State Narrative

FortTier’s public rhythm continues uninterrupted, but access patterns and enforcement vary subtly depending on time-cycle and gate alignment.
```

## Linked GM Sheet LS Example

```markdown
---
Name: FortTier
Type: City-Fortress
GMSheet: FortTier.LGM.md
Status: Active
Tags:
  - HiddenSystems
  - GMSecrets
---

## 📖 Location Overview

A fortified vertical city whose visible order conceals fragile systems beneath its tiers.
```