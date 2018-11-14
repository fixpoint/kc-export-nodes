# kc-export-nodes
Integration Tool for Kompira cloud to zabbix

## Requirements
- Python 3.6.5


## Install

### Install python modules
```
pip install openpyxl requests PyYAML
```

### Make config.yml

Rename config.yml.sample to config.yml

```
kompira_cloud:
  token: your_kompira_cloud_api_token
```

## Usage

```
kc_exporter.py https://yourspacename.cloud.kompira.jp/apps/sonar/networks/c3805f50-636b-4a75-8c41-e5efcd62ec1d/managed-nodes
2018-11-14 12:27:52,377 - [4826] - INFO - Get node list from KompiraCloud
2018-11-14 12:27:55,848 - [4826] - INFO - Export node list: csv
2018-11-14 12:27:55,849 - [4826] - INFO - Export node list: xlsx
```
