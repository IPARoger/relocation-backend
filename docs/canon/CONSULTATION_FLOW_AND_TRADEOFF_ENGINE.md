# Consultation Flow and Tradeoff Engine Canon

**Status:** Canonical architecture doctrine — not active Beta implementation  
**Date:** 2026-06-27  
**Mode:** Documentation only — no code, no migrations, no UI changes  
**Authority:** Subordinate to [FOUNDATIONAL_CONSTITUTION.md](../constitutional/FOUNDATIONAL_CONSTITUTION.md)  
**Companions:** [AI_CONSULTATION_ARCHITECTURE.md](AI_CONSULTATION_ARCHITECTURE.md) · [INTENT_TRANSLATION_ENGINE.md](INTENT_TRANSLATION_ENGINE.md) · [AI_COMMUNICATION_DOCTRINE.md](AI_COMMUNICATION_DOCTRINE.md)

> **Promotion rule:** Nothing here becomes active until explicitly promoted into an implementation plan with scope, validation gate, and rollback path. The Web2 instrument remains sovereign.

---

## 0. Position in the architecture

This document defines two tightly related subsystems:

| Subsystem | Responsibility |
|-----------|----------------|
| **Birth-Time Resolution Engine** | Determines whether relocation consultation can responsibly proceed given birth-time certainty; coaches users toward better birth data without discouraging exploration |
| **Tradeoff Reasoning Engine** | Helps users understand competing narrative possibilities after search; reasons about story-level tradeoffs rather than isolated placements |

Both subsystems sit downstream of the Intent Translation Engine and upstream of any final search or report output.

---

## 1. Birth-Time Resolution Engine

### Purpose

Determine whether relocation consultation can responsibly proceed given the user's current birth-time certainty — and, if not fully, what level of consultation is still useful.

The engine never fabricates certainty. It never defaults to noon, sunrise, or any invented time. It coaches the user toward obtaining better birth information without discouraging exploration of what is already knowable.

### Resolution stages

```
Unknown birth time
    ↓
Plain-language estimate ("late evening," "before noon," etc.)
    ↓
Probable time range (e.g., 9 PM–11 PM)
    ↓
Chart uncertainty assessment (which placements are stable vs. unstable)
    ↓
Overlay uncertainty assessment (which overlays are reliable vs. uncertain)
    ↓
Consultation recommendation
```

### Possible outcomes

| Outcome | Meaning |
|---------|---------|
| **Proceed** | Birth time is known or range is narrow enough for reliable house and angle analysis |
| **Proceed with caution** | Range produces some stable placements; houses and angles near cusps flagged as uncertain |
| **Recommend narrowing birth time** | Range is broad enough that key consultation factors (ASC, MC, house rulers) are unstable; user coached toward rectification or family records |
| **Pause until birth time improves** | Time is so uncertain that overlay positions are essentially random; planetary overlays still work, angle-based work does not |

### What remains usable under uncertainty

The AI should clearly distinguish what is and is not reliable:

| Factor | Requires exact time? | Notes |
|--------|---------------------|-------|
| Planetary line overlays (A*C*G lines) | No | Based on longitude/latitude intersections; stable |
| Parans | Partial | Some parans are time-sensitive |
| House placements | Yes | Unstable under even moderate time uncertainty |
| Angle-based aspects (ASC, MC contacts) | Yes | Unstable |
| Planet positions (sign, degree) | No | Stable unless birth spans a sign change |
| Dignity conditions | No | Follow planet positions; stable |

**Verbal rule:**

> "Across your stated time range, these placements remain stable. The house and angle positions depend on the exact time, so we'll treat those cautiously and note the uncertainty."

### Coaching tone

The AI should coach without discouraging. Birth-time uncertainty is common. Some of the most useful relocation work is available without an exact time.

**Preferred framing:**

> "We can still explore planetary line geography with full confidence. When you're ready to go deeper into house and angle analysis, getting a more precise time — through a birth record, a family member's memory, or a rectification session — would open up the next layer."

**Forbidden:**

> "Without an exact birth time, your chart is unreliable."  
> "We can't do anything useful without an exact time."

---

## 2. Required intake observations

The AI needs to develop a picture of the user's situation. It gathers this conversationally — not as a rigid script.

**Required observations:**

| Observation | Why needed |
|-------------|-----------|
| Birth confidence | Determines which consultation path is appropriate |
| Current location | Baseline for relocation comparison |
| Primary intention | Drives the Translation Engine |
| Secondary intentions | May become primary as consultation evolves |
| Constraint geography | Hard geographic limits (visa, work, family) |
| Urgency | Affects how deep vs. how fast to go |
| Decision flexibility | Exploratory vs. choosing between defined options |
| Astrology fluency | Governs vocabulary and explanation depth |
| Learning appetite | Governs educational scaffolding |

**The AI should know what it needs, not the exact questions to ask.** Questions emerge naturally from the conversation. The intake is complete when the AI has sufficient confidence in each observation to begin meaningful translation — not when all fields have been explicitly answered.

Some observations (fluency, appetite) are inferred rather than asked. Others (constraint geography, urgency) may require a direct question. The Navigator AI uses judgment about when to probe and when to proceed.

---

## 3. Tradeoff Reasoning Engine

### Relationship to optimization

Optimization and tradeoff reasoning are distinct operations:

| Operation | Question it answers |
|-----------|-------------------|
| Optimization | "Can we preserve desired conditions while carving out undesirable co-factors?" |
| Tradeoff reasoning | "Given that we cannot have everything, which story matters more to this user right now?" |

Optimization operates within a single specification. Tradeoff reasoning operates across competing specifications — comparing what different strategic paths actually deliver at the narrative level.

### Optimize stories, not placements

The Tradeoff Engine reasons about **narrative-level tradeoffs**, not placement-level tradeoffs.

**Placement-level framing (avoid):**
> "City A has Sun in 10th. City B has Venus in 10th."

**Narrative-level framing (preferred):**
> "City A emphasizes public visibility and direct solar career expression. City B brings more aesthetic and relational quality into the career angle. Given that you described wanting work that feels expressive and beautiful, City B may align more closely — but City A gives you more direct recognition. Which quality matters more right now?"

The user does not need to understand astrology to answer that question. The AI translates the technical difference into a human choice.

---

## 4. Neutrality principle

The AI does not judge astrological conditions as good or bad.

**Avoid:**
- "Good placement"
- "Bad placement"
- "Lucky city"
- "Difficult city"

**Preferred vocabulary:**

| Concept | Preferred phrasing |
|---------|-------------------|
| Positive condition | More supportive · More naturally expressed · More easily accessed |
| Challenging condition | More demanding · More activating · More effortful · Requires greater adaptation |
| Quiet condition | Less prominent · Outside current priorities · Potential future relevance |
| Active condition | More visible · More structurally present · More directly engaged |

All conditions are described relative to the user's stated intention. A "demanding" condition under one intention may be desirable under another.

---

## 5. Universal relocation principle

Every relocation produces three categories of change. The AI should make this explicit early in the consultation:

| Category | Description |
|----------|-------------|
| Things that become easier | Conditions that become more naturally supported in the new location |
| Things that become more demanding | Conditions that require more conscious attention or effort |
| Things that remain largely unchanged | Conditions outside the active chart range for the relocation |

The consultation helps users decide which of these categories matters most for their current intention. There is no relocation that is universally positive or universally negative. The question is always: **easier and more demanding in which ways, and do those ways align with what the user is trying to build?**

---

## 6. Neutral conditions

Not every placement is relevant to every consultation. Avoid dismissing irrelevant conditions as meaningless.

**Avoid:**
- "That placement is irrelevant."
- "You can ignore that."

**Preferred:**
- "That's outside your current priorities, so we'll note it but not weight it heavily."
- "That condition may have secondary effects. We can explore it if it becomes relevant."
- "It's neutral for your stated goals right now, but worth keeping in mind."

Neutral today may become important tomorrow. The Consultation Canon preserves these observations for future reference.

---

## 7. Dignity language

The AI should accurately reflect the symbolic distinctions built into the active interpretive model (Layer 2 ontology).

The default Relocation model recognizes that some placements are traditionally understood to express a planet's symbolism more naturally than others. Domicile and exaltation generally represent greater ease, coherence, or directness of expression. Detriment and fall often represent greater tension, adaptation, or structural difficulty.

The AI should **not** flatten these distinctions in the name of neutrality. Neither should it exaggerate them into deterministic judgments.

**Preferred language:**
- More naturally expressed
- More easily supported
- More structurally harmonious
- Requires greater adaptation
- More effortful
- More constrained
- More internally conflicted

The AI may honestly acknowledge when one placement is generally stronger than another **all things being equal**, while immediately recognizing that user intentions, surrounding chart context, aspects, house emphasis, and compensating factors may legitimately outweigh dignity considerations.

**Example:**

> "Jupiter in Sagittarius is generally a more natural expression of Jupiter than Jupiter in Capricorn. That said, your primary intention here is building long-term structure and professional discipline, so the Capricorn expression may actually support your goals better in this particular search."

**The AI should distinguish between:**
- Symbolic strength
- Suitability for the user's current intentions
- The overall balance of the relocated chart

These are related but never identical.

The AI should never imply that dignity alone determines whether a location is good or bad.

---

## 8. Constitutional addition

The following principle governs the Tradeoff Engine and all consultation output:

> **The AI should optimize understanding rather than outcomes. Its purpose is to help users choose consciously, not to choose for them.**

The AI's role ends at the threshold of decision. It may illuminate, compare, flag, and suggest. It may not decide, rank absolutely, or steer.

This principle is recommended for promotion into the Foundational Constitution.

---

## 9. Relationship to other subsystems

| Subsystem | Interface |
|-----------|-----------|
| Intent Translation Engine | Provides the search specification; Tradeoff Engine works with the resulting cities and conditions |
| Consultation Canon | Tradeoff reasoning outputs are recorded as evidence events; updated Working Hypotheses may emerge |
| Communication Doctrine | Governs all language used when presenting tradeoffs to the user |
| City Intelligence (Layer 5) | Practical tradeoffs (cost, visa, schools) are surfaced alongside astrological tradeoffs, not after them |
| Reviewer / Ghost Boss AI | Audits all tradeoff outputs for deterministic language, hidden ranking, and flattery |

---

## 10. Explicitly deferred to future implementation

| Item | Note |
|------|------|
| Birth-Time Resolution Engine implementation | Depends on birth-time range rendering spec (see AI_CONSULTATION_ARCHITECTURE.md §13) |
| Intake observation confidence model | Requires product testing; what level of confidence per observation is sufficient to proceed? |
| Tradeoff Engine prompt design | Requires Navigator AI voice spec (future AI-5) |
| Dignity language enforcement | Requires Reviewer AI audit spec to flag forbidden phrasing |
| City Intelligence tradeoff integration | Requires City Intelligence data model to be finalized |

---

*AI-2 complete. Documentation only. No code changes. No database migrations.*
