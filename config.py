"""
ネットワーク情報取得ツール用の設定ファイル
各OS用のシステムコマンドとメッセージを管理
"""

# Windows用コマンド設定
WINDOWS_COMMANDS = {
    "wifi_interfaces": ["netsh", "wlan", "show", "interfaces"],
    "wifi_profile": ["netsh", "wlan", "show", "profile"],  # プロファイル名は動的に追加
}

# macOS用コマンド設定
MACOS_COMMANDS = {
    "wifi_network": ["networksetup", "-getairportnetwork", "en0"],
    "wifi_password": ["security", "find-generic-password", "-wa"],  # Wi-Fi名は動的に追加
}

# メッセージ設定
MESSAGES = {
    "success": "ネットワーク情報の取得が完了しました",
    "no_wifi": "Wi-Fi接続が見つかりません",
    "no_password": "パスワードを取得できませんでした",
    "permission_error": "管理者権限が必要です",
}