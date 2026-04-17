# Narrative_RPG_Location_Game_Master_Sheet_Format_v0.4.0.LGM.md

**Narrative RPG Location Game Master Sheet – Specification v0.4.0**

The Location Game Master Sheet (LGM) of the Narrative RPG Save Point Format (NRSP) is the detailed extended or restricted information of a Location.

Location Game Master Sheets MAY evolve over time and multiple `.LGM.md` files MAY exist for the same Location to represent changes in extended or restricted information.

LGM files are organized into named sections using Markdown headers.  Section headers define the semantic meaning of the content that follows.  A LGM MAY contain any number of named sections but MUST contain at least one named section to be valid.  A LGM MAY describe the extended or restricted information in prose, bullet points, tables, or mixed formats.

LGM Sheets SHOULD NOT duplicate publicly observable details already present in the Location Sheet, except where repetition improves retrieval or reduces ambiguity.

Each Location Game Master Sheet MAY reference multiple Save Points.

When present, referenced Save Points indicate narrative states for which this Location Game Master Sheet is valid.

Subheadings within sections are optional unless otherwise specified.

The LGM sections and subsections defined here are suggestions and MAY be extended by the author.

This file is intended for Game Master or Orchestrator use and SHOULD NOT be shared with players unless explicitly desired.

This file format reflects the modularity of NRSP v0.4.0 splitting out the Location Game Master Sheet.

---

## 💾 Header Metadata in YAML

Each `.LGM.md` Location Game Master Sheet MUST begin with a YAML frontmatter block that defines the Location's extended or restricted narrative identity, lineage and the Save Points that it is a part of.

| Field | Required | Description |
|------|----------|-------------|
| Name | ✅ | Canonical name of the Location |
| CurrentAsOf | ❌ | Optional list of filenames of Save Points for which this Location Game Master Sheet is valid |
| Supersedes | ❌ | Optional filename of a prior Location Game Master Sheet this file replaces |
| SupersededBy | ❌ | Optional filename of a later Location Game Master Sheet that replaces this one |
| Status | ❌ | Optional narrative status (e.g., `Active`, `Abandoned`, `Destroyed`, `Hidden`, `Inaccessible`) |
| Tags | ❌ | Optional list of semantic tags for categorization or retrieval |

Field order is not significant; however, the ordering above is recommended for readability.

### Example

```markdown
---
Name: Broken Bridge
CurrentAsOf:
  - Conflict_At_The_Broken_Bridge.NRSP.md
Status: Active
Tags:
  - Crossing
  - Sabotaged
  - Strategic
  - Unstable
---
```

### Minimal Example

```markdown
---
Name: Broken Bridge
---
```

## 🗺️ Location Game Master Sheet Sections

The following sections are recommendations only and are not required for validity.

These sections MAY include tabular data to represent hidden character stats, inventory, or other structured information.

### 🔒 Hidden Truths

This section captures facts about the location that are objectively true but not yet observable by the players.

Hidden Truths represent:
- Concealed history
- False narratives or cover stories
- Structural secrets
- Hidden mechanisms or causes
- Information deliberately obscured by factions or time

These truths MAY eventually be revealed through investigation, consequences, or narrative triggers, but are not assumed to be known at the time of writing.

Hidden Truths SHOULD describe what is actually happening, not how or when players discover it.

#### Example

```markdown
## Hidden Truths

The bridge's central keystone was deliberately removed weeks before the party arrived. 
The damage was disguised as erosion caused by seasonal flooding.
```


### ⚠️ Latent Threats

Latent Threats describe dormant dangers tied to the location that have not yet manifested.

These threats are:
- Conditional
- Escalatory
- Often invisible until triggered

Latent Threats MAY be physical, political, environmental, or supernatural in nature.

This section SHOULD focus on:
- What could go wrong
- Under what conditions
- What kind of failure or escalation would occur

Latent Threats do not have to activate automatically and MAY be mitigated, delayed, or redirected by player action.

#### Example

```markdown
The western support pylons are unstable. Any heavy load or sustained combat on the bridge risks a partial collapse into the ravine below.
```

### 🕵️ Unrevealed Actors

This section documents characters, factions, or entities operating within or around the location that the players have not yet identified.

Unrevealed Actors may include:
- Hidden NPCs
- Observers or spies
- Sleeper agents
- Covert factions
- Creatures avoiding detection

This section SHOULD focus on intent and presence, not stat blocks (unless helpful).

Unrevealed Actors MAY later be promoted to full NPC Sheets once they become known to the party.

#### Example

```markdown
A scout loyal to Captain Vorn has been observing the bridge from the treeline, reporting movements back to Greyford.
```

### 🚨 Future Triggers

Future Triggers define conditional narrative or systemic events that will occur if specific criteria are met.

Triggers MAY be:
- Time-based
- Action-based
- State-based
- Consequence-based

This section SHOULD answer:
- If X happens…
- Then what follows?
- On what timescale?

Future Triggers help the Game Master maintain narrative momentum and internal consistency without pre-scripted outcomes.

Triggers MAY be ignored, altered, or overridden by author intent or emergent play.

#### Example

```markdown
If the party secures the bridge and restores trade, a regional authority will attempt to claim ownership within two sessions.
```

---

## LGM Example

```markdown
---
Name: FortTier
CurrentAsOf:
  - The_Day_The_Gears_Fell_Silent.NRSP.md
Status: Active
Tags:
  - Industrial_Fortress
  - Political_Center
  - Torse
  - Timekeeping
---

## Hidden Truths

FortTier's timekeeping system does more than mark hours.

The illuminated balls embedded along the outer wall are linked to the city's internal pressure regulation system. When all balls illuminate simultaneously, the city briefly enters a stabilized equilibrium—masking otherwise detectable stress in the core engine.

Only the senior engineers of House Calder are aware of this coupling.

---

## Latent Threats

The Core Pressure Engine beneath the Grand Tier is operating above recommended tolerances.

If Torse matches continue at their current frequency without recalibration, a cascading failure will begin in the lower gearworks, first manifesting as timekeeping irregularities (early or delayed ball illumination).

---

## Unrevealed Actors

A covert coalition of minor Houses is using the Torse tournament as political cover.

They have embedded agents among arena engineers, bookmakers, and logistics staff, quietly positioning themselves to exploit any disruption during the final matches.

---

## Future Triggers

- If the pressure engine spikes during a Torse match, the city council will declare emergency authority and suspend all House privileges.
- If the party publicly exposes timekeeping manipulation, House Calder will attempt to discredit them within one session.
- If all wall balls illuminate out of sequence, FortTier will enter lockdown mode.
```

## Minimal LGM Example

```markdown
---
Name: FortTier
Status: Active
---

## Hidden Truths

The city's timekeeping system conceals structural instability beneath the Grand Tier.
```

## Superseding LGM Example

```markdown
---
Name: FortTier
Supersedes: FortTier_Pre_Tournament.LGM.md
CurrentAsOf:
  - The_Day_The_Gears_Fell_Silent.NRSP.md
Status: Active
Tags:
  - Escalating
---

## Latent Threats

Core pressure variance has exceeded safe thresholds. Failure is now a question of timing, not probability.
---

## Secret Motives

The failed truce has forced Vorn into a defensive posture. He is now seeking outside protection and considering abandoning the bridge entirely.
```

## Multiple Save Points LGM Example

```markdown
---
Name: FortTier
CurrentAsOf:
  - Arrival_At_FortTier.NRSP.md
  - The_Day_The_Gears_Fell_Silent.NRSP.md
Status: Active
Tags:
  - Political
  - Volatile
---

## Unrevealed Actors

Multiple Houses are maneuvering behind the scenes, each assuming they are the only ones
using the Torse tournament as leverage.
```
