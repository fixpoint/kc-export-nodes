# kc-export-nodes
Export Nodes data on Kompira cloud

[Japanese README](README-ja.md)

## Requirements
- Python 3.6.5


## Install

### Install python modules
```
pip install -r requirements.txt
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

# Output node list & package list to xlsx file
kc_exporter.py --url https://yourspacename.cloud.kompira.jp/apps/sonar/networks/<networkId>/managed-nodes --filename kc_nodelist --package_filename kc_packagelist --format xlsx

# node list(0 array data only)
kc_exporter.py --url https://yourspacename.cloud.kompira.jp/apps/sonar/networks/<networkId>/managed-nodes --filename kc_nodelist --format xlsx --zeroth

# Output snapshot-node list to xlsx file
kc_exporter.py --url https://yourspacename.cloud.kompira.jp/apps/sonar/networks/<networkId>/snapshots/<snapshotId>/nodes --filename kc_snapshotlist --format xlsx

# Output snapshot-node list and package list to csv file
kc_exporter.py --url https://yourspacename.cloud.kompira.jp/apps/sonar/networks/<networkId>/snapshots/<snapshotId>/nodes --filename kc_snapshotlist --package_filename kc_packagelist --format csv
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
| vendor                       | Vendor Name (from macaddr) |
| internalIpAddress            | IP Address, internal information of node |
| internalSubnet               | subnet, internal information of node |
| internalMacaddr              | Mac Address, internal information of node |
| internalIfname               | Interface Name, internal information of node |
| internalVendor               | Vendor Name (from internalMacaddr) |
| systemFamily                 | System family name |
| systemVersion                | Version number of system |
| systemSerial                 | Serial number of system |
| kernelName                   | Kernel Name (Linux only) |
| kernelVersion                | Kernel Version (Linux only) |
| kernelRelease                | Kernel Release (Linux only) |
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
| storageNumberOfDrives        | Number of storage drives |
| storageTotalSize             | Total Size of storage |
| packagesTotal                | Number of installed packages |
| windowsupdatesTotal          | Number of applied windows updates (Windows only) |
| updatedAt                    | Last updated datetime |


### snapshot-nodes

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
| vendor                       | Vendor Name (from macaddr) |
| internalIpAddress            | IP Address, internal information of node |
| internalSubnet               | subnet, internal information of node |
| internalMacaddr              | Mac Address, internal information of node |
| internalIfname               | Interface Name, internal information of node |
| internalVendor               | Vendor Name (from internalMacaddr) |
| systemFamily                 | System family name |
| systemVersion                | Version number of system |
| systemSerial                 | Serial number of system |
| kernelName                   | Kernel Name (Linux only) |
| kernelVersion                | Kernel Version (Linux only) |
| kernelRelease                | Kernel Release (Linux only) |
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
| storageNumberOfDrives        | Number of storage drives |
| storageTotalSize             | Total Size of storage |
| packagesTotal                | Number of installed packages |
| windowsupdatesTotal          | Number of applied windows updates (Windows only) |


### packages

| Column Name | Description |
| ----- | ----- |
| managedNodeId                | Managed Node ID (Only when output managed-nodes) |
| nodeId                       | Node ID (Only when output snapshot-nodes) |
| hostName                     | Hostname |
| name                         | Package name |
| version                      | Version |
| architecture                 | Architecture (Linux Only) |



## Options

- `--url URL`
    - node list url or snapshots url
    - example: `https://yourspacename.cloud.kompira.jp/apps/sonar/networks/<networkId>/managed-nodes`
    - example: `https://yourspacename.cloud.kompira.jp/apps/sonar/networks/<networkId>/snapshots/<snapshotId>/nodes`
- `--config_path FILEPATH`
    - config.yml path
    - default:`config.yml`
- `--filename FILEPATH`
    - node list output file path
- `--package_filename FILEPATH`
    - package list output file path
- `--format OUTPUT_FORMAT`
    - `csv` or `xlsx`
    - default: `csv`
- `--zeroth`
    - output only 0 array data.

