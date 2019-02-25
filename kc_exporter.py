# coding: UTF-8
import argparse

from lib.helper import logger
from lib.node_manager import get_node_manager

def main(args):
    logger.info('Args value check')
    if args.filename == "":
        logger.error('please input filename.')
        exit(1)
    node_manager = get_node_manager(args.url, args.format, args.config_path, args.zeroth)
    logger.info("Get list from KompiraCloud")
    node_manager.fetch_nodes()
    node_manager.export_nodes(args.filename)
    if args.package_filename:
        node_manager.fetch_packages()
        node_manager.export_packages(args.package_filename)
    logger.info('Output complete.')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--url', type=str, required=True)
    parser.add_argument('--config_path', type=str, default='config.yml')
    parser.add_argument('--filename', type=str)
    parser.add_argument('--package_filename', type=str, default=None)
    parser.add_argument('--format', type=str, default='csv')
    parser.add_argument('--zeroth', action='store_true')
    args = parser.parse_args()
    main(args)
