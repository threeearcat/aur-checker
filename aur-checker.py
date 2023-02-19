#!/usr/bin/env python


import os
import git
import logging
import gi

logger = logging.getLogger()
logger.setLevel(logging.INFO)
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(logging.Formatter("[+] %(message)s"))
logger.addHandler(stream_handler)

gi.require_version("Notify", "0.7")
from gi.repository import Notify

Notify.init("AUR checker")


class aur_checker:
    class aur_package:
        def __init__(self, path: str):
            self.path = path
            self.name = os.path.basename(self.path)
            self.repo = git.Repo(path)

        def need_update(self) -> bool:
            logger.info("checking {}".format(self.name))
            origin = self.repo.remote()
            origin.fetch()
            logger.info("fetch done {}".format(self.name))

            origin_commit_id = origin.refs.master.commit
            local_commit_id = self.repo.refs.master.commit
            return not (origin_commit_id == local_commit_id)

    def __init__(self, directory: str):
        self.directory = directory
        self.pkgs_need_update = []

    def feed_pkg(self, pkg: aur_package):
        self.pkgs_need_update.append(pkg)

    def collect_pkgs_need_update(self):
        root_dir = self.directory
        pkgs = [
            dir
            for dir in os.listdir(root_dir)
            if os.path.isdir(os.path.join(root_dir, dir))
        ]
        for pkg in pkgs:
            pkg_path = os.path.join(root_dir, pkg)
            pkg = aur_checker.aur_package(pkg_path)
            if pkg.need_update():
                self.feed_pkg(pkg)

    def print_pkgs_need_update(self):
        pkgs = self.pkgs_need_update

        def notify(title, msg):
            notify = Notify.Notification.new(title, msg)
            notify.show()

        total = len(pkgs)
        title = "{} AUR packages need update".format(total)
        msg = "\n".join(list(map(lambda x: x.name, pkgs)))
        notify(title, msg)

    def run(self):
        self.collect_pkgs_need_update()
        self.print_pkgs_need_update()


def main(args):
    aur_directory = args.aur_directory
    logger.info("Check {}".format(aur_directory))
    checker = aur_checker(directory=aur_directory)
    checker.run()


if __name__ == "__main__":
    import argparse

    home = os.environ["HOME"]
    aur_directory_default = os.path.join(home, ".aur")

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--aur-directory",
        default=aur_directory_default,
        help="directory name that contains aur packages",
    )
    args = parser.parse_args()
    main(args)
