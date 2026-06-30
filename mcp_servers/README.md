# MCP Servers

このディレクトリには、プロジェクト固有のMCPサーバーを配置します。

新規追加時の基本手順:

1. `mcp_servers/{tool_name}/server.py` を作成
2. 必要な依存を `requirements.txt` に追加
3. `mcp_tools.yaml` にツール情報を追記
4. サーバーを起動してツール一覧を検証

テンプレート:

- [mcp_servers/_template/server.py](_template/server.py)
