# Distilled Paper Summary — Layer-Aware Conservative Cleanup

## Source documents
- `Docs/Core Research Paper.pdf`
- `Docs/Layer-Aware Animation Frame Cleanup Tool for Conservative Paint-Layer Repair.pdf`
- `Docs/Practical Prototype Plan for a Layer-Aware Paint-Layer Cleanup Tool.pdf`
- `Docs/Idea.pdf`

## Assumptions
- Defects are typically sparse relative to frame area.
- Layer/structure-aware repair preserves intent better than global denoising/inpainting.
- Artists need confidence-gated automation and explicit control.
- Neighboring-frame context helps prevent temporal artifacts.

## Core logic (high level)
1. Identify probable defect regions.
2. Estimate local structure/layer constraints.
3. Apply conservative repair bounded by confidence + structure priors.
4. Score edit risk and surface for artist review.
5. Propagate accepted logic across neighboring frames with temporal checks.

## Equations / formal logic (to be filled from full text)
Because PDF text extraction is currently unavailable in this runtime, capture the exact equations here once copied from the research paper:
- Objective/loss for conservative repair
- Confidence function and thresholding rule
- Temporal consistency term
- Any structural regularization terms

Placeholder notation for implementation planning:
- Defect mask: `M_t`
- Frame at time `t`: `I_t`
- Repaired frame: `\hat{I}_t`
- Confidence map: `C_t`
- Minimized objective: `L = L_data + \lambda_s L_structure + \lambda_t L_temporal`

## Required inputs
- Frame sequence (ordered images).
- Optional rough layer/region hints.
- User-configurable thresholds and repair strength.

## Outputs
- Repaired frames.
- Region-level confidence + decision metadata.
- Audit trail of accepted/rejected edits.

## Known limitations
- Without true layer decomposition, some edits may still leak across semantic boundaries.
- Conservative mode may miss subtle defects (recall trade-off).
- Temporal consistency can conflict with per-frame perfection.
- Current summary needs exact-paper equation backfill.
