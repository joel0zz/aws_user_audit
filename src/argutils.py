import argparse as ap


def parse_args(values: dict, args):
    parser = ap.ArgumentParser(description=values['description'])
    for item in values['options']:
        parser.add_argument(item['short_option'], item['long_option'], required=item['required'], help=item['help'])
    return parser.parse_args(args)
