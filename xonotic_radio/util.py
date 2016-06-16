import configparser
import time
import sys
import os


def reporthook(count, block_size, total_size):

    global start_time

    if count == 0:
        start_time = time.time()
        return
    duration = time.time() - start_time
    progress_size = int(count * block_size)
    speed = int(progress_size / (1024 * duration))
    percent = int(count * block_size * 100 / total_size)
    sys.stdout.write("\r...%d%%, %d MB, %d KB/s, %d seconds passed. " %
                    (percent, progress_size / (1024 * 1024), speed, duration))
    sys.stdout.flush()


def read_config(config_file):

    if not os.path.isfile(config_file):
        raise SystemExit(config_file + ' not found, please create one.')

    config = configparser.ConfigParser()

    config.read(config_file)

    return config['default'], config['endpoints']
