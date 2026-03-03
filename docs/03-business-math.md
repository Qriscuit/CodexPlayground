# Business Math Workbook (Use in Presentation)

> This version is built from period data points instead of generic assumptions.

## A) Hard inputs (from sources)

- Unit sales anchors: **117,000** (GCC oral history) and **125,000+** by 1988 (Bally/LA Times; Guinness).
- Period machine price anchors:
- Trade-magazine ad example: **$2,295** retail list (Play Meter, Feb. 1982).
- Operator investment context: **$2,500-$3,000 cash per machine** (Play Meter, Feb. 1982 reporting).
- Period weekly earnings anchors:
- National video average: around **$166-$171/week**.
- *Pac-Man* listing in the same survey: **$216/week**.

## B) Manufacturer sell-in revenue (cabinet sales)

Formula:
- `Units sold x machine price`

Scenarios:
- Low: `117,000 x $2,295 = $268,515,000`
- Base: `121,000 x $2,650 = $320,650,000`
- High: `125,000 x $3,000 = $375,000,000`

Readout:
- A realistic range is about **$269M-$375M** in cabinet sell-in.

## C) Operator coin-drop revenue (arcade floor economics)

Formula:
- `Installed units x weekly gross x 52`

Scenarios:
- Conservative (national avg): `117,000 x $171 x 52 = $1,040,364,000`
- Base (*Pac-Man* benchmark): `117,000 x $216 x 52 = $1,314,144,000`
- Upside (top-tier hit level): `125,000 x $260 x 52 = $1,690,000,000`

Readout:
- During strong years, installed-base coin-drop likely sat in a **$1.0B-$1.7B annualized** band.

## D) Development cost model (man-month + labor rate)

Timeline/team anchors:
- Build starts late May/early June 1981 and ships publicly in Feb. 1982.
- Team appears to be small, roughly **6-8 technical contributors** at peak.

Wage anchor:
- 1980 weekly earnings for beginning computer programmers:
- **Boston: $258**
- **Chicago: $311**
- (Occupational Outlook Handbook 1982-83 edition)

Adjustment:
- Rebased from 1980 to 1981-82 using SSA Average Wage Index growth.
- Added overhead/tools assumptions for fully loaded cost.
- Implied direct labor rate: about **$1,205-$1,453 per person-month**.
- Implied fully loaded labor rate: about **$1,687-$2,324 per person-month**.

Scenario outputs:
- Low: **28 man-months**, total about **$77,238** (1981-82$)
- Base: **48 man-months**, total about **$155,675** (1981-82$)
- High: **72 man-months**, total about **$267,339** (1981-82$)

CPI conversion:
- Using CPIAUCSL, this is roughly **$261k-$904k** in Jan. 2026 dollars.

## E) ROI sanity check

- GCC oral history says it made roughly **$10M** on the arcade deal.
- Against estimated build costs above, that implies a very large multiple even in high-cost scenarios.
- Business implication: this was a high-leverage product (small build, massive distribution).

## F) One-line defense in Q&A

Use this sentence:

> "I used period wage data, period trade economics, and transparent low/base/high scenarios, so the range is defensible even if exact ledgers are unavailable."

## Source links for this workbook

- https://web.archive.org/web/20180615004912/https://www.fastcompany.com/3067296/the-mit-dropouts-who-created-ms-pac-man-a-35th-anniversary-oral-history
- https://www.latimes.com/archives/la-xpm-1988-07-11-fi-4238-story.html
- https://www.guinnessworldrecords.com/world-records/106051-most-successful-us-made-arcade-machine
- https://fraser.stlouisfed.org/title/occupational-outlook-handbook-3964/occupational-outlook-handbook-1982-83-edition-498549/content/pdf/bls_2000_1982_pt1?start_page=163
- https://www.ssa.gov/oact/cola/AWI.html
- https://archive.org/details/play-meter-volume-8-number-4-february-15th-1982
- https://archive.org/download/play-meter-volume-8-number-4-february-15th-1982/Play%20Meter%20-%20Volume%208,%20Number%204%20-%20February%2015th%201982_djvu.txt
- https://fred.stlouisfed.org/graph/fredgraph.csv?id=CPIAUCSL
