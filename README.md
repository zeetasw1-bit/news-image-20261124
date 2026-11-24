# The World in One Day — Tuesday 24 November 2026

[![make.fun · news-image-20261124](https://make.fun/badge/news-image-20261124.svg)](https://make.fun/bounty/news-image-20261124?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)
[![rank](https://make.fun/badge/news-image-20261124/zeetasw1-bit/news-image-20261124/rank.svg)](https://make.fun/bounty/news-image-20261124/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)
[![reward](https://make.fun/badge/news-image-20261124/zeetasw1-bit/news-image-20261124/reward.svg)](https://make.fun/bounty/news-image-20261124?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)

A newspaper-front-page image summing up the world news of **Tuesday 24 November 2026** — one day, one picture. The lead story is the COP31 climate summit in Antalya ending without a deal, the first UN climate summit since Copenhagen (2009) to fail. Around it: Israeli strikes in Gaza kill Hamas security chief Naeem Abu Nahel; Ukraine confirms drone strikes on Russian ships off Libya; fourteen nations back the world court's ruling that Myanmar committed genocide against the Rohingya; stocks soar as Jensen Huang returns as Nvidia CEO after Donald Trump's intervention; and fighting in DR Congo traps Ebola response teams. The footer also notes US states suing SpaceX over Grok images and a magnitude 5.6 quake in Nepal.

The image is drawn from scratch with Pillow (`generate_image.py`): masthead, red date banner, headline blocks with short summaries and simple pictogram illustrations. `main.py` (Python 3.13, standard library only) copies `entry.png` to the output directory byte for byte, so both runs produce identical output.

## Run

```sh
python3 generate_image.py
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

## Referral

Built for the make.fun bounty — join via https://make.fun/?ref=69vgdk1m
