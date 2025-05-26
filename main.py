import tkinter as tk
from tkinter import messagebox, scrolledtext,filedialog
import json
from enum import Enum
from huffman_encode import encode_huffman as eh
from huffman_decode import decompress_huffman as dh

class ActionType(Enum):
    ENCODE = "Mã hoá"
    DECODE = "Giải mã"

# === Khởi tạo GUI ===
root = tk.Tk()
root.title("Huffman Tool")
root.geometry("950x600")
action_type = tk.StringVar()
action_type.set(ActionType.ENCODE.value)

selected_file:str|None = None

def update_action_type(act_type):
    action_type.set(act_type)
    print(act_type)

def select_file():
    if action_type.get()==ActionType.DECODE.value:
        file_path = filedialog.askopenfilename(
            title="Select File",
            filetypes=[("Huffman file","*.huff")]
        )
    else: file_path = filedialog.askopenfilename(
        title="Select File",
        filetypes=[("Any","*")]
    )
    if file_path:
        entry.config(state='normal')
        entry.delete(0,tk.END)
        entry.insert(0,file_path)
        entry.config(state='readonly')
        return file_path
    return None

def open_file():
    global selected_file
    selected_file = select_file()

# === Thực hiện hành động chính ===
def process_action():
    if not selected_file:
        messagebox.showerror("Lỗi", "Chưa chọn file.")
        return

    try:
        if action_type.get() == ActionType.ENCODE.value:
            [output_path,mapping_path] = eh(selected_file)
            with open(mapping_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                pretty_text = json.dumps(data, indent=4, ensure_ascii=False)
                custom_input.delete("1.0", tk.END)
                custom_input.insert(tk.END, pretty_text)
            log_text.config(state='normal')
            log_text.insert(tk.END,f"✅ Compressed file: {output_path}\n")
            log_text.insert(tk.END,f"✅ Huffman table: {mapping_path}\n")
            log_text.config(state='disabled')

        elif selected_file.endswith(".huff"):
            base = '.'.join(selected_file.split('.')[:-2])
            table_path = f"{base}_mapping.json"
            with open(table_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                pretty_text = json.dumps(data, indent=4, ensure_ascii=False)
                custom_input.delete("1.0", tk.END)
                custom_input.insert(tk.END, pretty_text)

            output_path = dh(selected_file, table_path)
            log_text.config(state='normal')
            log_text.insert(tk.END,f"✅ File đã giải mã: {output_path}\n")
            log_text.config(state='disabled')

    except Exception as e:
        log_text.insert(tk.END, f"❌ Lỗi xử lý: {e}\n")

# === Giao diện ===

# Container chính
main_container = tk.Frame(root, bg='#f8f9fa')
main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

# Header
header_frame = tk.Frame(main_container, bg='#343a40', height=60)
header_frame.pack(fill=tk.X, pady=(0, 20))
header_frame.pack_propagate(False)

header_label = tk.Label(header_frame, text="HUFFMAN COMPRESSION TOOL", 
                       font=('Arial', 14, 'bold'), fg='white', bg='#343a40')
header_label.pack(expand=True)

# Control panel
control_panel = tk.LabelFrame(main_container, text="Điều khiển", 
                             font=('Arial', 11, 'bold'), bg='#e9ecef', 
                             fg='#495057', relief=tk.GROOVE, bd=2)
control_panel.pack(fill=tk.X, pady=(0, 20))

# Hàng 1: Chọn chức năng
func_frame = tk.Frame(control_panel, bg='#e9ecef')
func_frame.pack(fill=tk.X, padx=15, pady=10)

tk.Label(func_frame, text="Chức năng:", font=('Arial', 10, 'bold'), 
         bg='#e9ecef', fg='#495057').pack(side=tk.LEFT)

actions = [act.value for act in ActionType]
action_menu = tk.OptionMenu(func_frame, action_type, *actions, command=update_action_type)
action_menu.config(bg='#6c757d', fg='white', font=('Arial', 9), 
                  activebackground='#5a6268', relief=tk.RAISED, bd=1)
action_menu.pack(side=tk.LEFT, padx=(10, 0))

# Hàng 2: Chọn file
file_frame = tk.Frame(control_panel, bg='#e9ecef')
file_frame.pack(fill=tk.X, padx=15, pady=(0, 10))

tk.Label(file_frame, text="File:", font=('Arial', 10, 'bold'), 
         bg='#e9ecef', fg='#495057').pack(side=tk.LEFT)

entry = tk.Entry(file_frame, width=50, font=('Arial', 9), 
                relief=tk.SUNKEN, bd=1, bg='white')
entry.pack(side=tk.LEFT, padx=(10, 10), fill=tk.X, expand=True)
entry.config(state='readonly')

tk.Button(file_frame, text="Duyệt", command=open_file,
          bg='#007bff', fg='white', font=('Arial', 9, 'bold'),
          relief=tk.RAISED, bd=2, width=8).pack(side=tk.RIGHT)

# Hàng 3: Nút thực hiện
execute_frame = tk.Frame(control_panel, bg='#e9ecef')
execute_frame.pack(fill=tk.X, padx=15, pady=(0, 15))

tk.Button(execute_frame, text="🚀 THỰC HIỆN", command=process_action,
          bg='#28a745', fg='white', font=('Arial', 11, 'bold'),
          relief=tk.RAISED, bd=3, height=2).pack()

# Workspace area
workspace = tk.Frame(main_container, bg='#f8f9fa')
workspace.pack(fill=tk.BOTH, expand=True)

# Bảng Huffman (trái)
huffman_frame = tk.LabelFrame(workspace, text="📊 Bảng mã Huffman", 
                             font=('Arial', 10, 'bold'), bg='#d4edda', 
                             fg='#155724', relief=tk.GROOVE, bd=2)
huffman_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))

custom_input = scrolledtext.ScrolledText(huffman_frame, wrap=tk.WORD, 
                                        font=('Consolas', 9), bg='#f8f9fa',
                                        relief=tk.SUNKEN, bd=1)
custom_input.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

# Log (phải)
log_frame = tk.LabelFrame(workspace, text="📝 Nhật ký", 
                         font=('Arial', 10, 'bold'), bg='#fff3cd', 
                         fg='#856404', relief=tk.GROOVE, bd=2)
log_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(10, 0))

log_text = scrolledtext.ScrolledText(log_frame, wrap=tk.WORD, 
                                    font=('Consolas', 9), bg='#fffbf0',
                                    relief=tk.SUNKEN, bd=1)
log_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
log_text.config(state='disabled')

root.mainloop()