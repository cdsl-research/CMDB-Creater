import xmlrpc.client
import mysql.connector

# サーバーのURLリスト
server_urls = [
    "http://bokoboko:8000/",
    "http://bokoboko-w2:8000/",
    "http://bokoboko-w3:8000/",
    "http://outside-nfs7:8000/"
]

# MySQL接続設定
mysql_config = {
    "host": "monitoring-master-ml",  # Kubernetes service name for the MySQL server
    "user": "devuser",  # 'root' -> 'devuser' as per the ConfigMap
    "password": "devuser",  # 'password' -> 'devuser' as per the ConfigMap
    "port": "32000",  # NodePort 32000
    "database": "cmdb"
}

# 各サーバーの結果を保存するリスト
all_results = []

def insert_to_mysql(data):
    """ MySQLにデータを挿入する関数 """
    try:
        # MySQL接続
        conn = mysql.connector.connect(**mysql_config)
        cursor = conn.cursor()

        # SQL文の準備
        insert_query = """
        INSERT INTO network_status (hypervisor_name, hypervisor_ip, ip_address, connected_ip_and_port)
        VALUES (%s, %s, %s, %s)
        """
        cursor.executemany(insert_query, data)
        conn.commit()

        cursor.close()
        conn.close()
    except mysql.connector.Error as e:
        print(f"Error inserting into MySQL: {e}")

def get_network_status_from_servers():
    """ サーバーからネットワークステータスを取得してMySQLに挿入 """
    results = []
    
    for server_url in server_urls:
        print(f"Trying server: {server_url}")
        try:
            # サーバーへの接続
            proxy = xmlrpc.client.ServerProxy(server_url)
            # get_network_status関数の呼び出し
            network_status = proxy.get_network_status()
            print(f"Peer Address:Port (Filtered) from {server_url}:")
            print(network_status)
            
            # 結果をリストに追加（分割して処理）
            for line in network_status.splitlines():
                if line.strip():  # 空行をスキップ
                    # データの構造（hypervisor_name, hypervisor_ip, ip_address, connected_ip_and_port）に変換
                    parts = line.strip().split(",")
                    print(parts)  # ここでpartsがどのように分割されているか確認

                    # parts の要素数が3つでない場合はスキップ
                    if len(parts) == 3:
                        # Lotusはハードコーディングされており、他のフィールドは分割された parts から取得
                        hv_ip = parts[0].strip('()')  # 不要な括弧を削除
                        client_ip = parts[1].strip('()')  # 不要な括弧を削除
                        port_info = parts[2].strip('()')  # 不要な括弧を削除
                        results.append(('Lotus', hv_ip, client_ip, port_info))
                    else:
                        print(f"Skipping invalid data: {line}")
            
        except Exception as e:
            print(f"Error calling get_network_status on {server_url}: {e}")

    # MySQLにデータを挿入
    if results:
        insert_to_mysql(results)

    return "\n".join(f"({line})" for line in results)

# 実行
if __name__ == "__main__":
    # ネットワークステータスを取得し、MySQLに挿入
    get_network_status_from_servers()

