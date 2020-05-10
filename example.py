import logging
import random

from alchemy import Logger

logging.basicConfig(level=logging.DEBUG)

# insert your personal token here
token = "..."
project = "default"

for gid in range(1):
    group = f"group_{gid}"
    for eid in range(2):
        experiment = f"experiment_{eid}"
        logger = Logger(
            token=token, experiment=experiment, group=group, project=project,
        )
        for mid in range(4):
            metric = f"metric_{mid}"
            # let's sample some random data
            n = 300
            x = random.randint(-10, 10)
            for _ in range(n):
                logger.log_scalar(metric, x)
                x += random.randint(-1, 1)
        logger.close()
