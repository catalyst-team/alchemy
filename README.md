<div align="center">

![Alchemy logo](https://raw.githubusercontent.com/catalyst-team/catalyst-pics/master/pics/alchemy_logo.png)

[![Telegram](https://img.shields.io/badge/news-on%20telegram-blue)](https://t.me/catalyst_team)
[![Gitter](https://badges.gitter.im/catalyst-team/community.svg)](https://gitter.im/catalyst-team/community?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge)
[![Spectrum](https://img.shields.io/badge/chat-on%20spectrum-blueviolet)](https://spectrum.chat/catalyst)
[![Slack](https://img.shields.io/badge/ODS-slack-red)](https://opendatascience.slack.com/messages/CGK4KQBHD)
[![Donate](https://raw.githubusercontent.com/catalyst-team/catalyst-pics/master/third_party_pics/patreon.png)](https://www.patreon.com/catalyst_team)

**Alchemy**. Experiments logging & visualization.
</div>

#### Installation

Common installation:
```bash
pip install -U alchemy-catalyst
```

## Quick start

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