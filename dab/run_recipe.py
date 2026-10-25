# Runs a Snowfakery recipe, with dab/plugins/ importable.
#
# This exists instead of the `snowfakery` console script because that script
# imports pkg_resources (snowfakery/utils/versions.py, only to check PyPI for
# a newer release). setuptools removed pkg_resources in 82.0.0, and every
# setuptools below 84.1.0 carries advisories (GHSA-h35f-9h28-mq5c,
# GHSA-xmj3-9gf7-h52w, PYSEC-2026-3447), so there is no setuptools version
# that both passes pip-audit and still provides pkg_resources. The library
# entry point snowfakery.generate_data does not import it.

import argparse
import os
import sys

from snowfakery import generate_data

PLUGINS = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'plugins')


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('recipe', help='the recipe YAML, e.g. snowfakery/example.yaml')
    parser.add_argument('--output-format', default='csv',
                        help='csv, json, txt, sql, ... (default: csv)')
    parser_output = parser.add_mutually_exclusive_group()
    parser_output.add_argument('--output-file', help='write one file')
    parser_output.add_argument('--output-folder', help='write into this folder')
    args = parser.parse_args(argv)

    # The recipes load their plugins by module name (faker_addons.Provider,
    # random_string.RandomString), so dab/plugins/ has to be on the path.
    if PLUGINS not in sys.path:
        sys.path.insert(0, PLUGINS)

    generate_data(
        args.recipe,
        output_format=args.output_format,
        output_file=args.output_file,
        output_folder=args.output_folder,
    )


if __name__ == '__main__':
    main()
