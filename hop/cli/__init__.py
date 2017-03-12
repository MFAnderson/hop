import argparse
import os

def new_dir(string):
    if os.path.exists(string):
        raise argparse.ArgumentTypeError("must specify a new directory for the hop project")
    return string


def create_parser():
    config_parser = argparse.ArgumentParser(add_help=False)
    config_parser.add_argument('--hop-config', help='path to hop.yml file (defaults to ./hop.yml)')
    parser = argparse.ArgumentParser()
    sparser = parser.add_subparsers(dest='command')

    init_parser = sparser.add_parser('init', help='initializes hop')
    init_parser.add_argument('dest_dir', help='destination directory for hop')
    init_parser.add_argument('--skip-passwd', help='skip creating passwd file during init', dest='create_passwd', action='store_false')
    init_parser.set_defaults(create_passwd=True)

    sparser.add_parser('provision', help='provisions gocd', parents=[config_parser])

    configure_parser = sparser.add_parser('configure', help='configures gocd', parents=[config_parser])
    configure_parser.add_argument('context', help='A folder with a set of yml files for app definitions')
    configure_parser.add_argument('--host', help='GoCD host. e.g: localhost:8153')
    configure_parser.add_argument('--user', help='User with admin role')
    configure_parser.add_argument('--password', help='Password for user')

    return parser
