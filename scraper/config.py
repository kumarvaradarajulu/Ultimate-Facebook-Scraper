"""
Module that processes config.json and creates a config object
"""
import json
import os
from collections import namedtuple


scan_list = {
    0: "crawl.friends",
    1: "crawl.photos",
    2: "crawl.videos",
    3: "crawl.about",
    4: "crawl.posts",
}


class Config:
    def __init__(self):
        config_file = "config.json" if os.path.isfile("config.json") else "../config.json"
        with open(config_file) as f:
            self.config = json.loads(f.read(), object_hook=lambda d: namedtuple("DataConfig", d.keys())(*d.values()))

    def __getattr__(self, item):
        # See if the pieces of config uis being asked
        config_pieces = item.split(".")

        def multi_level_get_from_config(pieces, config, start):
            if config is None:
                return

            if len(pieces) == 1:
                return getattr(config, pieces[0], None)

            start += 1

            return multi_level_get_from_config(config_pieces[start:], getattr(config, pieces[0], None), start)

        config_value = multi_level_get_from_config(config_pieces, self.config, 0)

        return config_value


config = Config()


def check_config(func):
    """ Decorator to check config and call the function """
    def decorator(*args, **kwargs):
        config_path = scan_list[args[4]]
        enabled = getattr(config, config_path, False)
        if enabled or enabled is None:  # None is also considered enabled to ensure the tool works backwards
            return func(*args, **kwargs)
        else:
            print("Configured not to Crawl scan_list={}".format(scan_list[args[4]]))

    return decorator


def is_enabled(config_path):
    """ Decorator to get check if config is enabled """
    return getattr(config, config_path, True)


if __name__ == "__main__":
    print(getattr(config, "scrape.friend_intro.get", None))
