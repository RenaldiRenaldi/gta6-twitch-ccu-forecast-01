# GTA VI Twitch CCU Forecast

[![Competition](https://make.fun/badge/gta6-twitch-ccu-forecast-01.svg)](https://make.fun/bounty/gta6-twitch-ccu-forecast-01)
[![Rank](https://make.fun/badge/gta6-twitch-ccu-forecast-01/RenaldiRenaldi/gta6-twitch-ccu-forecast-01/rank.svg)](https://make.fun/bounty/gta6-twitch-ccu-forecast-01)
[![Reward](https://make.fun/badge/gta6-twitch-ccu-forecast-01/RenaldiRenaldi/gta6-twitch-ccu-forecast-01/reward.svg)](https://make.fun/bounty/gta6-twitch-ccu-forecast-01)

This repository forecasts Twitch's concurrent viewers in the Grand Theft Auto VI category for UTC hours 2 through 24 of launch day. It reads one make.fun case from `MAKEFUN_INPUT_DIR` (default `/input`) and writes a deterministic five-quantile JSON forecast per case to `MAKEFUN_OUTPUT_DIR` (default `/output`).

The median follows a fixed UTC diurnal profile informed by comparable launch curves. Quantile spacing is expressed in log space, widens with forecast horizon, and is broader during the cross-region launch ramp.

Run locally with:

```sh
MAKEFUN_INPUT_DIR=input MAKEFUN_OUTPUT_DIR=out python3 main.py
```

MIT licensed.
