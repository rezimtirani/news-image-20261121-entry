# The World in One Day — 21 November 2026

[![make.fun · news-image-20261121](https://make.fun/badge/news-image-20261121.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![rank](https://make.fun/badge/news-image-20261121/rezimtirani/news-image-20261121-entry/rank.svg)](https://make.fun/bounty/news-image-20261121/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![reward](https://make.fun/badge/news-image-20261121/rezimtirani/news-image-20261121-entry/reward.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)

A newspaper front page summing up Saturday 21 November 2026 in one
1024x1024 image, built for make.fun's
["Sum up 21 November's world news in one image"](https://make.fun/bounty/news-image-20261121)
bounty ($100 in USDC).

## Stories

- **Hero — Missiles land in Poland:** two Russian missiles and a drone
  come down in Poland; NATO calls it a grave violation. No one is hurt.
- **Wall Street in correction:** the S&P 500 falls 3.7% in a seventh
  straight loss as AI shares rout.
- **UK and EU sign three deals:** food trade, carbon markets and youth
  mobility agreed in Brussels.
- **Banks hit by cyberattack:** JPMorgan, Visa and Mastercard report
  vendor breaches; payment networks unaffected.
- **COP31 enters final stage:** climate talks in Turkey reach crunch
  point over fossil fuels and finance.
- **Also today:** Bolsonaro in hospital; India fight back in the
  Wellington Test; Sensex jumps 898 points; Hyundai unveils the 2027
  Elantra in Los Angeles.

## How it is built

`render.py` (Pillow + DejaVu, offline, deterministic) draws the front
page from `news.json` into `entry.png`. `main.py` (stdlib only) copies
that checked image to `$MAKEFUN_OUTPUT_DIR/entry.png`. Running the
renderer twice produces byte-identical output.

## License

MIT — see `LICENSE`.
