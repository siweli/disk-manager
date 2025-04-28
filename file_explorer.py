import os
import json
import tkinter as tk
from tkinter import ttk

class FolderExplorer(tk.Frame):
    def __init__(self, master, data, base_dir):
        super().__init__(master)
        self.master = master
        self.size_map = {
            os.path.normpath(path): size
            for path, size in data.items()
        }
        self.base_dir = os.path.normpath(base_dir)

        # track current directory (None for initial view)
        self.current_path = None

        # navigation controls
        nav_frame = tk.Frame(self)
        nav_frame.pack(fill=tk.X)
        self.btn_up = tk.Button(nav_frame, text='Up', command=self.go_up)
        self.btn_up.pack(side=tk.LEFT)
        self.lbl_path = tk.Label(nav_frame, text=self.base_dir)
        self.lbl_path.pack(side=tk.LEFT, padx=10)
        self.btn_copy = tk.Button(nav_frame, text='Copy Path', command=self.copy_path)
        self.btn_copy.pack(side=tk.RIGHT)

        # treeview for folder list
        self.tree = ttk.Treeview(self, columns=('size',), show='tree headings')
        self.tree.heading('#0', text='Folder')
        self.tree.column('#0', width=300, anchor='w')
        self.tree.heading('size', text='Size')
        self.tree.column('size', width=120, anchor='e')
        self.tree.pack(fill=tk.BOTH, expand=True)
        self.tree.bind('<Double-1>', self.enter_folder)

        self.refresh_view()



    def refresh_view(self):
        # update buttons & path label
        if self.current_path:
            self.btn_up.config(state=tk.NORMAL)
            self.lbl_path.config(text=self.current_path)
            self.btn_copy.config(state=tk.NORMAL)
        else:
            self.btn_up.config(state=tk.DISABLED)
            self.lbl_path.config(text=self.base_dir)
            self.btn_copy.config(state=tk.DISABLED)

        # clear any existing items
        for iid in self.tree.get_children():
            self.tree.delete(iid)

        entries = {}

        if self.current_path is None:
            # show just the base directory itself
            entries[self.base_dir] = self.size_map.get(self.base_dir, 0)
        else:
            # list only direct children of current_path
            current = self.current_path
            try:
                with os.scandir(current) as it:
                    for entry in it:
                        if not entry.is_dir(follow_symlinks=False):
                            continue
                        full = os.path.normpath(entry.path)
                        entries[full] = self.size_map.get(full, 0)
            except Exception:
                pass

        # populate the treeview
        for full_path, total_size in sorted(
            entries.items(),
            key=lambda item: item[1],
            reverse=True
        ):
            display = os.path.basename(full_path.rstrip(os.sep))
            if not display:
                display = full_path # e.g. 'C:\\' drive root
            self.tree.insert(
                '', 'end',
                iid=full_path,
                text=display,
                values=(self.format_size(total_size),)
            )




    def enter_folder(self, event):
        sel = self.tree.focus()
        if sel:
            # only allow entering base or subfolders
            self.current_path = sel
            self.refresh_view()



    def go_up(self):
        if not self.current_path:
            return
        parent = os.path.dirname(self.current_path)
        # if parent is still under base_dir, go up; otherwise go to initial view
        if parent and parent.startswith(self.base_dir):
            self.current_path = parent
        else:
            self.current_path = None
        self.refresh_view()



    def copy_path(self):
        if self.current_path:
            self.master.clipboard_clear()
            self.master.clipboard_append(self.current_path)



    def format_size(self, size_bytes):
        size = float(size_bytes)
        for unit in ['B','KB','MB','GB','TB']:
            if size < 1024:
                return f"{size:.2f} {unit}"
            size /= 1024
        return f"{size:.2f} PB"




def create_file_explorer(base, data):
    # create the file explorer
    root = tk.Tk()
    root.title("Folder Explorer")
    explorer = FolderExplorer(root, data, base)
    explorer.pack(fill=tk.BOTH, expand=True)
    root.mainloop()



if __name__ == '__main__':
    # if run in main thread then open last save and show that
    print('opening last saved file map')
    start_path = 'C:\\'
    with open(r'C:\Users\siwel\Desktop\computing\cool\folder manager\size_map.json', 'r') as f:
        data = json.load(f)
    print('done')

    create_file_explorer(start_path, data)