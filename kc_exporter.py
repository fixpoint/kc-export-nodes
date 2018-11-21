# coding: UTF-8

import yaml
import argparse
import os
import csv
import openpyxl
import json
import jmespath
import datetime

from collections import defaultdict
from lib.helper import logger
from lib.kompira_cloud import KompiraCloudAPI
from openpyxl.utils import get_column_letter
from openpyxl.styles.borders import Border, Side

accept_format = ['csv', 'xlsx']

time_format = '%Y-%m-%dT%H:%M:%SZ'


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

            if type(row[header]) == str:
                col_len = len(row[header])
            else:
                col_len = len(str(row[header]))
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
    target = ''
    if args.url[-13:] == 'managed-nodes':
        target = 'managed-nodes'
    elif args.url[-9:] == 'snapshots':
        target = 'snapshots'
    else:
        logger.error('%s invalid url.' % args.url)
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

    logger.info("Get list from KompiraCloud")

    res_json = kcapi.get_from_url(args.url, {'limit': 500})
    items = res_json['items']
    logger.debug(items)

    rows = []
    for item in items:
        if target == 'managed-nodes':  # Node List
            managedNodeId = jmespath.search('managedNodeId', item)
            pk_res_json = kcapi.get_from_url(args.url + '/%s/packages' % managedNodeId, {})
            logger.debug(pk_res_json)
            wu_res_json = kcapi.get_from_url(args.url + '/%s/windows-updates' % managedNodeId, {})
            logger.debug(wu_res_json)

            row = {
                'networkId': jmespath.search('networkId', item),
                'managedNodeId': managedNodeId,
                'displayName': jmespath.search('displayName', item),
                'hostName': json.dumps(jmespath.search('addresses[].hostnames[].hostname', item)),
                'ipAddress': json.dumps(jmespath.search('addresses[].addr', item)),
                'subnet': json.dumps(jmespath.search('addresses[].subnet', item)),
                'macaddr': json.dumps(jmespath.search('addresses[].macaddr', item)),
                'vendor': json.dumps(jmespath.search('addresses[].extraFields.macaddr.organizationName', item)),
                'systemFamily': jmespath.search('system.family', item),
                'systemVersion': jmespath.search('system.version', item),
                'systemSerial': jmespath.search('system.serial', item),
                'biosVendorName': jmespath.search('extraFields.bios.vendorName', item),
                'biosVersionNumber': jmespath.search('extraFields.bios.versionNumber', item),
                'motherboardVendorName': jmespath.search('extraFields.motherboard.vendorName', item),
                'motherboardModelNumber': jmespath.search('extraFields.motherboard.modelNumber', item),
                'motherboardVersionNumber': jmespath.search('extraFields.motherboard.versionNumber', item),
                'motherboardSerialNumber': jmespath.search('extraFields.motherboard.serialNumber', item),
                'productModelNumber': jmespath.search('extraFields.product.modelNumber', item),
                'productModelName': jmespath.search('extraFields.product.modelName', item),
                'productSerialNumber': jmespath.search('extraFields.product.serialNumber', item),
                'productVersionNumber': jmespath.search('extraFields.product.versionNumber', item),
                'productFirmwareVersionNumber': jmespath.search('extraFields.product.firmwareVersionNumber', item),
                'productVendorName': jmespath.search('extraFields.product.vendorName', item),
                'cpuNumberOfSockets': jmespath.search('extraFields.cpu.numberOfSockets', item),
                'cpuNumberOfCores': jmespath.search('extraFields.cpu.numberOfCores', item),
                'cpuNumberOfProcessors': jmespath.search('extraFields.cpu.numberOfProcessors', item),
                'memoryTotalSize': jmespath.search('extraFields.memory.totalSize', item),
                'storageTotalSize': jmespath.search('extraFields.storage.totalSize', item),
                'packagesTotal': jmespath.search('total', pk_res_json),
                'windowsupdatesTotal': jmespath.search('total', wu_res_json),
                'updatedAt': jmespath.search('updatedAt', item)
            }
            if args.zeroth:
                row['hostName'] = jmespath.search('addresses[0].hostnames[0].hostname', item)
                row['ipAddress'] = jmespath.search('addresses[0].addr', item)
                row['subnet'] = jmespath.search('addresses[0].subnet', item)
                row['macaddr'] = jmespath.search('addresses[0].macaddr', item)
                row['vendor'] = jmespath.search('addresses[0].extraFields.macaddr.organizationName', item)
        elif target == 'snapshots':  # Snapshot List
            startedAt = jmespath.search('task.startedAt', item)
            terminatedAt = jmespath.search('task.terminatedAt', item)

            deltaTime = datetime.timedelta()
            if startedAt and terminatedAt:
                deltaTime = datetime.datetime.strptime(terminatedAt, time_format) - datetime.datetime.strptime(startedAt, time_format)

            row = {
                'networkId': jmespath.search('networkId', item),
                'createdAt': jmespath.search('createdAt', item),
                'startedAt': startedAt,
                'terminatedAt': terminatedAt,
                'deltaTime': deltaTime,
                'ksockets': len(jmespath.search('ksockets', item)),
                'numberOfNodes': jmespath.search('numberOfNodes', item),
                'numberOfAddresses': jmespath.search('numberOfAddresses', item),
                'taskStatus': jmespath.search('task.status', item),
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
    parser.add_argument('--config_path', type=str, default='config.yml')
    parser.add_argument('--filename', type=str)
    parser.add_argument('--format', type=str, default='csv')
    parser.add_argument('--zeroth', action='store_true')
    args = parser.parse_args()
    main(args)
