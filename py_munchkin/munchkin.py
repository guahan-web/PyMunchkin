import argparse
from py_munchkin.utils.die import *

def roll(args):
    die = Die(args.sides)
    value = die.roll()
    print("Dice roll: %d" % (value))

def main():
    parser = argparse.ArgumentParser(description="Munchkin")
    # Add your CLI commands, options, and arguments here

    # Create parser for the "roll" command
    subparsers = parser.add_subparsers(help='sub-command help')

    roll_parser = subparsers.add_parser('roll', help='roll help')
    roll_parser.add_argument('--sides', type=int, default=6, help='--sides help')
    roll_parser.set_defaults(func=roll)

    args = parser.parse_args()
    args.func(args)


if __name__ == '__main__':
    main()
