# Implementation Roadmap (Derived from `Docs/` materials)

## Phase 1 — Understanding (Week 1)
- Normalize the research context into machine-usable docs.
- Actions:
  - Finalize `Docs/project-brief.md`.
  - Backfill exact equations and algorithm details in `Docs/paper-summary.md`.
  - Curate 2–3 representative defect-heavy frame sequences.
- Exit criteria:
  - Problem statement and success metrics are stable.
  - Paper assumptions and objective terms are explicit.

## Phase 2 — Design (Week 1–2)
- Define MVP architecture for conservative cleanup workflow.
- Suggested modules:
  - `detector` — candidate defect proposals.
  - `repair` — structure-aware constrained edit.
  - `review` — human acceptance/rejection UI.
  - `export` — repaired outputs + audit logs.
- Exit criteria:
  - Data contracts for frames, masks, confidence maps, logs.
  - API contract between detector/repair/review components.

## Phase 3 — Implementation (Week 2–4)
- Build PR-sized slices:
  1. Frame IO + sequence loader
  2. Candidate region detector (threshold + morphology baseline)
  3. Conservative local repair operator
  4. Confidence scoring + risk flags
  5. Review loop (accept/reject/undo)
  6. Export + change-log persistence
- Exit criteria:
  - End-to-end prototype runs on sample sequences.
  - Every edit is traceable and reversible.

## Phase 4 — Validation (Week 4)
- Evaluate against baseline/manual process:
  - Precision of proposed fixes
  - Overcorrection rate
  - Temporal flicker/stability metric
  - Time saved per shot/sequence
- Exit criteria:
  - MVP provides measurable value without quality regression.

## Phase 5 — Iteration (Week 5+)
- Improve weakest modules based on pilot feedback:
  - Better defect proposals (reduce false positives)
  - Better temporal constraints
  - Usability improvements in review UI
- Decide go/no-go for:
  - layer decomposition upgrades
  - ML-assisted repair priors
  - pipeline/toolchain integration

## Immediate implementation kickoff tasks
1. Confirm prototype stack.
2. Add exact equations from core paper.
3. Build minimal detector + repair pipeline on one short sequence.
4. Add review UI (even minimal CLI/web) before optimization.
