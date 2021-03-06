node_columns = {
    'networkId': {
        'path': 'networkId'
    },
    'managedNodeId': {
        'path': 'managedNodeId'
    },
    'displayName': {
        'path': 'displayName'
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
    'internalIpAddress': {
        'path': 'sort_by(interfaces[], &macaddr)[].addr',
        # 存在する値の先頭を取得する
        'path_zeroth': 'sort_by(interfaces[], &macaddr)[].addr | [0]'
    },
    'internalSubnet': {
        'path': 'sort_by(interfaces[], &macaddr)[].netmask',
        # 存在する値の先頭を取得する
        'path_zeroth': 'sort_by(interfaces[], &macaddr)[].netmask | [0]'
    },
    'internalMacaddr': {
        'path': 'sort_by(interfaces[], &macaddr)[].macaddr',
        # 存在する値の先頭を取得する
        'path_zeroth': 'sort_by(interfaces[], &macaddr)[].macaddr | [0]'
    },
    'internalIfname': {
        'path': 'sort_by(interfaces[], &macaddr)[].ifname',
        # 存在する値の先頭を取得する
        'path_zeroth': 'sort_by(interfaces[], &macaddr)[].ifname | [0]'
    },
    'internalVendor': {
        'path': 'extraFields.networking.macaddrs.*.organizationName',
        # 存在する値の先頭を取得する
        'path_zeroth': 'extraFields.networking.macaddrs.*.organizationName | [0]'
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
    'kernelName': {
        'path': 'extraFields.kernel.name'
    },
    'kernelVersion': {
        'path': 'extraFields.kernel.version'
    },
    'kernelRelease': {
        'path': 'extraFields.kernel.release'
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
    },
    'updatedAt': {
        'path': 'updatedAt'
    }
}

package_columns = {
    'managedNodeId': {
        'node_key': 'managedNodeId',
    },
    'hostName': {
        'node_key': 'hostName'
    },
    'name': {
        'path': 'name'
    },
    'version': {
        'path': 'version'
    },
    'architecture': {
        'path': 'arch'
    }
}
