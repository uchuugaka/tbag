# -*- coding:utf-8 -*-

from tbag.core.context import TornadoContext


def main():
    config_module = 'config'

    # 注册定时间隔任务
    from tbag.core.heartbeat import heartbeat
    import tasks
    heartbeat.register(tasks.do_something, "today", "happy")

    TornadoContext(config_module).start()


if __name__ == '__main__':
    main()
