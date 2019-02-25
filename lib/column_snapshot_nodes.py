columns = {
    'networkId': {
        'path': 'networkId'
    },
    'snapshotId': {
        'path': 'snapshotId'
    },
    'nodeId': {
        'path': 'nodeId'
    },
    'aggregationType': {
        'path': 'aggregationType',
    },
    'hostName': {
        'path': 'addresses[].hostnames[].hostname',
        'path_zeroth': 'addresses[0].hostnames[0].hostname'
    },
    'ipAddress': {
        'path': 'addresses[].addr',
        'path_zeroth': 'addresses[0].addr'
    },
    'subnet': {
        'path': 'addresses[].subnet',
        'path_zeroth': 'addresses[0].subnet'
    },
    'macaddr': {
        'path': 'addresses[].macaddr',
        'path_zeroth': 'addresses[0].macaddr'
    },
    'vendor': {
        'path': 'addresses[].extraFields.macaddr.organizationName',
        'path_zeroth': 'addresses[0].extraFields.macaddr.organizationName'
    },
    'systemFamily': {
        'path': 'system.family'
    },
    'systemVersion': {
        'path': 'system.version'
    },
    'systemSerial': {
        'path': 'system.serial'
    },
    'biosVendorName': {
        'path': 'extraFields.bios.vendorName'
    },
    'biosVersionNumber': {
        'path': 'extraFields.bios.versionNumber'
    },
    'motherboardVendorName': {
        'path': 'extraFields.motherboard.vendorName'
    },
    'motherboardModelNumber': {
        'path': 'extraFields.motherboard.modelNumber'
    },
    'motherboardVersionNumber': {
        'path': 'extraFields.motherboard.versionNumber'
    },
    'motherboardSerialNumber': {
        'path': 'extraFields.motherboard.serialNumber'
    },
    'productModelNumber': {
        'path': 'extraFields.product.modelNumber'
    },
    'productModelName': {
        'path': 'extraFields.product.modelName'
    },
    'productSerialNumber': {
        'path': 'extraFields.product.serialNumber'
    },
    'productVersionNumber': {
        'path': 'extraFields.product.versionNumber'
    },
    'productFirmwareVersionNumber': {
        'path': 'extraFields.product.firmwareVersionNumber'
    },
    'productVendorName': {
        'path': 'extraFields.product.vendorName'
    },
    'cpuNumberOfSockets': {
        'path': 'extraFields.cpu.numberOfSockets'
    },
    'cpuNumberOfCores': {
        'path': 'extraFields.cpu.numberOfCores'
    },
    'cpuNumberOfProcessors': {
        'path': 'extraFields.cpu.numberOfProcessors'
    },
    'memoryTotalSize': {
        'path': 'extraFields.memory.totalSize'
    },
    'storageNumberOfDrives': {
        'path': 'extraFields.storage.numberOfDrives'
    },
    'storageTotalSize': {
        'path': 'extraFields.storage.totalSize'
    },
    'packagesTotal': {
        'path': 'numberOfPackages'
    },
    'windowsupdatesTotal': {
        'path': 'numberOfWindowsUpdates'
    }
}
