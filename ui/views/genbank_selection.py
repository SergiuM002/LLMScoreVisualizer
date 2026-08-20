import customtkinter as ctk
from customtkinter import filedialog
from config.styles import Theme
from ui.components.file_button import FileButton
from CTkMessagebox import CTkMessagebox
import config.environment as env
import subprocess

class GenbankSelection(ctk.CTkToplevel):   
    def __init__(self, controller, master, *args, **kwargs):   
        super().__init__(*args, **kwargs)
       
        self.master = master
        self.controller = controller   
        controller.connect_view(self)
        
        self.csv_buttons = []
        self.genbank_buttons = []
        
        self.attributes("-topmost", False)
        self.title("Genbank Selection")
        self.withdraw()
        
        win_width = round(600)
        win_height = round(490)
        
        self.geometry(f"{win_width}x{win_height}+{round(master.controller.center_x-win_width/2)}+{round(master.controller.center_y-win_height/2)}")
        self.resizable(False, False)
        
        self.select_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.select_frame.pack(fill="both", expand=True)
        
        self.select_frame.grid_columnconfigure(0, weight=1)
        self.select_frame.grid_columnconfigure(1, weight=0)
        self.select_frame.grid_columnconfigure(2, weight=1)
        self.select_frame.grid_rowconfigure(0, weight=1)
        
        self.genbank_frame = ctk.CTkFrame(self.select_frame, fg_color="transparent")
        self.genbank_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady= 10)
        
        self.genbank_label = ctk.CTkLabel(
            self.genbank_frame,
            font=("Roboto", 16),
            text_color=("gray20", "white"),
            text="GenBank Files"
        )
        self.genbank_label.pack(pady=20)
        
        self.genbank_button_frame = ctk.CTkFrame(self.genbank_frame, fg_color="transparent")
        self.genbank_button_frame.pack(anchor=ctk.W, padx=20, pady=(0, 10))
        
        self.genbank_remove = ctk.CTkButton(
            self.genbank_button_frame,
            text="-",
            command=self.remove_genbank_clicked,
            font=("Roboto", 18),
            height=30,
            width=30,
            text_color=Theme.GRAY_BUTTON_TEXT,
            fg_color=Theme.GRAY_BUTTON,
            hover_color=Theme.GRAY_BUTTON_HOVER,
            state="disabled"
        )
        self.genbank_remove.pack(side=ctk.LEFT)
        
        self.genbank_add = ctk.CTkButton(
            self.genbank_button_frame,
            text="+",
            command=self.add_genbank_clicked,
            font=("Roboto", 18),
            height=30,
            width=30,
            text_color=Theme.GRAY_BUTTON_TEXT,
            fg_color=Theme.GRAY_BUTTON,
            hover_color=Theme.GRAY_BUTTON_HOVER
        )
        self.genbank_add.pack(side=ctk.LEFT, padx=5)
        
        self.genbank_scrollframe = ctk.CTkScrollableFrame(self.genbank_frame)
        self.genbank_scrollframe.pack(padx=20, fill="both", expand=True)
        
        self.divider = ctk.CTkFrame(
            self.select_frame, 
            fg_color=("gray80", "#444444"),
            width=2
        )
        self.divider.grid(row=0, column=1, sticky="ns", padx=10, pady= 10)
        
        self.csv_frame = ctk.CTkFrame(self.select_frame, fg_color="transparent")
        self.csv_frame.grid(row=0, column=2, sticky="nsew", padx=10, pady= 10)
        
        self.csv_label = ctk.CTkLabel(
            self.csv_frame,
            font=("Roboto", 16),
            text_color=("gray20", "white"),
            text="CSV Files"
        )
        self.csv_label.pack(pady=(20, 60))
        
        self.csv_scrollframe = ctk.CTkScrollableFrame(self.csv_frame)
        self.csv_scrollframe.pack(padx=20, fill="both", expand=True)
        
        self.confirm_button = ctk.CTkButton(
            self, 
            text="Confirm",
            command=self.confirm_clicked,
            height=30,
            font=("Roboto", 13),
            text_color=Theme.GREEN_BUTTON_TEXT,
            fg_color=Theme.GREEN_BUTTON,
            hover_color=Theme.GREEN_BUTTON_HOVER,
        )
        self.confirm_button.pack(side=ctk.BOTTOM, pady=(15))
        
        controller.load_imported_csvs()
        controller.csvs_set_disabled_all()
        controller.load_imported_genbanks()
        
        self.deiconify()
        
        self.protocol("WM_DELETE_WINDOW", self.on_close)
        
    def pack_csv_button(self, file_name, file_path, info):
        new_button = FileButton(
            controller=self.controller,
            master=self.csv_scrollframe,  
            filename=file_name,
            info=info,
            file_path=file_path,
            function=lambda: self.csv_clicked(new_button)
        )
        new_button.pack(pady=(5, 0))
        self.csv_buttons.append(new_button)
        
    def pack_genbank_button(self, file_name, file_path, info):
        new_button = FileButton(
            controller=self.controller,
            master=self.genbank_scrollframe,  
            filename=file_name,
            info=info,
            file_path=file_path,
            function=lambda: self.genbank_clicked(new_button)
        )
        new_button.pack(pady=(5, 0))
        self.genbank_buttons.append(new_button)
        
    def genbank_clicked(self, button):
        self.controller.toggle_genbank(button)
        
    def csv_clicked(self, button):
        self.controller.toggle_csv(button)
        
    def remove_genbank_button(self, file_path):
        button = next((btn for btn in self.genbank_buttons if btn.file_path == file_path))
        self.genbank_buttons.remove(button)
        button.destroy()

    def add_genbank_clicked(self):
        if env.OPERATING_SYSTEM == "Linux":
            try:
                file_path = subprocess.check_output(
                    [
                        'zenity', 
                        '--file-selection', 
                        '--title=Select a GenBank file', 
                        '--file-filter=GenBank files | *.gb *.gbk'
                    ],
                    stderr=subprocess.DEVNULL
                ).decode('utf-8').strip()
            except subprocess.CalledProcessError:
                return None
        else:
            file_path = filedialog.askopenfilename(title="Select a file", filetypes=[("GenBank files", "*.gb *.gbk")])
            
        if file_path:
            self.controller.add_genbank(file_path)
        
    def remove_genbank_clicked(self):
        self.controller.remove_genbank()
        
    def show_already_imported_error(self):
        scaling = self.controller.main_ctrl.height_quo
        CTkMessagebox(
            master=self.controller.main_ctrl.root,
            title="Error",
            message="File is already imported.",
            icon="cancel",
            width=int(400*scaling),
            height=int(200*scaling),
            button_width=int(110*scaling),
            button_height=int(35*scaling),
            button_color=Theme.GREEN_BUTTON,
            button_hover_color=Theme.GREEN_BUTTON_HOVER
        )  

    def confirm_clicked(self):
        self.controller.pass_genbank_binds()
        self.master.genbank_upload_text.set("imported ✓")
        self.on_close()
        
    def on_close(self):
        self.master.genbank_button.configure(state="normal")
        self.destroy()

        
        