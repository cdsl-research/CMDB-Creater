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


- ```mysql-pvc.yaml```
MySQLのPVCをK3s上に立てるためのYAMLファイル 
