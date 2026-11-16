# Who gets paid at Wimbledon?

Live page: https://takizawadaiki.github.io/grand-slam-economics/

Wimbledon's prize money since 1968, adjusted for inflation, how the 2026 fund is split between champions and first-round losers, and how it compares with what the tournament earns.

## Findings

- The prize fund has gone from £26,150 in 1968 to £64.2 million in 2026. After inflation the 2025 fund was 3.5 times the 2000 fund and 5.7 times the 1990 fund.
- In 2026 the two singles main draws receive £47.3 million, 74% of the fund. The 128 first-round losers share 22% of that, more than any other round, and the two champions share 15%.
- A champion earns 45 times a first-round loser's £80,000, the widest gap of the four majors (Australian Open 28, Roland Garros 32, US Open 39).
- Prize money was about 12% of the tournament company's turnover in 2023 and 2024.
- The women's champion was paid 38% of the men's prize in 1968, about 90% from the late 1970s, and the same from 2007.

## Files

| Path | What it is |
| --- | --- |
| `data/` | Prize money, UK consumer prices, 2026 round-by-round prizes, the four majors in 2026 and two years of accounts, with `SOURCES.md` |
| `analysis.py` | Inflation adjustment, the split by round, the Gini coefficient; writes `results/results.json` |
| `tests/test_analysis.py` | Five tests |
| `index.html` | The page |

## Limits

Prize money is not income: players pay coaches, travel and tax from it. Accounts are shown for two years only. The history is Wimbledon's alone.

An earlier version of this page presented estimates of Grand Slam revenue, players' share of it, an "impact score" and a career simulator that could not be traced to sources. They have been removed.

```
python analysis.py
python -m pytest tests
```
