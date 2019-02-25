# coding: UTF-8

import yaml
import argparse
import os
import json
import jmespath
import datetime
import importlib

from lib.helper import logger
from lib.kompira_cloud import KompiraCloudAPI
from lib.exporter import get_exporter, CSVExporter, ExcelExporter

def get_node_columns(datatype):
    if datatype == 'managed-nodes':
        rule_module = importlib.import_module('lib.column_managed_nodes')
        return rule_module.columns
    else:
        rule_module = importlib.import_module('lib.column_snapshot_nodes')
        return rule_module.columns

def export_nodes(nodes, target, format, filename, exporter):
    columns = get_node_columns(target)
    node_rows = []
    for node in nodes:
        row = {}
        for key, val in columns.items():
            try:
                if 'zeroth' in val:
                    v = jmespath.search(val['path_zeroth'], node)
                else:
                    v = jmespath.search(val['path'], node)
                if isinstance(v, list) or isinstance(v, dict):
                    v = json.dumps(v)
            except Exception:
                v = None
            row[key] = v
        node_rows.append(row)
    exporter.export(node_rows, filename)

def main(args):
    logger.info('Args value check')
    if not os.path.exists(args.config_path):
        logger.error('file "%s" is not found.' % args.config_path)
        exit(1)
    target = ''
    if args.url[-14:] == '/managed-nodes':
        target = 'managed-nodes'
    elif args.url[-6:] == '/nodes':
        target = 'snapshot-nodes'
    else:
        logger.error('%s invalid url.' % args.url)
        exit(1)

    exporter = get_exporter(args.format)
    if not exporter:
        logger.error('format "%s" is not supported.' % args.format)
        exit(1)

    if args.filename == "":
        logger.error('please input filename.' % args.format)
        exit(1)

    with open(args.config_path) as f:
        config = yaml.load(f)

    logger.info('Read config YML')
    if config['kompira_cloud'].get('basic_auth'):
        kcapi = KompiraCloudAPI(
            config['kompira_cloud']['token'],
            username=config['kompira_cloud']['basic_auth']['username'],
            password=config['kompira_cloud']['basic_auth']['password'],
        )
    else:
        kcapi = KompiraCloudAPI(config['kompira_cloud']['token'])

    logger.info("Get list from KompiraCloud")

    nodes = kcapi.get_items_from_webui_url(args.url)
    logger.debug(nodes)

    export_nodes(nodes, target, args.format, args.filename, exporter)
    logger.info('Output complete.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--url', type=str, required=True)
    parser.add_argument('--config_path', type=str, default='config.yml')
    parser.add_argument('--filename', type=str)
    parser.add_argument('--format', type=str, default='csv')
    parser.add_argument('--zeroth', action='store_true')
    args = parser.parse_args()
    main(args)
