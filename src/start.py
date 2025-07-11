import sys
import getopt

import json

import logging

import monitor


def usage():
    """ Prints usage.
    """
    print("Usage: %s [-h | --help] [OPTION]..." % (sys.argv[0]))


def print_help():
    """ Prints detailled help.
    """
    usage()

    with open("help.txt", "r") as read_file:
        content = read_file.readlines()

    for line in content:
        print(line, end='')


def set_logger(logger, opts):
    """ Set the logger.

    @param logger the logger data,
    @param opts   the options to set the logger.
    """
    for opt, arg in opts:
        if opt in ("-l", "--level"):
            logger['level'] = arg
        elif opt in ("-o", "--output"):
            logger['output'] = arg
        elif opt in ("-F", "--format"):
            logger['format'] = arg
        elif opt in ("-D", "--datefmt"):
            logger['datefmt'] = arg

    logger_level = getattr(logging, logger['level'].upper())

    if not isinstance(logger_level, int):
        raise ValueError('Invalid log level: %s' % (logger['level']))

    logging.basicConfig(level = logger_level, filename = logger['output'],
                        format = logger['format'], datefmt = logger['datefmt'])
    logging.info("Logging level set to %s" % (logger['level']))


def set_mongodb(mongodb, opts):
    """ Set the MongoDB

    @param mongodb the MongoDB data,
    @param opts    the options to set the MongoDB.

    @return the MongoDB data set.
    """
    for opt, arg in opts:
        if opt in ("-H", "--host"):
            mongodb['host'] = arg
        elif opt in ("-u", "--username"):
            mongodb['username'] = arg
        elif opt in ("-p", "--password"):
            mongodb['password'] = arg
        elif opt in ("-d", "--dbname"):
            mongodb['dbname'] = arg
        elif opt in ("-c", "--collection"):
            mongodb['collection'] = arg

    return mongodb


def main():
    """ Main function.
    """
    OPTLIST      = "hl:o:F:D:H:u:p:d:c:"
    LONG_OPTLIST = [
        "help", "settings=", "param=",
        "level=", "output=", "format=", "datefmt=",
        "host=", "username=", "password=", "dbname=", "collection=",
    ]

    settings_file = "config/settings.json"
    param_file    = "config/param.json"

    try:
        opts, args = getopt.getopt(sys.argv[1:], OPTLIST, LONG_OPTLIST)
    except getopt.GetoptError as e:
        print(e)
        usage()
        sys.exit(1)

    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print_help()
            sys.exit()
        elif opt == "--settings":
            settings_file = arg
        elif opt == "--param":
            param_file = arg

    with open(settings_file, "r") as read_file:
        settings = json.load(read_file)

    set_logger(settings['logger'], opts)
    logging.debug("Logging initialised")

    monitor.run(set_mongodb(settings['mongodb'], opts), param_file,
                            settings['vtk']['output'])


if __name__ == "__main__":
    main()
