# Narrative_RPG_Character_Sheet_Format_v0.4.0.CS.md

**Narrative RPG Character Sheet – Specification v0.4.0**

The Character Sheet (CS) of the Narrative RPG Save Point Format (NRSP) is the detailed identity and narrative state of a player character, companion, recurring non-player character (NPC) or a non-player entity with ongoing narrative significance.

Character Sheets MAY evolve over time and multiple `.CS.md` files MAY exist for the same character to represent changes in state, role, or narrative phase.

CS files are organized into named sections using Markdown headers.  Section headers define the semantic meaning of the content that follows.  A CS MAY contain any number of named sections but MUST contain at least one named section to be valid.  A CS MAY describe the character in prose, bullet points, tables, or mixed formats.

Each Character Sheet MAY reference multiple Save Points.

When present, referenced Save Points indicate narrative states for which this Character Sheet is valid.

Subheadings within sections are optional unless otherwise specified.

The CS sections and subsections defined here are suggestions and MAY be extended by the author.

This file format reflects the modularity of NRSP v0.4.0 splitting out the Character Sheet.

---

## 💾 Header Metadata in YAML

Each `.CS.md` Character Sheet MUST begin with a YAML frontmatter block that defines the character's identity, lineage and the Save Points that it is a part of.

| Field | Required | Description |
|------|----------|-------------|
| Name | ✅ | Canonical name of the character |
| Type | ❌ | Optional one of: `PC`, `Companion`, `NPC`, `Entity` (defaults to `PC`) |
| NPCSheet | ❌ | Optional filename of the NPC.md containing extended or restricted details |
| System | ❌ | Optional mechanical or narrative system used to interpret character data |
| IntroducedIn | ❌ | Optional filename of the Save Point or Module where the character first appears |
| CurrentAsOf | ❌ | Optional list of filenames of Save Points for which this Character Sheet is valid |
| Supersedes | ❌ | Optional filename of a prior Character Sheet this file replaces |
| SupersededBy | ❌ | Optional filename of a later Character Sheet that replaces this one |
| Status | ❌ | Optional narrative status (e.g., `Active`, `Missing`, `Deceased`, `Retired`) |
| Tags | ❌ | Optional list of semantic tags for categorization or retrieval |

Field order is not significant; however, the ordering above is recommended for readability.

### Example

```markdown
---
Name: Elara Vance
Type: PC
System: d7-RPG
IntroducedIn: ArrivalAtGreyford.NRSP.md
CurrentAsOf:
  - Conflict_At_The_Broken_Bridge.NRSP.md
Status: Active
Tags:
  - Leader
  - Reluctant
  - Bridge_Arc
---

### Minimal Example

```markdown
---
Name: Elara Vance
```

## 🧑‍🎤 Character Sheet Sections

The following sections are recommendations only and are not required for validity.

These sections MAY include tabular data to represent character stats, inventory, or other structured information.

### 📜 Character Backstory

The narrative history, origin, formative events, or defining moments that occurred for this character.

#### Example

```markdown
## Character Backstory

Elara was raised on the margins of authority, taught early to rely on her own judgment rather than inherited power. She has led before—but never without cost—and every command she gives carries the memory of someone left behind.
```

### 🪪 Character Information

General identifying information such as role, title, species, occupation, age, appearance, or other descriptive traits for this character.

#### Example

```markdown
## Character Information

- Role: Reluctant leader
- Appearance: Travel-worn cloak, weathered armor bearing old insignia
- Demeanor: Controlled, watchful, slow to trust
```

### ⚖️ Character Motivations

Goals, fears, beliefs, ideals, oaths, drives, or unresolved internal conflicts that influence this character's decisions.

#### Example

```markdown
## Character Motivations

Elara seeks stability without tyranny. She believes order is necessary, but only if it is earned—and she is deeply conflicted whenever leadership demands violence.
```

### 🩺 Character Current State

The character's present narrative condition, including emotional state, injuries, stress, fatigue, curses, boons, or temporary effects.

This section MAY reflect the character as of the Save Points referenced in the YAML Frontmatter.

#### Example

```markdown
## Character Current State

Elara was wounded during the skirmish at the Broken Bridge. Though physically weakened, her resolve has hardened. She is wary of the choices ahead and troubled by the consequences of mercy shown to an enemy.
```

### 🤝 Character Relationships

Important relationships, alliances, rivalries, loyalties, or tensions with other characters, factions, or entities.

Relationships MAY be described narratively or as a structured list.

#### Example

```markdown
## Character Relationships

- **Tomas** Trusted ally; offers counsel Elara quietly relies on
- **Captain Vorn** Uneasy truce; mutual respect strained by opposing values
```

### 🧮 Character Stats

This section MAY include mechanical or quantitative attributes defined by the game system in use.

This section MAY include levels, attributes, abilities, moves, conditions, or other system-specific data.

#### Example

```markdown
## Character Stats

| Attribute | Value |
|---------|-------|
| WITS    | 16    |
| LUCK    | 14    |
| RESOLVE | 17    |
| EMPATHY | 11    |
| HP      | 15 / 20 |
```

### 🎒 Inventory / Equipment

Items, resources, artifacts, gear, currency, or possessions currently carried or owned by the character.

Item condition, charges, or narrative significance MAY be noted here.

#### Example

```markdown
## Inventory / Equipment

- Broken signet ring (symbol of lost authority)
- Healing draught (1 remaining)
- The Black Thorn (blade of uncertain origin)
```

### ⚔️ Combat Details

Combat-relevant information such as attacks, defenses, armor, special actions, reactions, or tactical notes.

This section SHOULD be omitted for characters where combat is not narratively relevant.

#### Example

```markdown
## Combat Details

Elara favors defensive positioning and measured strikes. She avoids unnecessary escalation and will withdraw rather than pursue a fleeing opponent.
```

---

## CS Example

```markdown
---
Name: Elara Vance
Type: PC
System: d7-RPG
IntroducedIn: Arrival_At_FortTier.NRSP.md
CurrentAsOf:
  - The_Day_The_Gears_Fell_Silent.NRSP.md
Status: Active
Tags:
  - Leader
  - Stragegist
  - FortTierCitizen
---

## Character Backstory

Elara Vance was raised in the shadow of FortTier's lower gearworks, where failure was loud and survival required precision. Recruited into House Calder's tactical corps at a young age, she distinguished herself through discipline rather than bravado.

Her first command ended in partial success and personal loss, instilling a deep aversion to reckless leadership.

---

## Character Information

- Role: Field Captain
- Affiliation: House Calder
- Species: Human
- Occupation: Tactical Officer
- Appearance: Dark hair worn in a tight braid, scar along left forearm, reinforced field coat
- Known For: Calm under pressure, uncompromising integrity

---

## Character Motivations

- Maintain control in chaotic situations
- Prevent civilian casualties at all costs
- Prove that discipline outlasts spectacle
- Fear: Becoming the kind of leader who sacrifices people for results

---

## Character Current State

Elara is physically uninjured but mentally strained following irregular pressure readings beneath the Grand Tier.

She is aware that her political protection is fragile and suspects House Calder may be withholding critical information.

Morale: Controlled but tense

---

## Character Relationships

| Name              | Relationship Type | Status              | Notes                                      |
|-------------------|-------------------|---------------------|--------------------------------------------|
| Korrin Hale       | Teammate          | Trusted             | Relies on Elara's judgment in the field    |
| Magistrate Calder | Political Patron  | Complicated         | Supportive publicly, evasive privately     |
| Ressa Quill       | Rival             | Hostile             | Competing striker with unclear motives    |

---

## Character Stats

_System: Custom Narrative / Tactical_

| Attribute | Value | Notes                          |
|----------|-------|--------------------------------|
| WITS     | 17    | Tactical awareness             |
| RESOLVE  | 18    | Exceptional mental endurance   |
| AGILITY  | 14    | Trained but not acrobatic      |
| EMPATHY  | 12    | Selective emotional openness   |
| HP       | 28/32 | Minor fatigue accumulated      |

---

## Inventory / Equipment

- Steam-etched Signet of FortTier (symbol of authority)
- Reinforced Torse Gauntlet (field-certified)
- Personal Chronometer (damaged; intermittent lag)
- Field rations (2 remaining)

---

## Combat Details

- Preferred Engagement: Coordinated team maneuvers
- Strengths: Tactical positioning, command presence
- Weaknesses: Limited solo mobility
- Special Notes:
  - Can issue one tactical directive per engagement
  - Gains advantage when defending a fixed position
```

## Minimal CS Example

```markdown
---
Name: Elara
Type: PC
CurrentAsOf:
  - Conflict_At_The_Broken_Bridge.NRSP.md
Status: Active
---

## Character Current State

Injured during the bridge skirmish, but committed to seeing the party through.
```

## Superseding CS Example

```markdown
---
Name: Elara
Type: PC
Supersedes: Elara_Pre_Bridge.CS.md
CurrentAsOf:
  - Conflict_At_The_Broken_Bridge.NRSP.md
Status: Active
Tags:
  - Leader
  - Wounded
---

## Character Current State

Elara bears a fresh wound from the fighting at the bridge. The physical pain is manageable; the weight of command is not.
```

## Multiple Save Points CS Example

```markdown
---
Name: Elara
Type: PC
IntroducedIn: ArrivalAtGreyford.NRSP.md
CurrentAsOf:
  - Conflict_At_The_Broken_Bridge.NRSP.md
  - Aftermath_Of_The_Ravine.NRSP.md
Status: Active
Tags:
  - Leader
  - Transitional
---

## Character Motivations

Elara's decisions at the bridge continue to shape her actions. She is increasingly aware that leadership is no longer something she can avoid.
```

## Linked NPC Sheet CS Example

```markdown
---
Name: Captain Vorn
Type: NPC
IntroducedIn: Conflict_At_The_Broken_Bridge.NRSP.md
NPCSheet: Captain_Vorn.NPC.md
Status: Active
Tags:
  - Authority
  - Truce
---

## Character Current State

Publicly cooperative, privately calculating. Captain Vorn honors the truce—for now.
```