# kc-exporter.py
Integration Tool for Kompira cloud to csv(excel)

## Requirements
- Python 3.6.5


## Install

### Install python modules
```
pip install openpyxl requests PyYAML jmespath
```

### Make config.yml

Rename config.yml.sample to config.yml

```
kompira_cloud:
  token: your_kompira_cloud_api_token
```

## Usage

Output Kompira Cloud node list or snapshot list.


```
# node list(Excel)
kc_exporter.py --url https://yourspacename.cloud.kompira.jp/apps/sonar/networks/<networdId>/managed-nodes --filename kc_nodelist --format xlsx

# node list(csv)
kc_exporter.py --url https://yourspacename.cloud.kompira.jp/apps/sonar/networks/<networdId>/managed-nodes --filename kc_nodelist --format csv

# node list(0 array data only)
kc_exporter.py --url https://yourspacename.cloud.kompira.jp/apps/sonar/networks/<networdId>/managed-nodes --filename kc_nodelist --format xlsx --zeroth

# snapshot list(Excel)
kc_exporter.py --url https://yourspacename.cloud.kompira.jp/apps/sonar/networks/<networdId>/snapshots --filename kc_snapshotlist --format xlsx

```

## Options

* `--url URL`
    * node list url or snapshots url
    * example: `https://yourspacename.cloud.kompira.jp/apps/sonar/networks/<networdId>/managed-nodes `
    * example: `https://yourspacename.cloud.kompira.jp/apps/sonar/networks/<networdId>/snapshots`
* `--config_path FILEPATH`
    * config.yml path
    * default:`config.yml`
* `--filename FILEPATH`
    * output filename
* `--format OUTPUT_FORMAT`
    * `csv` or `xlsx`
    * default: `csv` 
* `--zeroth`
    * output only 0 array data. 

