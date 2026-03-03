# Sources, Evidence Quality, and Confidence Notes

## Core source stack (with direct links)

1. **Fast Company oral history (archived)**
- URL: https://web.archive.org/web/20180615004912/https://www.fastcompany.com/3067296/the-mit-dropouts-who-created-ms-pac-man-a-35th-anniversary-oral-history
- Used for: team names, development timeline, locations, 117,000-unit claim, GCC "$10 million" claim, Atari contract context.
- Confidence: **medium-high** (first-person interviews, but retrospective).

2. **Los Angeles Times archive (1988-07-11)**
- URL: https://www.latimes.com/archives/la-xpm-1988-07-11-fi-4238-story.html
- Used for: Bally executive statement that company sold more than 125,000 Ms. Pac-Man machines; Franklin Park factory context.
- Confidence: **high** for quoted executive statements.

3. **Guinness World Records entry**
- URL: https://www.guinnessworldrecords.com/world-records/106051-most-successful-us-made-arcade-machine
- Used for: 125,000 cabinets by 1988 benchmark.
- Confidence: **medium-high** (compiled reference source).

4. **Occupational Outlook Handbook 1982-83 (BLS via FRASER)**
- URL: https://fraser.stlouisfed.org/title/occupational-outlook-handbook-3964/occupational-outlook-handbook-1982-83-edition-498549/content/pdf/bls_2000_1982_pt1?start_page=163
- Used for: 1980 weekly earnings of beginning computer programmers (Boston $258, Chicago $311) to build man-month rates.
- Confidence: **high** for wage anchor inputs.

5. **SSA Average Wage Index table**
- URL: https://www.ssa.gov/oact/cola/AWI.html
- Used for: wage-growth rebasing from 1980 wages to 1981-82 project period.
- Confidence: **high**.

6. **Play Meter trade issue (1982-02-15) + OCR text**
- Item URL: https://archive.org/details/play-meter-volume-8-number-4-february-15th-1982
- OCR URL: https://archive.org/download/play-meter-volume-8-number-4-february-15th-1982/Play%20Meter%20-%20Volume%208,%20Number%204%20-%20February%2015th%201982_djvu.txt
- Used for: period machine-price anchors ($2,295 list example; $2,500-$3,000 machine investment context), weekly earnings anchors ($166-$171 national video average; Pac-Man $216).
- Confidence: **medium** (trade source + OCR can introduce transcription noise).

7. **FRED CPI series (BLS CPIAUCSL)**
- URL: https://fred.stlouisfed.org/graph/fredgraph.csv?id=CPIAUCSL
- Used for: converting 1981-82 dollar estimates to Jan. 2026 dollars (ratio-based estimate).
- Confidence: **high** for inflation conversion math.

8. **Modern legal reporting (optional legal slide support)**
- Polygon (2019): https://www.polygon.com/2019/9/26/20886032/ms-pac-man-lawsuit-bandai-namco-atgames-rights-royalties
- Polygon (2022): https://www.polygon.com/23015420/ms-pac-man-pac-land-bandai-namco-atgames-lawsuit
- GamesIndustry.biz (2020): https://www.gamesindustry.biz/articles/2020-11-04-bandai-namco-atgames-resolve-legal-dispute
- Used for: modern rights dispute timeline and release impact context.
- Confidence: **medium** (journalistic reporting; good for timeline, not contract text).

## Confidence framework for your presentation

- **High confidence**
- Dated milestones (1981 agreement period, 1982 launch, 1988 unit benchmark context).
- Wage-index and inflation-index mechanics.

- **Medium confidence**
- Exact unit total between 117k and 125k (different credible reports).
- Derived revenue ranges from period price/earnings anchors.

- **Low confidence**
- Any single "exact" all-time revenue number without method disclosure.

## Citation behavior for slides

- Add one source line at bottom-right of every number-heavy slide.
- Show formulas directly on the slide for estimated values.
- Use ranges, not fake precision, when ledgers are unavailable.

## Safe wording templates

- "The best-supported range I found is 117k-125k units, based on GCC oral-history and Bally/Guinness references."
- "I modeled revenue from period machine pricing and period weekly earnings, then showed low/base/high cases."
- "Where exact ledgers were unavailable, I used transparent assumptions and showed the calculation."
