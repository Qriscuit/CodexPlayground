# Ms. Pac-Man Deep Dive: Build, Team, Cost, and Sales

## Why this document exists

This is the "show your work" version of the story: where the game was made, which companies drove each stage, what team/time likely looked like, what development probably cost, and what sales likely looked like using source-backed ranges.

## 1) Where the game was made

- **Core development** happened in Massachusetts via GCC (MIT/Cambridge orbit, later Wayland house setup).
- **Commercial production/distribution** happened through Bally Midway in the Chicago area.
- **Manufacturing context** from Bally reporting places video/pinball factory activity in suburban Franklin Park, Illinois.
- **IP context** remained tied to Namco's Pac-Man rights structure.

## 2) Companies and teams that matter

- **General Computer Corporation (GCC)**: prototype origin, design iteration, and technical execution.
- **Bally Midway**: productization, manufacturing scale, and U.S. arcade distribution.
- **Namco**: core franchise/IP rights and royalty structure around Pac-Man.
- **Atari (contextual)**: earlier legal and contract environment that shaped GCC's business trajectory before Ms. Pac-Man.
- **Bandai Namco + AtGames (modern context)**: later rights/licensing conflict that affected legacy-era re-release decisions.

You can present this at company/team level and only use individual names if the class asks for creator credits.

## 3) Team size and timeline (man-month inputs)

Timeline anchors:

- GCC started *Crazy Otto* in late May or early June 1981.
- GCC and Midway signed the agreement on October 29, 1981.
- Public debut occurred on February 3, 1982.

Working timeline for estimation: roughly **8 months** (mid-1981 to early-1982).

Team-size anchors from oral history:

- A small core group initially living/working in the Wayland house.
- Additional engineers brought in during project push.
- Reasonable peak estimate: about **6-8 technical contributors**.

Man-month scenarios:

- Low: `4 FTE x 7 months = 28 man-months`
- Base: `6 FTE x 8 months = 48 man-months`
- High: `8 FTE x 9 months = 72 man-months`

## 4) Man-month rate and development cost estimate

Rate anchor:

- 1980 weekly earnings for beginning computer programmers:
- Boston: **$258/week**
- Chicago: **$311/week**

Rebasing method:

- Rebased to 1981-82 using SSA Average Wage Index growth.
- Added overhead multipliers (benefits/equipment/office) and tool costs.
- Tool-cost context includes Tektronix in-circuit emulators cited around **$25,000** each in the oral history.
- Implied monthly direct labor rate: about **$1,205-$1,453** per person-month.
- Implied fully loaded labor rate: about **$1,687-$2,324** per person-month.

Estimated total development cost:

- Low: **$77,238** (1981-82 dollars)
- Base: **$155,675** (1981-82 dollars)
- High: **$267,339** (1981-82 dollars)

CPI conversion to Jan. 2026 dollars:

- Low: **$261,064**
- Base: **$526,181**
- High: **$903,605**

Interpretation:

- Even the high case is small relative to the game's commercial outcome.
- Oral-history context that GCC was profit-sharing and cash-constrained suggests actual cash payroll could have been lower than the economic value of labor.

## 5) How much did it really sell?

### Unit sales (best-supported range)

- **117,000 units** (GCC oral-history statement).
- **125,000+ units by 1988** (Bally executive quote in LA Times; Guinness benchmark).
- Working range: **117k-125k**.

### Manufacturer sell-in estimate

Price anchors (period, not modern guesses):

- Trade ad list example: **$2,295**.
- Operator machine investment context: **$2,500-$3,000**.

Sell-in scenarios:

- Low: `117,000 x $2,295 = $268,515,000`
- Base: `121,000 x $2,650 = $320,650,000`
- High: `125,000 x $3,000 = $375,000,000`

### Operator coin-drop estimate

Period weekly earnings anchors:

- National video average: **$166-$171/week**
- Pac-Man benchmark in same survey: **$216/week**

Annualized installed-base scenarios:

- Conservative: `117,000 x $171 x 52 = $1,040,364,000`
- Base: `117,000 x $216 x 52 = $1,314,144,000`
- Upside: `125,000 x $260 x 52 = $1,690,000,000`

Interpretation:

- Billion-dollar annualized coin-drop scale is plausible under period earnings data.

## 6) What made this business story unique

- It was effectively a mod-to-mainstream conversion at industrial scale.
- It used a small-team, short-cycle build model before "lean product" language existed in games.
- The rights architecture solved short-term commercialization but created long-term friction.
- Oral-history claim that GCC made roughly **$10M** implies exceptional return on build effort.

## 7) Q&A-ready one-liners

- "I used period wages, period operator economics, and period sales references to build ranges."
- "I avoided fake precision and showed low/base/high with formulas."
- "The point is not one perfect number; the point is that every reasonable scenario still lands in blockbuster territory."

## Source links used here

- Fast Company oral history (archived): https://web.archive.org/web/20180615004912/https://www.fastcompany.com/3067296/the-mit-dropouts-who-created-ms-pac-man-a-35th-anniversary-oral-history
- Los Angeles Times archive (1988-07-11): https://www.latimes.com/archives/la-xpm-1988-07-11-fi-4238-story.html
- Guinness World Records entry: https://www.guinnessworldrecords.com/world-records/106051-most-successful-us-made-arcade-machine
- Occupational Outlook Handbook 1982-83 (BLS via FRASER): https://fraser.stlouisfed.org/title/occupational-outlook-handbook-3964/occupational-outlook-handbook-1982-83-edition-498549/content/pdf/bls_2000_1982_pt1?start_page=163
- SSA Average Wage Index: https://www.ssa.gov/oact/cola/AWI.html
- Play Meter issue page: https://archive.org/details/play-meter-volume-8-number-4-february-15th-1982
- Play Meter OCR text: https://archive.org/download/play-meter-volume-8-number-4-february-15th-1982/Play%20Meter%20-%20Volume%208,%20Number%204%20-%20February%2015th%201982_djvu.txt
- FRED CPIAUCSL CSV: https://fred.stlouisfed.org/graph/fredgraph.csv?id=CPIAUCSL
