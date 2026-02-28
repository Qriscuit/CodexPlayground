# Project Brief — Layer-Aware Paint-Layer Cleanup Prototype

## Problem statement
Animation frame cleanup is often destructive: removing artifacts (dust, line jitter, small paint errors) can unintentionally alter artist-intended paint structure and temporal consistency across frames. We need a conservative cleanup tool that repairs defects while preserving original layer intent.

## Research paper key claims
Based on the repository source papers in `Docs/` (especially **Core Research Paper.pdf** and the two layer-aware planning docs), the project assumes:
1. **Layer awareness improves repair quality** versus flat pixel-space edits.
2. **Conservative repair strategy** (minimal edits constrained by confidence/structure priors) reduces overcorrection.
3. **Human-in-the-loop controls** are required for production use (artist approval, tuning, rollback).
4. **Temporal consistency** across nearby frames is essential to avoid flicker/regressions.

> Note: full-paper text extraction is not yet available in this environment; claims above are distilled from available document titles/metadata and should be tightened after importing paper excerpts.

## MVP scope
### Must-have (prototype)
- Load image sequence (or frame triplets).
- Detect candidate cleanup regions with tunable thresholding.
- Run conservative repair on selected regions only.
- Provide side-by-side before/after with diff overlay.
- Add manual accept/reject per region and full rollback.
- Export repaired frames and a change log.

### Later
- Full paint-layer decomposition integration.
- Sequence-level batch optimization.
- Learned priors/custom model fine-tuning.
- Plugin integration with animation DCC tools.

## Success metrics
- **Precision of proposed fixes** (accepted edits / proposed edits).
- **Overcorrection rate** (artist-rejected edits due to style/content drift).
- **Temporal stability score** (flicker metric over repaired sequences).
- **Human time saved** versus manual cleanup baseline.
- **Undo/recovery confidence** (no irreversible destructive edits).

## Non-goals
- Fully automatic “one-click” cleanup with no review.
- Repainting or restyling artistic intent.
- Solving all defect classes in v1.
- End-to-end studio pipeline integration in MVP.

## Technical constraints
- Start with deterministic, inspectable methods first; add ML only where needed.
- Preserve provenance: every edit must be auditable and reversible.
- Keep module boundaries clear: detection, repair, review UI, export.
- Optimize for prototype speed and iteration, not final production throughput.
- Work from local repo docs as primary source of truth.
