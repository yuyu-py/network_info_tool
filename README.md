# システムコマンドを活用したネットワーク情報取得ツール

## プロジェクト内容

現在接続中のWi-Fiネットワークの名前とパスワードを取得するネットワーク情報管理ツールです。Windows・macOS両対応のクロスプラットフォーム仕様で、各OSのシステムコマンドを活用してセキュアなネットワーク情報を自動取得します。Pythonのsubprocessモジュールとシステムコマンド実行技術を学習することを目的として実装しました。

## プロジェクト構成

```
network_info_tool/
├── wifi_manager.py          # メインプログラム
├── config.py               # 設定管理ファイル
├── requirements.txt        # 依存関係管理
├── README.md              # プロジェクト説明書
└── .gitignore             # Git除外ファイル設定
```

## 必要要件/開発環境

- **Python 3.7以上**
- **VSCode** (開発環境)
- **Git** (バージョン管理)
- **Windows 10以上** または **macOS 10.14以上**

### 使用ライブラリ

- **subprocess** システムコマンドの実行処理
- **platform** OS種別の自動判定
- **os** オペレーティングシステム操作

## 機能

- **OS自動判定** Windows・macOSの自動識別とコマンド選択
- **Wi-Fi名取得** 現在接続中のネットワーク名を自動取得
- **Wi-Fiパスワード取得** 接続中ネットワークのパスワードを安全に取得
- **クロスプラットフォーム対応** Windows・macOS両環境での動作保証
- **システムコマンド実行** netsh・networksetup・securityコマンドの活用
- **データ解析処理** コマンド出力の文字列解析と情報抽出
- **エラーハンドリング** コマンド実行失敗やタイムアウトへの対応
- **権限管理** 管理者権限が必要な処理の適切な案内

## 実行方法

### 1. リポジトリのクローン

```bash
git clone https://github.com/yourusername/network_info_tool.git
cd network_info_tool
```

### 2. 仮想環境の作成・アクティベート

**Windows**
```bash
python -m venv myenv
myenv\Scripts\activate
```

**macOS**
```bash
python3 -m venv myenv
source myenv/bin/activate
```

### 3. 依存関係のインストール

```bash
pip install -r requirements.txt
```

### 4. プログラムの実行

**Windows**
```bash
python wifi_manager.py
```

**macOS**
```bash
python3 wifi_manager.py
```

実行後、現在接続中のWi-Fi名とパスワードが表示されます。

### 注意事項

- パスワード取得には管理者権限が必要な場合があります
- macOSでは初回実行時にキーチェーンアクセスの許可が求められることがあります
- セキュリティソフトによってコマンド実行がブロックされる場合があります

## データ取得について

* **Windows環境** netshコマンドを使用してWLAN情報を取得
* **macOS環境** networksetupとsecurityコマンドを使用してネットワーク情報を取得
* **出力形式** コンソールに接続情報を表示

## 開発者

YuYu
