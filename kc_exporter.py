# coding: UTF-8

import yaml
import argparse
import os
import csv
import openpyxl

from collections import defaultdict
from lib import helper
from lib.helper import logger
from lib.kompira_cloud import KompiraCloudAPI
from openpyxl.utils import get_column_letter
from openpyxl.styles.borders import Border, Side

accept_format = ['csv', 'xlsx']


border = Border(
    top=Side(style='thin', color='000000'),
    bottom=Side(style='thin', color='000000'),
    left=Side(style='thin', color='000000'),
    right=Side(style='thin', color='000000')
)


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

    max_dims = defaultdict(lambda: 0)
    # Headers
    headers = rows[0].keys()
    for i, header in enumerate(headers):
        cell = sheet.cell(row=1, column=i+1, value=header)
        max_dims[header] = len(header)

        cell.border = border

    # Values
    row_num = 2
    for row in rows:
        for i, header in enumerate(headers):
            cell = sheet.cell(row=row_num, column=i+1, value=row[header])

            cell.border = border

            if type(row[header]) == int:
                col_len = len(str(row[header]))
            else:
                col_len = len(row[header])
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
    logger.info('Args value check')
    if not os.path.exists(args.config_path):
        logger.error('file "%s" is not found.' % args.config_path)
        exit(1)
    if args.format not in accept_format:
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

    logger.info("Get node list from KompiraCloud")
    res_json = kcapi.get_from_url(args.nodelist_url, {'limit': 500})
    items = res_json['items']
    logger.debug(items)

    rows = []
    for item in items:
        managedNodeId = helper.dig(item, 'managedNodeId')
        pk_res_json = kcapi.get_from_url(args.nodelist_url + '/%s/packages' % managedNodeId, {})
        logger.debug(pk_res_json)
        wu_res_json = kcapi.get_from_url(args.nodelist_url + '/%s/windows-updates' % managedNodeId, {})
        logger.debug(wu_res_json)

        row = {
            'networkId': helper.dig(item, 'networkId'),
            'managedNodeId': managedNodeId,
            'displayName': helper.dig(item, 'displayName'),
            'hostName': helper.dig(item, 'addresses', 0, 'hostnames', 0, 'hostname'),
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
            'productVendorName': helper.dig(item, 'extraFields', 'product', 'vendorName'),
            'cpuNumberOfSockets': helper.dig(item, 'extraFields', 'cpu', 'numberOfSockets'),
            'cpuNumberOfCores': helper.dig(item, 'extraFields', 'cpu', 'numberOfCores'),
            'cpuNumberOfProcessors': helper.dig(item, 'extraFields', 'cpu', 'numberOfProcessors'),
            'memoryTotalSize': helper.dig(item, 'extraFields', 'memory', 'totalSize'),
            'storageTotalSize': helper.dig(item, 'extraFields', 'storage', 'totalSize'),
            'packagesTotal': helper.dig(pk_res_json, 'total'),
            'windowsupdatesTotal': helper.dig(wu_res_json, 'total'),
            'updatedAt': helper.dig(item, 'updatedAt'),
        }
        rows.append(row)

    if args.format == 'csv':
        export_csv(rows, '%s.csv' % args.filename)
    elif args.format == 'xlsx':
        export_xlsx(rows, '%s.xlsx' % args.filename)

    logger.info('Output complete.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--url', type=str, required=True)
    parser.add_argument('--type', type=str, required=True)
    parser.add_argument('--config_path', type=str, default='config.yml')
    parser.add_argument('--filename', type=str)
    parser.add_argument('--format', type=str, default='csv')
    args = parser.parse_args()
    main(args)
