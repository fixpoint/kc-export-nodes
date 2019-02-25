import os
import yaml
import json
import jmespath
import importlib

from . import column_managed_nodes
from . import column_snapshot_nodes
from .helper import logger
from .exporter import get_exporter
from .kompira_cloud import KompiraCloudAPI

def get_node_manager(url, format, config_path, zeroth):
    if url[-14:] == '/managed-nodes':
        return ManagedNodes(url, format, config_path, zeroth)
    elif url[-6:] == '/nodes':
        return SnapshotNodes(url, format, config_path, zeroth)
    else:
        logger.error('%s invalid url.' % url)
        exit(1)

class Nodes:
    def __init__(self, nodes_url, format, config_path, zeroth=False):
        self.exporter = get_exporter(format)
        self.nodes_url = nodes_url
        self.nodes = []
        self.only_zeroth = zeroth

        if not os.path.exists(config_path):
            logger.error('file "%s" is not found.' % config_path)
            exit(1)

        with open(config_path) as f:
            config = yaml.load(f)
        if config['kompira_cloud'].get('basic_auth'):
            self.kcapi = KompiraCloudAPI(
                config['kompira_cloud']['token'],
                username=config['kompira_cloud']['basic_auth']['username'],
                password=config['kompira_cloud']['basic_auth']['password']
            )
        else:
            self.kcapi = KompiraCloudAPI(config['kompira_cloud']['token'])

    def fetch_nodes(self):
        self.nodes = self.kcapi.get_items_from_webui_url(self.nodes_url)
        # logger.debug(self.nodes)

    def fetch_packages(self):
        if not self.nodes:
            self.fetch_nodes()
        for node in self.nodes:
            packages_path = self.get_packages_path(node)
            ps = self.kcapi.get_items_from_webui_url(packages_path)
            node['packages'] = ps

    def export_nodes(self, filename):
        logger.info("Export node list: %s" % self.exporter.format)

        node_rows = []
        for node in self.nodes:
            row = {}
            for key, val in self.node_columns.items():
                try:
                    v = self.get_node_path_value(node, val)
                    if isinstance(v, list) or isinstance(v, dict):
                        v = json.dumps(v)
                except Exception:
                    v = None
                row[key] = v
            node_rows.append(row)
        self.exporter.export(node_rows, filename)

    def export_packages(self, filename):
        logger.info("Export package list: %s" % self.exporter.format)

        package_rows = []
        for node in self.nodes:
            for package in node['packages']:
                row = {}
                for key, val in self.package_columns.items():
                    try:
                        # node_key が指定された場合、
                        # node_columns で指定されたpathを取得する
                        if 'node_key' in val:
                            v = self.get_node_path_value(node, self.node_columns[val['node_key']])
                        else:
                            v = jmespath.search(val['path'], package)
                        if isinstance(v, list) or isinstance(v, dict):
                            v = json.dumps(v)
                    except Exception:
                        v = None
                    row[key] = v
                package_rows.append(row)
        self.exporter.export(package_rows, filename)


    def get_node_path_value(self, node, column_dict):
        # node の中から、pathで指定された値を返す。
        #
        # column_dict = {
        #     'path': 'addresses[].hostnames[].hostname',
        #     'path_zeroth': 'addresses[0].@hostnames[0].hostname'
        # }
        # zeroth オプションが指定されている場合は path_zerothで指定されたpathの値を優先して返す
        if self.only_zeroth and ('path_zeroth' in column_dict):
            return jmespath.search(column_dict['path_zeroth'], node)
        else:
            return jmespath.search(column_dict['path'], node)


class ManagedNodes(Nodes):
    def __init__(self, url, format, config_path, zeroth):
        super().__init__(url, format, config_path, zeroth)
        self.datatype = 'managed-nodes'
        column_module = importlib.import_module('lib.column_managed_nodes')
        self.node_columns = column_module.node_columns
        self.package_columns = column_module.package_columns

    def get_packages_path(self, node):
        return os.path.join(self.nodes_url, node['managedNodeId'], 'packages')

class SnapshotNodes(Nodes):
    def __init__(self, url, format, config_path, zeroth):
        super().__init__(url, format, config_path, zeroth)
        self.datatype = 'snapshot-nodes'
        column_module = importlib.import_module('lib.column_snapshot_nodes')
        self.node_columns = column_module.node_columns
        self.package_columns = column_module.package_columns

    def get_packages_path(self, node):
        return os.path.join(self.nodes_url, node['nodeId'], 'packages')
