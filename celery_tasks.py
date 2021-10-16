# -*- coding:utf-8 -*-
from celery import Celery
from zhiHuHot_spider import *
from celery.schedules import crontab
from celery_config import *

# celery -A tasks worker --loglevel=info -P eventlet
# celery -A tasks beat
# app.config_from_object('celery_config')
# app.conf.timezone = 'Asia/Shanghai'
# CELERY_TIMEZONE = 'Asia/Shanghai'
# celery 使用的是UTC时间 比北京时间慢8小时

app = Celery('tasks', broker=BROKERS, backend=BACKEND)

app.conf.beat_schedule = {
    "celery_task": {
        "task": "tasks.zhihu_task",
        "schedule": crontab(hour="4,16", minute=30),
        # "args": (10, 10)
    }
}


@app.task
def zhihu_task():
    try:
        zhihu = ZhihuHot()
        html = zhihu.download_item()
        items = zhihu.clear_item(html)
        result = zhihu.save_item(items)
        if result:
            return 'zhihu_hot spider successful'
        else:
            return 'zhihu_hot spider failed'
    except Exception as e:
        print(e)
        return 'error' + str(e)


@app.task
def add(x, y):
    return "my task result: ", x + y
