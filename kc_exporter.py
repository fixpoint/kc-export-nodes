# coding: UTF-8

import os
import yaml
import argparse
import csv
import openpyxl
from openpyxl.styles.borders import Border, Side

from collections import defaultdict
from lib import helper
from lib.helper import logger
from lib.kompira_cloud import KompiraCloudAPI
from openpyxl.utils import get_column_letter


output_format = ['csv', 'xlsx']


def export_csv(rows, filename):
    logger.info("Export node list: csv")
    with open(filename, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def export_xlsx(rows, filename):
    logger.info("Export node list: xlsx")
    wb = openpyxl.Workbook()
    sheet = wb.create_sheet('NodeList')

    headers_border = Border(
        top=Side(style='medium', color='000000'),
        bottom=Side(style='medium', color='000000'),
        left=Side(style='medium', color='000000'),
        right=Side(style='medium', color='000000')
    )

    row_border = Border(
        top=Side(style='thin', color='000000'),
        bottom=Side(style='thin', color='000000'),
        left=Side(style='thin', color='000000'),
        right=Side(style='thin', color='000000')
    )

    # width調整のための文字数を格納する
    max_dims = defaultdict(lambda: 0)

    # Headers
    headers = rows[0].keys()
    for i, header in enumerate(headers):
        cell = sheet.cell(row=1, column=i+1, value=header)
        cell.border = headers_border  # border設定
        col_len = len(header)
        max_dims[header] = col_len

    # Values
    row_num = 2
    for row in rows:
        for i, header in enumerate(headers):
            value = row[header]
            cell = sheet.cell(row=row_num, column=i+1, value=value)
            cell.border = row_border  # border設定

            # cellのwidth調整
            # len関数にint型を入れるとエラーが発生
            if type(value) == int:
                value = str(value)
            col_len = len(value)
            if col_len > max_dims[header]:
                max_dims[header] = col_len
        row_num += 1

    # cell size
    for i, header in enumerate(headers):
        if max_dims[header]:
            sheet.column_dimensions[get_column_letter(i+1)].width = max_dims[header]
    if wb['Sheet']:
        wb.remove(wb['Sheet'])
    wb.save(filename)


def main(args):

    logger.info('Check args value.')
    if os.path.exists(args.yaml_path):
        with open(args.yaml_path) as f:
            config = yaml.load(f)
    else:
        logger.error('%s is not found.' % args.yaml_path)
        exit(1)

    if args.format not in output_format:
        logger.error('format %s is not support.' % args.format)
        exit(1)

    if config['kompira_cloud'].get('basic_auth'):
        kcapi = KompiraCloudAPI(
            config['kompira_cloud']['token'],
            username=config['kompira_cloud']['basic_auth']['username'],
            password=config['kompira_cloud']['basic_auth']['password'],
        )
    else:
        kcapi = KompiraCloudAPI(config['kompira_cloud']['token'])

    logger.info("Get node list from KompiraCloud")
    res_json = kcapi.get_from_url(args.nodelist_url, {'limit': 500})
    items = res_json['items']
    logger.debug(items)

    rows = []
    for item in items:
        managed_node_id = helper.dig(item, 'managedNodeId')
        res_json = kcapi.get_from_url(args.nodelist_url + '/%s/packages' % managed_node_id, {})
        packages_num = res_json['total']
        res_json = kcapi.get_from_url(args.nodelist_url + '/%s/windows-updates' % managed_node_id, {})
        windows_updates_num = res_json['total']

        data = {
            'networkId': helper.dig(item, 'networkId'),
            'managedNodeId': helper.dig(item, 'managedNodeId'),
            'displayName': helper.dig(item, 'displayName'),
            'hostName': helper.dig(item, 'addresses', 0, 'hostnames', 0, "hostname"),
            'ipAddress': helper.dig(item, 'addresses', 0, 'addr'),
            'subnet': helper.dig(item, 'addresses', 0, 'subnet'),
            'macaddr': helper.dig(item, 'addresses', 0, 'macaddr'),
            'vendor': helper.dig(item, 'addresses', 0, 'extraFields', 'macaddr', 'organizationName'),
            'systemFamily': helper.dig(item, 'system', 'family'),
            'systemVersion': helper.dig(item, 'system', 'version'),
            'systemSerial': helper.dig(item, 'system', 'serial'),
            'biosVendorName': helper.dig(item, 'extraFields', 'bios', 'vendorName'),
            'biosVersionNumber': helper.dig(item, 'extraFields', 'bios', 'versionNumber'),
            'motherboardVendorName': helper.dig(item, 'extraFields', 'motherboard', 'vendorName'),
            'motherboardModelNumber': helper.dig(item, 'extraFields', 'motherboard', 'modelNumber'),
            'motherboardVersionNumber': helper.dig(item, 'extraFields', 'motherboard', 'versionNumber'),
            'motherboardSerialNumber': helper.dig(item, 'extraFields', 'motherboard', 'serialNumber'),
            'productModelNumber': helper.dig(item, 'extraFields', 'product', 'modelNumber'),
            'productModelName': helper.dig(item, 'extraFields', 'product', 'modelName'),
            'productSerialNumber': helper.dig(item, 'extraFields', 'product', 'serialNumber'),
            'productVersionNumber': helper.dig(item, 'extraFields', 'product', 'versionNumber'),
            'productFirmwareVersionNumber': helper.dig(item, 'extraFields', 'product', 'firmwareVersionNumber'),
            'cpuNumberOfSockets': helper.dig(item, 'extraFields', 'cpu', 'numberOfSockets'),
            'cpuNumberOfCores': helper.dig(item, 'extraFields', 'cpu', 'numberOfCores'),
            'cpuNumberOfProcessors': helper.dig(item, 'extraFields', 'cpu', 'numberOfProcessors'),
            'memoryTotalSize': helper.dig(item, 'extraFields', 'memory', 'totalSize'),
            'storageTotalSize': helper.dig(item, 'extraFields', 'storage', 'totalSize'),
            'packageNum': packages_num,
            'windowsupdatesNum': windows_updates_num,
            'updatedAt': helper.dig(item, 'updatedAt'),
        }
        logger.debug(data)
        rows.append(data)

    if rows:
        if args.format == 'csv':
            export_csv(rows, '%s.csv' % args.filename)
        elif args.format == 'xlsx':
            export_xlsx(rows, '%s.xlsx' % args.filename)

    logger.info('Output complete.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--nodelist_url", type=str, required=True)
    parser.add_argument("--yaml_path", type=str, default='config.yml')
    parser.add_argument("--filename", type=str, required=True)
    parser.add_argument("--format", type=str, help='support format: csv, xlsx', default='csv')
    args = parser.parse_args()
    main(args)
