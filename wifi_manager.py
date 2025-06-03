import subprocess  # システムコマンド実行用
import os  # OS情報取得用
import platform  # プラットフォーム判定用


class NetworkInfoManager:
    """ネットワーク情報を取得するクラス"""
    
    def __init__(self):
        """初期設定"""
        # 動いているOSを判定
        self.operating_system = platform.system()
        print(f"検出されたOS: {self.operating_system}")

    def check_platform(self):
        """OSを確認して使用するコマンドを決める"""
        if self.operating_system == "Windows":
            # print("Windows環境を検出しました。netshコマンドを使用します。")
            return "windows"
        elif self.operating_system == "Darwin":  # macOSはDarwinになる
            # print("macOS環境を検出しました。networksetupコマンドを使用します。")
            return "macos"
        else:
            print(f"サポートされていないOS: {self.operating_system}")
            return "unsupported"

    def execute_command(self, command_list):
        """コマンドを実行（エラーハンドリング強化版）
        
        Args:
            command_list: 実行するコマンドのリスト
            
        Returns:
            str: コマンドの結果、失敗時はNone
        """
        try:
            # コマンド実行
            result = subprocess.check_output(
                command_list,
                stderr=subprocess.STDOUT,  # エラーも標準出力に含める
                timeout=15  # パスワード取得は時間がかかることがあるので15秒
            )
            # バイト列を文字列に変換
            return result.decode('utf-8', errors='ignore')
        except subprocess.CalledProcessError as e:
            # 管理者権限エラーの場合
            if "access" in str(e).lower() or "permission" in str(e).lower():
                print("注意: 管理者権限が必要な場合があります")
            else:
                print(f"コマンド実行エラー: {e}")
            return None
        except subprocess.TimeoutExpired:
            print("コマンドがタイムアウトしました")
            return None
        except Exception as e:
            print(f"予期しないエラー: {e}")
            return None

    def get_current_wifi_name(self):
        """接続中のWi-Fi名を取得
        
        Returns:
            str: Wi-Fi名、取得失敗時はNone
        """
        platform_type = self.check_platform()
        
        if platform_type == "windows":
            # Windows: netshコマンドでインターフェース情報取得
            command = ["netsh", "wlan", "show", "interfaces"]
            output = self.execute_command(command)
            
            if output:
                return self._parse_windows_wifi_name(output)
                
        elif platform_type == "macos":
            # macOS: networksetupコマンドで現在のネットワーク取得
            command = ["networksetup", "-getairportnetwork", "en0"]
            output = self.execute_command(command)
            
            if output:
                return self._parse_macos_wifi_name(output)
        
        return None

    def _parse_windows_wifi_name(self, command_output):
        """Windowsのnetshコマンド結果からWi-Fi名を取得
        
        Args:
            command_output: netshコマンドの結果
            
        Returns:
            str: Wi-Fi名、見つからない場合はNone
        """
        # 行ごとに分割
        lines = command_output.split('\n')
        
        for line in lines:
            # 空白を除去
            cleaned_line = line.strip()
            
            # SSIDが含まれる行を探す
            if "ssid" in cleaned_line.lower() and ":" in cleaned_line:
                # コロンで分割してSSID名を取得
                parts = cleaned_line.split(":", 1)  # 最初のコロンで分割
                if len(parts) >= 2:
                    wifi_name = parts[1].strip()  # 前後の空白除去
                    if wifi_name and wifi_name != "":
                        return wifi_name
        
        return None

    def _parse_macos_wifi_name(self, command_output):
        """macOSのnetworksetupコマンド結果からWi-Fi名を取得
        
        Args:
            command_output: networksetupコマンドの結果
            
        Returns:
            str: Wi-Fi名、見つからない場合はNone
        """
        # 改行で分割
        lines = command_output.split('\n')
        
        for line in lines:
            cleaned_line = line.strip()
            
            # "Current Wi-Fi Network:"の行を探す
            if "current wi-fi network:" in cleaned_line.lower():
                # コロンで分割してWi-Fi名を取得
                parts = cleaned_line.split(":", 1)
                if len(parts) >= 2:
                    wifi_name = parts[1].strip()
                    return wifi_name
        
        return None

    def get_wifi_password(self, wifi_name):
        """Wi-Fiのパスワードを取得
        
        Args:
            wifi_name: パスワードを取得したいWi-Fi名
            
        Returns:
            str: Wi-Fiパスワード、取得失敗時はNone
        """
        if not wifi_name:
            return None
            
        platform_type = self.check_platform()
        
        if platform_type == "windows":
            # Windows: netshコマンドでプロファイル詳細を取得
            command = ["netsh", "wlan", "show", "profile", wifi_name, "key=clear"]
            output = self.execute_command(command)
            
            if output:
                return self._parse_windows_wifi_password(output)
                
        elif platform_type == "macos":
            # macOS: securityコマンドでキーチェーンからパスワード取得
            command = ["security", "find-generic-password", "-wa", wifi_name]
            output = self.execute_command(command)
            
            if output:
                return self._parse_macos_wifi_password(output)
        
        return None

    def _parse_windows_wifi_password(self, command_output):
        """Windowsのnetshコマンド結果からパスワードを抽出
        
        Args:
            command_output: netsh show profileコマンドの結果
            
        Returns:
            str: Wi-Fiパスワード、見つからない場合は"パスワードなし"
        """
        # 行ごとに分割
        lines = command_output.split('\n')
        
        for line in lines:
            # 前後の空白除去
            cleaned_line = line.strip()
            
            # "Key Content"の行を探す（パスワード情報）
            if "key content" in cleaned_line.lower() and ":" in cleaned_line:
                # コロンで分割してパスワード部分を取得
                parts = cleaned_line.split(":", 1)  # 最初のコロンで分割
                if len(parts) >= 2:
                    password = parts[1].strip()  # 空白除去
                    if password and password != "":
                        return password
        
        # パスワードが見つからない
        return "パスワードなし"

    def _parse_macos_wifi_password(self, command_output):
        """macOSのsecurityコマンド結果からパスワードを抽出
        
        Args:
            command_output: security find-generic-passwordコマンドの結果
            
        Returns:
            str: Wi-Fiパスワード、見つからない場合は"パスワードなし"
        """
        # 改行で分割
        lines = command_output.split('\n')
        
        for line in lines:
            cleaned_line = line.strip()
            
            # securityコマンドの直接出力（パスワードのみ）
            if cleaned_line and not cleaned_line.startswith("security:"):
                return cleaned_line
        
        return "パスワードなし"

    def display_network_info(self):
        """ネットワーク情報を表示（パスワード含む）"""
        print("=" * 50)
        print("ネットワーク詳細情報取得ツール")
        print("=" * 50)
        
        # 接続中のWi-Fi名を取得
        current_wifi = self.get_current_wifi_name()
        
        if current_wifi:
            print(f"接続中のWi-Fi名: {current_wifi}")
            
            # Wi-Fiパスワードを取得
            wifi_password = self.get_wifi_password(current_wifi)
            
            if wifi_password and wifi_password != "パスワードなし":
                print(f"Wi-Fiパスワード: {wifi_password}")
            else:
                print("Wi-Fiパスワード: 取得できませんでした")
                
        else:
            print("Wi-Fi接続が見つかりません")
        
        print("=" * 50)


def main():
    """メイン処理（パスワード取得機能含む）"""
    try:
        # ネットワーク管理クラスを作成
        network_manager = NetworkInfoManager()
        
        # OS情報表示をコメントアウト
        # print(f"検出されたOS: {network_manager.operating_system}")
        
        # ネットワーク詳細情報を表示（Wi-Fi名とパスワード）
        network_manager.display_network_info()
        
    except KeyboardInterrupt:
        print("\nプログラムが中断されました")
    except Exception as e:
        print(f"プログラム実行エラー: {e}")


# 直接実行時のみmain関数を呼び出し
if __name__ == "__main__":
    main()