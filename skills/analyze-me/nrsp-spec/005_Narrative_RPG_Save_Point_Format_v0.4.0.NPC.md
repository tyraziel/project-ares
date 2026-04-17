# Narrative_RPG_Character_Sheet_Format_v0.4.0.NPC.md

**Narrative RPG Non-Player Character Sheet – Specification v0.4.0**

The Non-Player Character Sheet (NPC) of the Narrative RPG Save Point Format (NRSP) is the detailed extended or restricted information of a Non-Player Character, companion, or a non-player entity with ongoing narrative significance.

Non-Player Character Sheets MAY evolve over time and multiple `.NPC.md` files MAY exist for the same Non-Player Character to represent changes in extended or restricted information.

NPC files are organized into named sections using Markdown headers.  Section headers define the semantic meaning of the content that follows.  A NPC MAY contain any number of named sections but MUST contain at least one named section to be valid.  A NPC MAY describe the extended or restricted information in prose, bullet points, tables, or mixed formats.

NPC Sheets SHOULD NOT duplicate publicly observable details already present in the Character Sheet, except where repetition improves retrieval or reduces ambiguity.

Each Non-Player Character Sheet MAY reference multiple Save Points.

When present, referenced Save Points indicate narrative states for which this Non-Player Character Sheet is valid.

Subheadings within sections are optional unless otherwise specified.

The NPC sections and subsections defined here are suggestions and MAY be extended by the author.

This file is intended for Game Master or Orchestrator use and SHOULD NOT be shared with players unless explicitly desired.

This file format reflects the modularity of NRSP v0.4.0 splitting out the Non-Player Character Sheet.

---

## 💾 Header Metadata in YAML

Each `.NPC.md` Non-Player Character Sheet MUST begin with a YAML frontmatter block that defines the Non-Player Character's identity, lineage and the Save Points that it is a part of.

| Field | Required | Description |
|------|----------|-------------|
| Name | ✅ | Canonical name of the Non-Player Character |
| CurrentAsOf | ❌ | Optional list of filenames of Save Points for which this Non-Player Character Sheet is valid |
| Supersedes | ❌ | Optional filename of a prior Non-Player Character Sheet this file replaces |
| SupersededBy | ❌ | Optional filename of a later Non-Player Character Sheet that replaces this one |
| Status | ❌ | Optional narrative status (e.g., `Active`, `Missing`, `Deceased`, `Retired`) |
| Tags | ❌ | Optional list of semantic tags for categorization or retrieval |

Field order is not significant; however, the ordering above is recommended for readability.

### Example

```markdown
---
Name: Captain Vorn
CurrentAsOf:
  - Conflict_At_The_Broken_Bridge.NRSP.md
Status: Active
Tags:
  - Authority
  - Truce
  - HiddenAgenda
---
```

### Minimal Example

```markdown
---
Name: Captain Vorn
---
```

## 🕵️ Non-Player Character Sheet Sections

The following sections are recommendations only and are not required for validity.

These sections MAY include tabular data to represent hidden character stats, inventory, or other structured information.

### 🎭 Secret Motives

Hidden goals, private beliefs, long-term plans, or conflicting loyalties not openly expressed by the character.

This section SHOULD capture why the NPC acts the way they do behind the scenes.

#### Example

```markdown
## Secret Motives

Captain Vorn intends to maintain control of the Broken Bridge regardless of which faction officially claims authority. He views the truce as temporary and is quietly assessing which side will best secure his long-term position.
```

### 🗝️ Secret Inventory

Items, resources, leverage, or assets possessed by the NPC that are not publicly known.

This may include hidden weapons, documents, illicit goods, blackmail material, or off-screen resources.

#### Example

```markdown
## Secret Inventory

- Sealed orders from the Greyford council (unsigned)
- Hidden signal flare stored beneath the bridge watchtower
- Personal ledger detailing past toll arrangements
```

### 🤝 Secret Relationships

Covert alliances, debts, obligations, informants, or manipulative ties unknown to the players.

Relationships in this section MAY contradict or undermine publicly stated allegiances.

#### Example

```markdown
- **Greyford Trade Syndicate** – Accepts quiet payments in exchange for reduced inspections
- **Unnamed Bandit Lieutenant** – Former subordinate believed dead; still active
```

---

## NPC Example

```markdown
---
Name: Captain Vorn
CurrentAsOf:
  - Conflict_At_The_Broken_Bridge.NRSP.md
Status: Active
Tags:
  - Authority
  - Opportunist
---

## Secret Motives

Vorn believes centralized authority is inevitable and intends to survive whichever regime emerges. He is willing to betray both the party and the bandits if it ensures his continued command.

## Secret Inventory

- Counterfeit bridge permits
- Hidden weapon cache beneath the eastern pylon

## Secret Relationships

- **Bridge Smugglers** – Ongoing profit-sharing arrangement
- **Greyford Magistrate (unknown to party)** – Political cover in exchange for silence
```

## Minimal NPC Example

```markdown
---
Name: Captain Vorn
CurrentAsOf:
  - Conflict_At_The_Broken_Bridge.NRSP.md
---

## Secret Motives

Vorn intends to break the truce once the party leaves the region.
```

## Superseding NPC Example

```markdown
---
Name: Captain Vorn
Supersedes: Captain_Vorn_Pre_Truce.NPC.md
CurrentAsOf:
  - Aftermath_Of_The_Ravine.NRSP.md
Status: Active
Tags:
  - Compromised
---

## Secret Motives

The failed truce has forced Vorn into a defensive posture. He is now seeking outside protection and considering abandoning the bridge entirely.
```

## Multiple Save Points NPC Example

```markdown
---
Name: Captain Vorn
CurrentAsOf:
  - Conflict_At_The_Broken_Bridge.NRSP.md
  - Aftermath_Of_The_Ravine.NRSP.md
Status: Active
Tags:
  - Transitional
---

## 🕸️ Secret Relationships

Vorn's alliances are shifting rapidly as control of the region destabilizes.
```