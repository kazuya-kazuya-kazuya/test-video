# test-video

MCPツールを組み合わせて動画生成・編集を行うためのプロジェクトです。

## ディレクトリ構成

```text
test-video/
  assets/              生成・取得した素材
    audio/
    fonts/
    images/
    video/
  config/              プロジェクト設定
  logs/                実行ログ
  mcp_servers/         自作・追加MCPサーバー
  outputs/             最終出力動画
  prompts/             動画生成・画像生成・ナレーション用プロンプト
  scripts/             補助スクリプト
  subtitles/           srt/vtt等の字幕
  tmp/                 一時ファイル
  mcp_tools.yaml       利用可能なMCPツール一覧
```

## 基本運用

1. `mcp_tools.yaml` で利用可能なMCPツールを確認する
2. 複数候補がある場合は、実行前に使用ツールを確認する
3. 複数ステップの動画制作では、実行前に計画を提示する
4. 生成物は `outputs/` に保存する
5. 素材や中間生成物は `assets/` または `tmp/` に保存する

## 環境依存ツール

以下のようなローカル環境依存ツールは、実行前に起動状態や認証状態を確認します。

- `voicevox-mcp`: VOICEVOXアプリの起動が必要
- `premiere-mcp`: Adobe Premiere Pro / Adobe CC環境が必要
- `capcut-mcp`: Business API契約またはGUI自動化環境が必要

## 新しいMCPツールの追加

新しいMCPを追加する場合は、`mcp_servers/{tool_name}/server.py` を作成し、`mcp_tools.yaml` にエントリを追記します。

テンプレートは [mcp_servers/_template/server.py](mcp_servers/_template/server.py) を参照してください。
