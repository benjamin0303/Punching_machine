import os
import winshell
from win32com.client import Dispatch
import sys

def create_desktop_shortcut(target_path, shortcut_name):
    desktop = winshell.desktop()
    shortcut_path = os.path.join(desktop, f"{shortcut_name}.lnk")
    
    shell = Dispatch('WScript.Shell')
    shortcut = shell.CreateShortCut(shortcut_path)

    # pythonw.exe의 정확한 경로 설정
    python_dir = os.path.dirname(sys.executable)
    pythonw_path = os.path.join(python_dir, 'pythonw.exe')

    if os.path.exists(pythonw_path):
        python_path = pythonw_path
    else:
        # pythonw.exe가 없으면 python.exe 사용
        python_path = sys.executable

    print(f"사용되는 Python 경로: {python_path}")
    shortcut.Targetpath = python_path
    shortcut.Arguments = f'"{target_path}"'
    shortcut.WorkingDirectory = os.path.dirname(target_path)
    shortcut.WindowStyle = 1
    shortcut.save()

# 사용 예시
program_path = r"C:\Users\benja\Punch_time_clock\punch_box.py"
shortcut_name = "PunchMe"
create_desktop_shortcut(program_path, shortcut_name)

