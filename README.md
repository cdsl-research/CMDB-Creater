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

 ### 使い方

 **準備**

 まずはCMDBに入れるようのDBを作成します．なおMySQLをK3s上に配置します．

cdで対象のディレクトリに移動
```
$ cd CMDB-Creater/cmdb
```

NameSpaceの作成
```
$ kubectl create ns cmdb
```


PVCの配置
```
$ kubectl apply -f mysql-pvc.yaml -n cmdb
```

deploymentとserviceの配置
```
$ kubectl apply -f mysql.yaml -n cmdb
```

podとserviceが立っているかどうかを確認します．
```
$ kubectl get pods -n cmdb
NAME                            READY   STATUS    RESTARTS   AGE
mysql-server-75c9cc7bd5-vhqrh   1/1     Running   0          10h
$ kubectl get svc -n cmdb
NAME           TYPE       CLUSTER-IP     EXTERNAL-IP   PORT(S)          AGE
mysql-server   NodePort   10.43.253.57   <none>        3306:32000/TCP   10h
```


**CMDB-Createrの使い方**

対象のディレクトリに移動
```
cd CMDB-Creater/cmdb-creater
```

実行
```
$ python3 cmdb-create.py 
```

こんな感じの表示が出ればOKです．

<img width="634" alt="スクリーンショット 2024-12-19 14 43 42" src="https://github.com/user-attachments/assets/73ce6d3c-3680-444d-8cd3-6c148520a170" />


MySQLにデータが入っているかも確認しましょう．
```
$ mysql -uroot -h monitoring-master-ml -p -P 32000
```

データベースの確認
```
mysql> show databases;
```

<img width="183" alt="スクリーンショット 2024-12-18 12 32 38" src="https://github.com/user-attachments/assets/517ceb73-944e-4751-977c-edc97053aaf3" />


cmdbを選択
```
mysql> use cmdb;
```

cmdbの中にあるnetwork_statusを確認
```
mysql> SELECT * FROM network_status;
```


<img width="601" alt="スクリーンショット 2024-12-18 12 34 00" src="https://github.com/user-attachments/assets/e8c95491-9abc-4613-8184-e6e8216f72ed" />








 

