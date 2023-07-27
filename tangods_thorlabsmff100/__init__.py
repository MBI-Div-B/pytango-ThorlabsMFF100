from .ThorlabsMFF100 import ThorlabsMFF100


def main():
    import sys
    import tango.server

    args = ["ThorlabsMFF100"] + sys.argv[1:]
    tango.server.run((ThorlabsMFF100,), args=args)
