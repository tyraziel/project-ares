# Narrative_RPG_Save_Point_Format_v0.4.0.SLD.md

**Narrative RPG Save Point Format - Session Log Document – Specification v0.4.0**

The Session Log Document (SLD) of the Narrative RPG Save Point Format (NRSP) is the detailed, chronological record of what happened during play.  "Chronological" refers to narrative sequence, not mechanical timestamps.
An SLD MAY summarize scenes, emotions, or symbolic moments so long as the ordering and consequences of events are preserved.

SLD files are organized into named sections using Markdown headers.  Section headers define the semantic meaning of the content that follows.  An SLD MAY contain any number of named sections but MUST contain at least one named section to be valid.  An SLD MAY describe events in prose, bullet points, scene blocks, dialogue transcripts, or mixed formats.

Each Session Log Document MUST reference exactly one Save Point.

Subheadings within sections are optional unless otherwise specified.

The SLD sections and subsections defined here are suggestions and MAY be extended by the author.

This file format reflects the modularity of NRSP v0.4.0 splitting out the Session Log Document.

---

## 💾 Header Metadata in YAML

Each `.SLD.md` Session Log Document MUST begin with a YAML frontmatter block that defines the Save Point that it is a part of.

| Field         | Required | Description |
|---------------|----------|-------------|
| SessionLogTitle         | ✅       | Human-readable name of the Session Log Document |
| SavePoint       | ✅       | The filename of the Save Point the Session Log Document is a part of |
| InGameDate     | ❌      | Optional in game date/time of the session |
| SessionDate     | ❌      | Optional real date/time of the session |
| SessionDuration | ❌      | Optional the duration of the session |
| SessionNumber   | ❌      | Optional the session number |
| System | ❌ | Optional mechanical or narrative system used |
| Tags | ❌ | Optional list of semantic tags for categorization or retrieval |

Field order is not significant; however, the ordering above is recommended for readability.

### Example

```markdown
---
SessionLogTitle: The Conflict at the Broken Bridge
SavePoint: TheConflictattheBrokenBridge.NRSP.md
InGameDate: 12th Day of Highsummer, Year 403
SessionDate: 2025-03-14
SessionDuration: 3h 45m
SessionNumber: 17
System: d7-RPG
Tags:
 - Bridge
 - Conflict
---
```

---

## 🗂️ Session Log Document Sections

The following sections are recommendations only and are not required for validity.

### 🎬 Opening Scene

Introduces the session's initial location, mood, and narrative framing.

This section is commonly used to establish tone, stakes, or environmental context before significant events occur.

#### Example

```markdown
## Opening Scene

The fog hangs low over the Broken Bridge as the party approaches at dawn. The river below churns loudly, masking distant voices on the far side. Weathered banners hang from the stone pylons, their colors faded by rain and neglect. Even before words are exchanged, it is clear this crossing is not unguarded.
```

### 🧭 Major Events

Summarizes the key actions, decisions, or turning points that occurred during the session, listed in narrative order.

This section SHOULD focus on events with lasting narrative and/or mechanical consequences.

#### Example

```markdown
## Major Events

- **First Contact:** Armed guards halt the party at the bridge's edge and demand a toll far exceeding local custom.
- **Negotiation Fails:** Accusations of smuggling and espionage derail attempts at diplomacy.
- **Violence Erupts:** A crossbow bolt strikes the stone railing, splintering the fragile truce.
- **Structural Damage:** Fighting along the span damages the central support, leaving the bridge unstable.
- **Aftermath:** The guards withdraw, but control of the crossing remains uncertain.
```

### 🤝 Important Interactions

Captures meaningful interactions between characters, factions, entities, or locations that may affect future relationships, alliances, or conflicts.

This section is especially useful for tracking social dynamics and evolving tensions.

#### Example

```markdown
## Important Interactions

- Elara challenges Captain Vorn's authority over the bridge and questions his mandate.
- Tomas intervenes to prevent the execution of a wounded guard after the fighting ends.
- A fleeing bandit is spared, leaving behind information about movements in nearby settlements.
```

### 📖 Session Narrative

Provides a freeform prose account of the session's flow.

This section MAY overlap with other sections and is intended to preserve narrative continuity, emotional beats, or thematic progression.

#### Example

```markdown
## Session Narrative

What began as a tense standoff quickly spiraled into chaos. The narrow stone span offered little room for maneuvering, and every misstep threatened to send combatants tumbling into the river below. Amid the clash of steel and shouted orders, the party was forced to decide whether control of the crossing was worth the cost in blood.

By the time the fighting ended, the bridge itself bore the scars of the conflict. Trust was broken, alliances strained, and word of the confrontation was already beginning to spread beyond the ravine.
```

### 🌟 Legendary Acknowledgments

Records mythic, symbolic, or world-altering moments of recognition, judgment, or transformation.

This section is OPTIONAL and most appropriate for pivotal encounters, trials, prophecies, or irreversible narrative milestones.

#### Example

```markdown
## Legendary Acknowledgments

As the last echoes of battle fade, ancient ward stones set into the bridge flicker briefly with a pale blue light before going dark once more. The crossing has endured many conflicts, and something old and unseen has taken notice of this one.
```

### 🖼️ Closing Image

Provides a final narrative snapshot that thematically or emotionally concludes the session.

This section often serves as a transition point into the next Save Point.

#### Example

```markdown
## Closing Image

As night falls, the broken silhouette of the bridge stands stark against the moonlit river. Fires burn on both banks, but no one dares cross. The path forward remains open—but at a cost.
```

### 🧾 Detailed Transcript

Contains optional verbatim dialogue, mechanical resolution, rolls, or moment-to-moment narration.

This section MAY be omitted entirely for narrative-focused sessions.

#### Example

```markdown
## Detailed Transcript

**Elara:** "Lower your weapons. No one needs to die here."  
**Captain Vorn:** "You should have turned back when you had the chance."

*Negotiation attempt fails.*

**GM:** The guard captain raises his hand. Archers loose their bolts, and the first strike shatters stone instead of flesh.

**Tomas:** "Enough! This ends now."

*Combat resolves. The guards retreat, carrying their wounded.*
```

---

## SLD Example

```markdown
---
SessionLogTitle: The Conflict at the Broken Bridge
SavePoint: TheConflictattheBrokenBridge.NRSP.md
InGameDate: 12th Day of Highsummer, Year 403
SessionDate: 2025-03-14
SessionDuration: 3h 45m
SessionNumber: 17
System: d7-RPG
Tags:
 - Bridge
 - Conflict
---

## Opening Scene

The fog hangs low over the Broken Bridge as the party approaches at dawn. The river below churns loudly, masking distant voices on the far side. Weathered banners hang from the stone pylons, their colors faded by rain and neglect. Even before words are exchanged, it is clear this crossing is not unguarded.

## Major Events

- **First Contact:** Armed guards halt the party at the bridge's edge and demand a toll far exceeding local custom.
- **Negotiation Fails:** Accusations of smuggling and espionage derail attempts at diplomacy.
- **Violence Erupts:** A crossbow bolt strikes the stone railing, splintering the fragile truce.
- **Structural Damage:** Fighting along the span damages the central support, leaving the bridge unstable.
- **Aftermath:** The guards withdraw, but control of the crossing remains uncertain.

## Important Interactions

- Elara challenges Captain Vorn's authority over the bridge and questions his mandate.
- Tomas intervenes to prevent the execution of a wounded guard after the fighting ends.
- A fleeing bandit is spared, leaving behind information about movements in nearby settlements.

## Session Narrative

What began as a tense standoff quickly spiraled into chaos. The narrow stone span offered little room for maneuvering, and every misstep threatened to send combatants tumbling into the river below. Amid the clash of steel and shouted orders, the party was forced to decide whether control of the crossing was worth the cost in blood.

By the time the fighting ended, the bridge itself bore the scars of the conflict. Trust was broken, alliances strained, and word of the confrontation was already beginning to spread beyond the ravine.

## Legendary Acknowledgments

As the last echoes of battle fade, ancient ward stones set into the bridge flicker briefly with a pale blue light before going dark once more. The crossing has endured many conflicts, and something old and unseen has taken notice of this one.

## Closing Image

As night falls, the broken silhouette of the bridge stands stark against the moonlit river. Fires burn on both banks, but no one dares cross. The path forward remains open—but at a cost.

## Detailed Transcript

**Elara:** "Lower your weapons. No one needs to die here."  
**Captain Vorn:** "You should have turned back when you had the chance."

*Negotiation attempt fails.*

**GM:** The guard captain raises his hand. Archers loose their bolts, and the first strike shatters stone instead of flesh.

**Tomas:** "Enough! This ends now."

*Combat resolves. The guards retreat, carrying their wounded.*
```
