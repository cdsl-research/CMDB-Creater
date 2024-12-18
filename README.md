# CMDB-Creater

構成管理データベースを作るためのソフトウェアです．
以下のCMDB-exporterが保持しているssコマンドとESXiホストの情報から作成します．


https://github.com/cdsl-research/CMDB-exporter2

### 環境
- Ubuntu 24.04.1 LTS
- K3s
- MySQL
- Python 3.10.12
  - ライブラリ
    - xmlrpc.client
    - mysql.connector
   

### 構成要素
```
.
├── cmdb
│   ├── mysql-pvc.yaml
│   └── mysql.yaml
├── cmdb-creater
│   ├── cmdb-create.py
│   ├── __pycache__
│   │   └── target_get.cpython-312.pyc
│   └── target_get.py
└── README.md
```


cmdb
- ```mysql-pvc.yaml```：MySQLのPVCをK3s上に立てるためのYAMLファイル
- ```mysql.yaml```：MySQLのserveceやdeployment，を立てるためのYAMLファイル

cmdb-creater
- ```target_get.py```
  - insert_to_mysql()：CMDBを構成するMySQLに対してCMDB-exporterが取得してきたデータを格納
  - get_network_status_from_servers()：CMDB-exporterに対してデータを要求し，データを入れるように整形
- ```cmdb-create.py```
  - main()：target.pyの内容を実行する関数
 


 

