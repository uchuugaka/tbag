# -*- coding:utf-8 -*-

from tbag.core.context import TornadoContext


def main():
    config_module = 'config'
    TornadoContext(config_module).start()


if __name__ == '__main__':
    main()
