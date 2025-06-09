import os
import sys
import shutil
import winreg
import ctypes
import subprocess

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def install_wmatrix():
    # Create installation directory
    install_dir = os.path.join(os.environ['LOCALAPPDATA'], 'WMatrix')
    os.makedirs(install_dir, exist_ok=True)
    
    # Copy files
    script_dir = os.path.dirname(os.path.abspath(__file__))
    shutil.copy2(os.path.join(script_dir, 'Program.py'), install_dir)
    shutil.copy2(os.path.join(script_dir, 'wmatrix.bat'), install_dir)
    
    # Add to PATH
    path_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, 
                             r'Environment', 
                             0, 
                             winreg.KEY_READ | winreg.KEY_WRITE)
    
    try:
        path_value, _ = winreg.QueryValueEx(path_key, 'PATH')
    except WindowsError:
        path_value = ""
    
    if install_dir not in path_value:
        new_path = path_value + ";" + install_dir if path_value else install_dir
        winreg.SetValueEx(path_key, 'PATH', 0, winreg.REG_EXPAND_SZ, new_path)
        
    winreg.CloseKey(path_key)
    
    # Install required packages
    subprocess.check_call([sys.executable, "-m", "pip", "install", "windows-curses"])
    
    print(f"WMatrix has been installed to {install_dir}")
    print("It has been added to your PATH. You may need to restart your terminal or computer for the changes to take effect.")
    print("Run 'wmatrix' to start the matrix effect")
    print("Run 'wmatrix --help' to see available options")

if __name__ == "__main__":
    if not is_admin() and sys.platform == 'win32':
        print("Installing without admin privileges. WMatrix will only be available for the current user.")
    
    install_wmatrix()