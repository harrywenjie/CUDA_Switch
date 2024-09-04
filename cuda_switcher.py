import os
import tkinter as tk
from tkinter import messagebox
import winreg as reg

def get_current_cuda_version():
    cuda_path = os.environ.get('CUDA_PATH', '')
    if 'CUDA_PATH_V11_8' in os.environ and os.environ['CUDA_PATH_V11_8'] in cuda_path:
        return '11.8'
    elif 'CUDA_PATH_V12_5' in os.environ and os.environ['CUDA_PATH_V12_5'] in cuda_path:
        return '12.5'
    else:
        return 'Unknown'

def update_cuda_version_label():
    current_version = get_current_cuda_version()
    cuda_version_label.config(text=f"Current CUDA Version: {current_version}")

def set_cuda_version(version):
    if version == '11.8':
        cuda_path = os.environ.get('CUDA_PATH_V11_8')
        cuda_bins = [
            r'C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v11.8\bin',
            r'C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v11.8\libnvvp',
            r'C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v12.5\bin',
            r'C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v12.5\libnvvp',
        ]
    elif version == '12.5':
        cuda_path = os.environ.get('CUDA_PATH_V12_5')
        cuda_bins = [
            r'C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v12.5\bin',
            r'C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v12.5\libnvvp',
            r'C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v11.8\bin',
            r'C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v11.8\libnvvp'
            r'c:\program files\nvidia\cudnn\v8.x\bin'
            r'c:\program files\nvidia\cudnn\v9.1\bin'
        ]
    else:
        messagebox.showerror("Error", "Invalid CUDA version selected")
        return

    if cuda_path:
        try:
            # Update CUDA_PATH in the system environment
            reg_key = reg.OpenKey(reg.HKEY_LOCAL_MACHINE, r"SYSTEM\CurrentControlSet\Control\Session Manager\Environment", 0, reg.KEY_SET_VALUE)
            reg.SetValueEx(reg_key, "CUDA_PATH", 0, reg.REG_SZ, cuda_path)
            reg.CloseKey(reg_key)
            
            # Update PATH in the system environment
            reg_key = reg.OpenKey(reg.HKEY_LOCAL_MACHINE, r"SYSTEM\CurrentControlSet\Control\Session Manager\Environment", 0, reg.KEY_READ | reg.KEY_WRITE)
            path_value, reg_type = reg.QueryValueEx(reg_key, "NEW_CUDA_PATH")
            paths = path_value.split(';')
            
            # Remove existing CUDA paths regardless of their order and position
            paths = [p for p in paths if not any(cb in p for cb in [
                r'C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v11.8\bin',
                r'C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v11.8\libnvvp',
                r'C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v12.5\bin',
                r'C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v12.5\libnvvp'
                r'c:\program files\nvidia\cudnn\v8.x\bin'
                r'c:\program files\nvidia\cudnn\v9.1\bin'
            ])]
            
            # Prepend the selected CUDA paths
            paths = cuda_bins + paths
            new_path_value = ';'.join(paths)
            reg.SetValueEx(reg_key, "NEW_CUDA_PATH", 0, reg_type, new_path_value)
            reg.CloseKey(reg_key)
            
            # Update the environment variable in the current session
            os.environ['CUDA_PATH'] = cuda_path
            
            messagebox.showinfo("Success", f"Switched to CUDA {version}")
            update_cuda_version_label()
        except PermissionError:
            messagebox.showerror("Error", "Permission denied. Please run the script as an administrator.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to set CUDA_PATH: {e}")
    else:
        messagebox.showerror("Error", f"CUDA_PATH_V{version.replace('.', '_')} is not set")

def switch_to_11_8():
    set_cuda_version('11.8')

def switch_to_12_5():
    set_cuda_version('12.5')

root = tk.Tk()
root.title("CUDA Version Switcher")

cuda_version_label = tk.Label(root, text=f"Current CUDA Version: {get_current_cuda_version()}")
cuda_version_label.pack(pady=10)

button_11_8 = tk.Button(root, text="Switch to CUDA 11.8", command=switch_to_11_8)
button_11_8.pack(pady=10)

button_12_5 = tk.Button(root, text="Switch to CUDA 12.5", command=switch_to_12_5)
button_12_5.pack(pady=10)

root.mainloop()
