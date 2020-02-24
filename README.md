<div align="center">

![Alchemy logo](https://raw.githubusercontent.com/catalyst-team/catalyst-pics/master/pics/alchemy_logo.png)

**Experiments logging & visualization**

[![Build Status](https://travis-ci.com/catalyst-team/alchemy.svg?branch=master)](https://travis-ci.com/catalyst-team/alchemy)
[![CodeFactor](https://www.codefactor.io/repository/github/catalyst-team/alchemy/badge)](https://www.codefactor.io/repository/github/catalyst-team/alchemy)
[![Pipi version](https://img.shields.io/pypi/v/alchemy-catalyst.svg)](https://pypi.org/project/alchemy-catalyst/)
[![Docs](https://img.shields.io/badge/dynamic/json.svg?label=docs&url=https%3A%2F%2Fpypi.org%2Fpypi%2Falchemy-catalyst%2Fjson&query=%24.info.version&colorB=brightgreen&prefix=v)](https://catalyst-team.github.io/alchemy-catalyst/index.html)
[![PyPI Status](https://pepy.tech/badge/alchemy-catalyst)](https://pepy.tech/project/alchemy-catalyst)

[![Twitter](https://img.shields.io/badge/news-on%20twitter-499feb)](https://twitter.com/catalyst_core)
[![Telegram](https://img.shields.io/badge/channel-on%20telegram-blue)](https://t.me/catalyst_team)
[![Slack](https://img.shields.io/badge/ODS-slack-red)](https://opendatascience.slack.com/messages/CGK4KQBHD)
[![Github contributors](https://img.shields.io/github/contributors/catalyst-team/alchemy.svg?logo=github&logoColor=white)](https://github.com/catalyst-team/alchemy/graphs/contributors)

</div>

Part of [Catalyst Ecosystem](https://docs.google.com/presentation/d/1D-yhVOg6OXzjo9K_-IS5vSHLPIUxp1PEkFGnpRcNCNU/edit?usp=sharing). Project [manifest](https://github.com/catalyst-team/catalyst/blob/master/MANIFEST.md).

---

## Installation

Common installation:
```bash
pip install -U alchemy-catalyst
```

## Getting started

1. Goto [Alchemy](https://alchemy.host/) and get your personal token.

2. Run following **example.py**:
    ```python
    import random

    from alchemy import Logger

    token = "..."  # insert your personal token here

    for gid in range(1):
        for eid in range(2):
            for mid in range(3):
                metric = f"metric_{mid}"
                group = f"group_{gid}"
                experiment = f"experiment_{eid}"

                logger = Logger(token, experiment, group)

                n = 300
                x = random.randint(-10, 10)
                for i in range(n):
                    logger.log_scalar(metric, x)
                    x += random.randint(-1, 1)
                logger.close()
    ```
3. Now you should see your metrics on [Alchemy](https://alchemy.host/).

## Example

For mode detailed tutorials, please follow [Catalyst examples](https://github.com/catalyst-team/catalyst/tree/master/examples#tutorials).
