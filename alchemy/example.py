import random

from alchemy import Logger

token = '...'

for gid in range(3):
    for eid in range(5):
        for mid in range(10):
            metric = f'metric_{mid}'
            group = f'group_{gid}'
            experiment = f'experiment_{eid}'

            logger = Logger(token, experiment, group)

            n = 300
            x = random.randint(-10, 10)
            for i in range(n):
                logger.log_scalar(metric, x)
                x += random.randint(-1, 1)
            logger.close()
