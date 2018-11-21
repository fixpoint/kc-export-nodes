# kc-export-nodes
Export Nodes data on Kompira cloud

[Japanese README](README-ja.md)

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

Output Kompira cloud node list or snapshot list to local file.

```
# Output node list to xlsx file
kc_exporter.py --url https://yourspacename.cloud.kompira.jp/apps/sonar/networks/<networkId>/managed-nodes --filename kc_nodelist --format xlsx

# Output node list to csv file
kc_exporter.py --url https://yourspacename.cloud.kompira.jp/apps/sonar/networks/<networkId>/managed-nodes --filename kc_nodelist --format csv

# node list(0 array data only)
kc_exporter.py --url https://yourspacename.cloud.kompira.jp/apps/sonar/networks/<networkId>/managed-nodes --filename kc_nodelist --format xlsx --zeroth

# Output snapshot-node list to xlsx file
kc_exporter.py --url https://yourspacename.cloud.kompira.jp/apps/sonar/networks/<networkId>/snapshots/<snapshotId>/nodes --filename kc_snapshotlist --format xlsx
```

## Columns

### managed-nodes

| Column Name | Description |
| ----- | ----- |
| networkId                    | Network ID on Kompira cloud |
| managedNodeId                | Managed Node ID on Kompira cloud |
| displayName                  | Display Name |
| hostName                     | Hostname |
| ipAddress                    | IP Address |
| subnet                       | subnet |
| macaddr                      | Mac Address |
| vendor                       | Vendor Name (from Mac Address) |
| systemFamily                 | System family name |
| systemVersion                | Version number of system |
| systemSerial                 | Serial number of system |
| biosVendorName               | Vendor name of bios |
| biosVersionNumber            | Version number of bios |
| motherboardVendorName        | Vendor name of motherboard |
| motherboardModelNumber       | Model number of motherboard |
| motherboardVersionNumber     | Version number of motherboard |
| motherboardSerialNumber      | Serial number of motherboard |
| productModelNumber           | Model number of product |
| productModelName             | Model name of product |
| productSerialNumber          | Serial number of product |
| productVersionNumber         | Version number of product |
| productFirmwareVersionNumber | Firmware version number of product |
| productVendorName            | Vendor name of product |
| cpuNumberOfSockets           | Number of sockets of CPU |
| cpuNumberOfCores             | Number of cores of CPU |
| cpuNumberOfProcessors        | Number of processors of CPU |
| memoryTotalSize              | Total Size of memory |
| storageNumberOfDrives        | Number of storage drive |
| storageTotalSize             | Total Size of storage |
| packagesTotal                | Number of installed packages |
| windowsupdatesTotal          | Number of applied windows updates (windows only) |
| updatedAt                    | Last updated datetime |


### snapshot-node

| Column Name | Description |
| ----- | ----- |
| networkId                    | Network ID on Kompira cloud |
| snapshotId                   | Snapshot ID on Kompira cloud |
| nodeId                       | Node ID on Kompira cloud |
| aggregationType              | Aggregation Type |
| hostName                     | Hostname |
| ipAddress                    | IP Address |
| subnet                       | subnet |
| macaddr                      | Mac Address |
| vendor                       | Vendor Name (from Mac Address) |
| systemFamily                 | System family name |
| systemVersion                | Version number of system |
| systemSerial                 | Serial number of system |
| biosVendorName               | Vendor name of bios |
| biosVersionNumber            | Version number of bios |
| motherboardVendorName        | Vendor name of motherboard |
| motherboardModelNumber       | Model number of motherboard |
| motherboardVersionNumber     | Version number of motherboard |
| motherboardSerialNumber      | Serial number of motherboard |
| productModelNumber           | Model number of product |
| productModelName             | Model name of product |
| productSerialNumber          | Serial number of product |
| productVersionNumber         | Version number of product |
| productFirmwareVersionNumber | Firmware version number of product |
| productVendorName            | Vendor name of product |
| cpuNumberOfSockets           | Number of sockets of CPU |
| cpuNumberOfCores             | Number of cores of CPU |
| cpuNumberOfProcessors        | Number of processors of CPU |
| memoryTotalSize              | Total Size of memory |
| storageNumberOfDrives        | Number of storage |
| storageTotalSize             | Total Size of storage drive |
| packagesTotal                | Number of installed packages |
| windowsupdatesTotal          | Number of applied windows updates (windows only) |


## Options

* `--url URL`
    * node list url or snapshots url
    * example: `https://yourspacename.cloud.kompira.jp/apps/sonar/networks/<networkId>/managed-nodes`
    * example: `https://yourspacename.cloud.kompira.jp/apps/sonar/networks/<networkId>/snapshots/<snapshotId>/nodes`
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

