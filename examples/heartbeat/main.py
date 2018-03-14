# -*- coding:utf-8 -*-

from tbag.core.context import TornadoContext


def main():
    config_module = 'config'
    t_context = TornadoContext(config_module)

    # 注册定时间隔任务
    from tbag.core.heartbeat import heartbeat
    import tasks
    heartbeat.register(tasks.do_something)

    t_context.start()


if __name__ == '__main__':
    main()
