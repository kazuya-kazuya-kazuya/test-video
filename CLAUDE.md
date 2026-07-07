# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## プロジェクト概要

MCPツール（Model Context Protocol）を組み合わせて動画・画像・音声素材を生成するためのプロジェクト。コード自体は薄く、実体は「どのMCPツールをいつ使うか」を定義した設定（`mcp_tools.yaml`, `config/project.yaml`）と、素材/成果物のディレクトリ規約。加えて、求人広告用の画像・コピーを生成する実運用スクリプトが `scripts/` と各種素材ディレクトリに存在する。

## セットアップとコマンド

```
python -m pip install -r requirements.txt
```

- lintやテストスイートは設定されていない（pytestやlint設定ファイルはリポジトリ内に存在しない）。変更の確認は該当スクリプトを直接実行して行う。
  ```
  python scripts/generate_job_image.py
  python scripts/list_mcp_tools.py
  ```
- `scripts/generate_job_image.py` はPillowを使って `outputs/job_posting.png`（1080x1920）を生成する。フォントは `C:\Windows\Fonts` から直接読み込む（例: `NotoSansJP-VF.ttf`, `BIZ-UDGothicB.ttc`）ため、これらのフォントがインストールされたWindows環境でのみ実行可能。
- `scripts/list_mcp_tools.py` は `mcp_tools.yaml` を正規表現ベースの簡易パーサーで読み取り（完全なYAMLパーサーではない）、各ツールについて `name\tcategory\tdescription` を出力する。新しいエントリを `mcp_tools.yaml` に追加する際は、既存と同じフラットな `name:`/`category:`/`description:` 形式を維持すること。それ以外の形式だとこのスクリプトはフィールドを無視する。

## アーキテクチャ

### MCPツールレジストリ（`mcp_tools.yaml`, `mcp_servers/`）

`mcp_tools.yaml` は利用可能なMCPツールの一覧を管理する唯一の情報源で、カテゴリ（`video`, `image`, `audio`, `text`, `distribution`）ごとに `requires`（必要な認証・実行環境）と `input_formats`/`output_formats` を持つ。`config/project.yaml` の `tool_selection.defaults` では、タスク種別ごとのデフォルトツールを定義している（例: `japanese_tts: voicevox-mcp`, `professional_editing: premiere-mcp`）。

新しいMCPツールを追加する手順:
1. `mcp_servers/_template/server.py`（`mcp.server.Server` を使い `@app.tool()` で非同期関数を定義し、stdio経由で実行する最小構成）をもとに `mcp_servers/{tool_name}/server.py` を作成する。
2. 新しい依存関係があれば `requirements.txt` に追加する。
3. `mcp_tools.yaml` にツール情報を登録する。

`mcp_servers/ffmpeg/server.py` はテンプレート以外で唯一実装されているサーバーで、実際のサーバーが `subprocess.run` で `ffmpeg`/`ffprobe` を呼び出し、結果を文字列で返す実装の参考になる。

### 複数ステップ・複数ツールを扱う際の運用ルール

以下は `README.md` に由来するルールで、MCPツールの選定や成果物生成を伴うタスク全般に適用する:
- ツール選定前に `mcp_tools.yaml` を確認する。
- 複数のツールが候補になり得る場合は、実行前にユーザーに確認する（ただし `config/project.yaml` の `tool_selection.skip_confirmation_when_user_specifies_tool` により、ユーザーが特定のツールを指定済みの場合は確認不要）。
- 複数ステップの動画制作では、実行前に計画を提示する。
- 最終成果物は `outputs/` に、素材や中間生成物は `assets/` または `tmp/` に保存する。
- 一部のMCPツールはローカル環境依存であり、使用前に起動状態・認証状態を確認する必要がある: `voicevox-mcp`（VOICEVOXアプリの起動が必要、デフォルト `http://127.0.0.1:50021`）、`premiere-mcp`（Adobe Premiere Pro/CC環境が必要）、`capcut-mcp`（CapCut Business APIまたはGUI自動化環境が必要）。
- `config/project.yaml` には出力のデフォルト仕様（mp4/h264、1920x1080、30fps、48kHz/ステレオ音声）と、生成後の品質チェック項目（`quality_checks`: 長さ・解像度・フレームレートの検証、音声がある場合は音声同期の検証、出力パスの報告）も定義されている。動画を生成・検証する際はこれらの期待値に従う。

### 求人広告コンテンツ生成（求人コピー・バナー）

MCP動画パイプラインとは別に、このリポジトリは日本語の求人バナーとリライト済み求人コピーの制作にも使われている:
- `scripts/generate_job_image.py` はPillowでバナー画像を生成する際の基本パターン。固定サイズのページ、名前付きカラー定数の小さなパレット、ヘルパー関数（`rect`, `text_center`, `wrap_text`, `draw_wrapped`, `section_header`, `bullet_item`）を使い、ヘッダー→バッジ→リード文→本文セクション→概要テーブル→フッターCTAの順に上から積み上げる構成になっている。新しいバナーを作る際は、新しいレイアウト手法を持ち込むのではなく、この構成に従うこと。
- リライト済みの求人コピーは `求人文章_リライト10件/`（クライアントごとのサブフォルダあり）配下にプレーンテキストとして、生成済みバナー画像は `内部管理ファイル/`（クライアント・商材ごとのサブフォルダあり）配下に存在する。これらはコードではなくコンテンツ・素材ディレクトリであり、リファクタリング対象ではなく、読み書きするデータとして扱う。
