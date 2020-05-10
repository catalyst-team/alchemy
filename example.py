import logging
import random

from alchemy import Logger

logging.basicConfig(level=logging.DEBUG)

token = "..."
project = 'my-project'

for gid in range(1):
    for eid in range(2):
        for mid in range(3):
            metric = f"metric-{mid}"
            group = f"group-{gid}"
            experiment = f"experiment-{eid}"

            logger = Logger(token, experiment, group, project=project)

            n = 300
            x = random.random() * 20
            for i in range(n):
                logger.log_scalar(metric, x)
                x += random.random() * 2 - 1.01
            logger.close()
