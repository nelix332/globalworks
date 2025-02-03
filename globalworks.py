import ctypes
import winreg

class GlobalWorks:
    def __init__(self):
        self.registry_path = r"SOFTWARE\Policies\Microsoft\Windows\Personalization"
        self.settings = {
            "NoLockScreen": 1,
            "NoLockScreenCamera": 1,
            "NoLockScreenSlideshow": 1,
            "ScreenSaverIsSecure": 1
        }

    def create_registry_key(self):
        try:
            with winreg.CreateKey(winreg.HKEY_LOCAL_MACHINE, self.registry_path) as key:
                print(f"Registry key created at {self.registry_path}")
                return key
        except WindowsError as e:
            print(f"Failed to create registry key: {e}")
            return None

    def configure_lock_screen(self):
        key = self.create_registry_key()
        if key:
            for setting, value in self.settings.items():
                try:
                    winreg.SetValueEx(key, setting, 0, winreg.REG_DWORD, value)
                    print(f"Set {setting} to {value}")
                except WindowsError as e:
                    print(f"Failed to set {setting}: {e}")

    def apply_changes(self):
        try:
            # SendMessage to refresh the lock screen settings
            ctypes.windll.user32.SendMessageTimeoutW(0xFFFF, 0x001A, 0, 0, 0x0002, 5000)
            print("Lock screen settings updated successfully.")
        except Exception as e:
            print(f"Failed to apply changes: {e}")

if __name__ == "__main__":
    gw = GlobalWorks()
    gw.configure_lock_screen()
    gw.apply_changes()