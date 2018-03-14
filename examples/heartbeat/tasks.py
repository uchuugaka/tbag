# -*- coding:utf-8 -*-

from tbag.utils import log as logger


def do_something(x, y, *args, **kwargs):
    hb_count = kwargs.get('heart_beat_count', 0)
    logger.debug('heart_beat_count:', hb_count)

    if hb_count % 10 == 0:
        logger.info('do something here every 10 seconds.')
        logger.info('x:', x, 'y:', y)
