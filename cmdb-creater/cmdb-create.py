from target_get import get_network_status_from_servers

def main():
    # get_network_status_from_servers関数を呼び出して結果を取得
    combined_results = get_network_status_from_servers()

    # 返された結果を表示
    print("\nFinal combined results:")
    print(combined_results)

if __name__ == "__main__":
    main()

