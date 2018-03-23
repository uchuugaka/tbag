# -*- coding:utf-8 -*-

from tbag.core.context import TornadoContext


def main():
    """ 启动程序
    """
    config_module = 'config'

    # 初始化 & 启动io loop
    TornadoContext(config_module).start()


if __name__ == '__main__':
    main()
