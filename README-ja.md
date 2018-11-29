# kc-export-nodes
Kompira cloudのノード情報をcsv/xlsx形式で出力するコマンドを提供します。

## 要件
- Python 3.6.5


## インストール

### Python のインストール

お使いの環境に沿って、以下のページを参考に Python 3.6 をインストールしてください。

- [Ubuntu](https://www.python.jp/install/ubuntu/index.html)
- [CentOS](https://www.python.jp/install/centos/index.html)
- [Windows](https://www.python.jp/install/windows/install_py3.html)

### Python モジュールのインストール
```
pip install openpyxl requests PyYAML jmespath
```

### config.yml の作成

`config.yml.sample` を参考に、 `config.yml` を作成してください。

`your_kompira_cloud_api_token` の部分には、お使いのKompira cloudの「全体設定 > APIトークン」で発行したトークン文字列を記載してください。


```
kompira_cloud:
  token: your_kompira_cloud_api_token
```

## 使用方法

Kompira cloudのノード一覧URL、もしくはスナップショットURLを指定することで、ローカルファイルとしてデータを出力します。

```
# ノード一覧をxlsx形式で出力
kc_exporter.py --url https://yourspacename.cloud.kompira.jp/apps/sonar/networks/<networkId>/managed-nodes --filename kc_nodelist --format xlsx

# ノード一覧をcsv形式で出力
kc_exporter.py --url https://yourspacename.cloud.kompira.jp/apps/sonar/networks/<networkId>/managed-nodes --filename kc_nodelist --format csv

# 複数の値を持つカラムは最初のデータのみ書くようにする
kc_exporter.py --url https://yourspacename.cloud.kompira.jp/apps/sonar/networks/<networkId>/managed-nodes --filename kc_nodelist --format xlsx --zeroth

# スナップショットノード一覧をxlsx形式で出力
kc_exporter.py --url https://yourspacename.cloud.kompira.jp/apps/sonar/networks/<networkId>/snapshots/<snapshotId>/nodes --filename kc_snapshotlist --format xlsx
```

## カラム

### ノード一覧

| カラム名 | 説明 |
| ----- | ----- |
| networkId                    | Kompira cloud上のネットワークID |
| managedNodeId                | Kompira cloud上のノードID |
| displayName                  | ノード名 |
| hostName                     | ホスト名 |
| ipAddress                    | IPアドレス |
| subnet                       | サブネット |
| macaddr                      | MACアドレス |
| vendor                       | ベンダー名 |
| systemFamily                 | 機種・OS |
| systemVersion                | システムバージョン |
| systemSerial                 | システムシリアル |
| biosVendorName               | BIOS ベンダ名 |
| biosVersionNumber            | BIOS バージョン |
| motherboardVendorName        | マザーボードベンダ名 |
| motherboardModelNumber       | マザーボードモデル番号 |
| motherboardVersionNumber     | マザーボードバージョン |
| motherboardSerialNumber      | マザーボードシリアル番号 |
| productModelNumber           | 製品モデル番号 |
| productModelName             | 製品モデル名 |
| productSerialNumber          | 製品シリアル番号 |
| productVersionNumber         | 製品バージョン |
| productFirmwareVersionNumber | 製品ファームウェアバージョン |
| productVendorName            | 製品ベンダ名 |
| cpuNumberOfSockets           | CPU ソケット数 |
| cpuNumberOfCores             | CPU コア数 |
| cpuNumberOfProcessors        | CPU プロセッサ数 |
| memoryTotalSize              | メモリ総容量 |
| storageNumberOfDrives        | ストレージドライブ数 |
| storageTotalSize             | ストレージ総容量 |
| packagesTotal                | パッケージ数 |
| windowsupdatesTotal          | Windows アップデート数 |
| updatedAt                    | 最後に更新された日時 |


### スナップショットノード一覧

| カラム名 | 説明 |
| ----- | ----- |
| networkId                    | Kompira cloud上のネットワークID |
| snapshotId                   | Kompira cloud上のスナップショットID |
| nodeId                       | Kompira cloud上のノードID |
| aggregationType              | 集約タイプ |
| hostName                     | ホスト名 |
| ipAddress                    | IPアドレス |
| subnet                       | サブネット |
| macaddr                      | MACアドレス |
| vendor                       | ベンダー名 |
| systemFamily                 | 機種・OS |
| systemVersion                | システムバージョン |
| systemSerial                 | システムシリアル |
| biosVendorName               | BIOS ベンダ名 |
| biosVersionNumber            | BIOS バージョン |
| motherboardVendorName        | マザーボードベンダ名 |
| motherboardModelNumber       | マザーボードモデル番号 |
| motherboardVersionNumber     | マザーボードバージョン |
| motherboardSerialNumber      | マザーボードシリアル番号 |
| productModelNumber           | 製品モデル番号 |
| productModelName             | 製品モデル名 |
| productSerialNumber          | 製品シリアル番号 |
| productVersionNumber         | 製品バージョン |
| productFirmwareVersionNumber | 製品ファームウェアバージョン |
| productVendorName            | 製品ベンダ名 |
| cpuNumberOfSockets           | CPU ソケット数 |
| cpuNumberOfCores             | CPU コア数 |
| cpuNumberOfProcessors        | CPU プロセッサ数 |
| memoryTotalSize              | メモリ総容量 |
| storageNumberOfDrives        | ストレージドライブ数 |
| storageTotalSize             | ストレージ総容量 |
| packagesTotal                | パッケージ数 |
| windowsupdatesTotal          | Windows アップデート数 |

## Options

* `--url URL`
    * 情報取得元のノード一覧URL または スナップショットURLを指定
    * example: `https://yourspacename.cloud.kompira.jp/apps/sonar/networks/<networkId>/managed-nodes`
    * example: `https://yourspacename.cloud.kompira.jp/apps/sonar/networks/<networkId>/snapshots/<snapshotId>/nodes`
* `--config_path FILEPATH`
    * config.yml ファイルパス
    * default:`config.yml`
* `--filename FILEPATH`
    * 出力先ファイルパス
* `--format OUTPUT_FORMAT`
    * `csv` or `xlsx`
    * default: `csv`
* `--zeroth`
    * 複数個データが存在するフィールドの場合、先頭のデータの値のみを出力する
    * 指定しない場合、複数個データが存在するフィールドはjson形式ですべてのデータを出力する

