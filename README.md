<div align="center">

![Alchemy logo](https://raw.githubusercontent.com/catalyst-team/catalyst-pics/master/Catalyst.Ecosystem/PNG/alchemy-logo.png)

**Experiments logging & visualization**

![Build Status](https://github.com/catalyst-team/alchemy/workflows/CI/badge.svg)
[![CodeFactor](https://www.codefactor.io/repository/github/catalyst-team/alchemy/badge)](https://www.codefactor.io/repository/github/catalyst-team/alchemy)
[![Pipi version](https://img.shields.io/pypi/v/alchemy.svg)](https://pypi.org/project/alchemy/)
[![Docs](https://img.shields.io/badge/dynamic/json.svg?label=docs&url=https%3A%2F%2Fpypi.org%2Fpypi%2Fcatalyst%2Fjson&query=%24.info.version&colorB=brightgreen&prefix=v)](https://catalyst-team.github.io/catalyst/index.html)
[![PyPI Status](https://pepy.tech/badge/alchemy)](https://pepy.tech/project/alchemy)

[![Twitter](https://img.shields.io/badge/news-on%20twitter-499feb)](https://twitter.com/catalyst_core)
[![Telegram](https://img.shields.io/badge/channel-on%20telegram-blue)](https://t.me/catalyst_team)
[![Slack](https://img.shields.io/badge/Catalyst-slack-success)](https://join.slack.com/t/catalyst-team-core/shared_invite/zt-d9miirnn-z86oKDzFMKlMG4fgFdZafw)
[![Github contributors](https://img.shields.io/github/contributors/catalyst-team/alchemy.svg?logo=github&logoColor=white)](https://github.com/catalyst-team/alchemy/graphs/contributors)

</div>

Project [manifest](https://github.com/catalyst-team/catalyst/blob/master/MANIFEST.md). Part of [Catalyst Ecosystem](https://docs.google.com/presentation/d/1D-yhVOg6OXzjo9K_-IS5vSHLPIUxp1PEkFGnpRcNCNU/edit?usp=sharing):
- [Alchemy](https://github.com/catalyst-team/alchemy) - Experiments logging & visualization
- [Catalyst](https://github.com/catalyst-team/catalyst) - Accelerated Deep Learning Research and Development
- [Reaction](https://github.com/catalyst-team/reaction) - Convenient Deep Learning models serving

---

## Installation

Common installation:
```bash
pip install -U alchemy
```

Previous name `alchemy-catalyst` [![PyPI Status](https://pepy.tech/badge/alchemy-catalyst)](https://pepy.tech/project/alchemy-catalyst)

## Getting started

1. Goto [Alchemy](https://alchemy.host/) and get your personal token.

2. Run following **example.py**:
    ```python
    import random
    
    from alchemy import Logger
    
    # insert your personal token here
    token = "..."
    project = "default"
    
    for gid in range(1):
        group = f"group_{gid}"
        for eid in range(2):
            experiment = f"experiment_{eid}"
            logger = Logger(
                token=token,
                experiment=experiment,
                group=group,
                project=project,
            )
            for mid in range(4):
                metric = f"metric_{mid}"
                # let's sample some random data
                n = 300
                x = random.randint(-10, 10)
                for i in range(n):
                    logger.log_scalar(metric, x)
                    x += random.randint(-1, 1)
            logger.close()
    ```
3. Now you should see your metrics on [Alchemy](https://alchemy.host/).


## Catalyst.Ecosystem

1. Goto [Alchemy](https://alchemy.host/) and get your personal token.

2. Log your Catalyst experiment with **AlchemyLogger**:
    ```python
    from catalyst.dl import SupervisedRunner, AlchemyLogger

    runner = SupervisedRunner()
    runner.train(
        model=model,
        criterion=criterion,
        optimizer=optimizer,
        loaders=loaders,
        logdir=logdir,
        num_epochs=num_epochs,
        verbose=True,
        callbacks={
            "logger": AlchemyLogger(
                token="...", # your Alchemy token
                project="your_project_name",
                experiment="your_experiment_name",
                group="your_experiment_group_name",
            )
        }
    )
    ```
3. Now you should see your metrics on [Alchemy](https://alchemy.host/).

## Examples

For mode detailed tutorials, please follow [Catalyst examples](https://github.com/catalyst-team/catalyst/tree/master/examples#tutorials).
