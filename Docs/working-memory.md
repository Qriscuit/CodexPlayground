# Working Memory

## Key decisions
- Use `Docs/project-brief.md` as source-of-truth summary.
- Begin with conservative, human-reviewed cleanup flow.
- Prioritize reversibility and change auditability.

## Current assumptions
- The core approach is layer-aware and conservative by design.
- Temporal consistency is required for sequence quality.
- MVP should prove operator value, not full autonomy.

## Open questions
- Exact equations/thresholding from core paper.
- Preferred prototype stack (Python desktop, web app, plugin).
- Expected frame formats, sizes, and sequence lengths.
- Availability of labeled defect examples for validation.

## Risks
- Paper details may alter objective function choices.
- Overly aggressive defaults can reduce trust.
- Lack of benchmark dataset could hide regressions.
