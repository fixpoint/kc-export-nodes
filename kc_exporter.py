# coding: UTF-8

import yaml
import argparse
import re
import csv
import openpyxl

from pprint import pprint
from collections import defaultdict
from lib import helper
from lib.helper import logger
from lib.kompira_cloud import KompiraCloudAPI
from openpyxl.utils import get_column_letter

yaml_path = 'config.yml'

def export_csv(rows, filename):
    logger.info("Export node list: csv")
    with open(filename, 'w', newline='') as f:
        writer = csv.writer(f)
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        for row in rows:
            writer.writerow(row)

def export_xlsx(rows, filename):
    logger.info("Export node list: xlsx")
    wb = openpyxl.Workbook()
    sheet = wb.create_sheet('NodeList')

    # Headers
    headers = rows[0].keys()
    for i, col in enumerate(headers):
        sheet.cell(row=1, column=i+1, value=col)

    # Values
    max_dims = defaultdict(lambda: 0)
    row_num = 2
    for row in rows:
        for i, header in enumerate(headers):
            sheet.cell(row=row_num, column=i+1, value=row[header])
            col_len = len(row[header])
            if col_len > max_dims[header]:
                max_dims[header] = col_len
        row_num += 1

    # cell size
    for i, header in enumerate(headers):
        if max_dims[header]:
            sheet.column_dimensions[get_column_letter(i+1)].width = max_dims[header]

    wb.save(filename)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("nodelist_url", type=str)
    args = parser.parse_args()

    with open(yaml_path) as f:
        config = yaml.load(f)

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

    rows = [{
        'displayName' : helper.dig(item, 'displayName'),
        'hostName'    : helper.dig(item, 'addresses', 0, 'hostnames', 0),
        'ipAddress'   : helper.dig(item, 'addresses', 0, 'addr'),
        'vendor'      : helper.dig(item, 'extraFields', 'macaddr', 'organizationName'),
        'systemFamily': helper.dig(item, 'system', 'family'),
        'updatedAt'   : helper.dig(item, 'updatedAt'),
    } for item in items]

    if rows:
        export_csv(rows, 'kc_nodelist.csv')
        export_xlsx(rows, 'kc_nodelist.xlsx')

if __name__ == '__main__':
    main()
