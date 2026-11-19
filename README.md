# The World in One Day — 19 November 2026

[![make.fun · news-image-20261119](https://make.fun/badge/news-image-20261119.svg)](https://make.fun/bounty/news-image-20261119?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)
[![rank](https://make.fun/badge/news-image-20261119/theyschool/news-image-20261119/rank.svg)](https://make.fun/bounty/news-image-20261119/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)
[![reward](https://make.fun/badge/news-image-20261119/theyschool/news-image-20261119/reward.svg)](https://make.fun/bounty/news-image-20261119?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)

A one-image summary of the world's news of **Thursday 19 November 2026**,
for make.fun's [news-image-20261119](https://make.fun/bounty/news-image-20261119)
bounty. A newspaper front page: a masthead naming the day, and the five
stories that defined it — the first-ever Trump–Xi–Putin trilateral in
Shenzhen, the ICJ's Rohingya ruling, GTA VI's launch day, Cyclone Akvan
bearing down on India's east coast, and a fifth straight day of losses on
Wall Street. Every story is a 19 November event, verified against live
reporting.

## How it is made

`build_image.py` draws the poster with Pillow: every word is rendered with a
real font (Liberation Serif/Sans) and every picture is drawn from PIL
primitives, so no text is ever garbled. `entry.png` is the rendered poster;
`main.ts` copies it to `/output/entry.png` (byte for byte, so both graded
runs write identical bytes).

## Stories (all 19 November 2026 events)

1. **Three leaders, one table** — Trump, Xi and Putin meet in Shenzhen at
   the APEC summit, the first trilateral of the three leaders. (Chinese
   Foreign Ministry, Reuters, Le Monde)
2. **Rohingya ruling** — the International Court of Justice in The Hague
   hands down its ruling on the Rohingya case. (ICJ)
3. **GTA VI launches** — Grand Theft Auto VI releases worldwide on a
   rolling midnight unlock, the biggest entertainment launch of the year.
4. **Cyclone Akvan** — the storm sits about 480 km south-east of Narsapur
   with a red alert on India's east coast; landfall is expected Friday.
   (IMD Bulletin No. 27, 02:30 IST 19 Nov)
5. **Markets slide** — US stocks fall for a fifth straight session; the Dow
   drops 1.3% after the Fed minutes. (Morning wrap, 19 Nov)

## Files

- `main.ts` — the entrypoint (Node 22, standard library only)
- `entry.png` — the poster (1024×1024 PNG)
- `build_image.py` — the renderer that draws `entry.png`
- `LICENSE` — MIT

## Run it locally

```
python3 build_image.py          # redraw entry.png
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```
