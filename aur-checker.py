#!/usr/bin/env python

class aur_checker():
    def __init__(self):
        pass

    def run(self):
        pass

def main(args):
    checker = aur_checker()
    checker.run()

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    args = parser.parse_args()
    main(args)
