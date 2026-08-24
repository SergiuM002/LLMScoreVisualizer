import customtkinter as ctk
from customtkinter import filedialog
from config.styles import Theme
import config.environment as env
import subprocess
from CTkMessagebox import CTkMessagebox
from ui.components.file_button import FileButton
from ui.error_popup import ErrorPopup

class CSVImportMenu(ctk.CTkToplevel):   
    def __init__(self, controller, master, *args, **kwargs):   
        super().__init__(*args, **kwargs)
       
        self.master = master
        self.controller = controller   
        controller.connect_view(self)
        
        self.csv_buttons = []
        
        self.attributes("-topmost", False)
        self.title("Import CSVs")
        self.withdraw()
        
        controller.set_window_size_and_pos()
        
        self.resizable(False, False)
        
        self.csv_label = ctk.CTkLabel(
            self,
            font=("Roboto", 16),
            text_color=("gray20", "white"),
            text="CSV Files"
        )
        self.csv_label.pack(pady=(15, 10))
        
        self.csv_button_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.csv_button_frame.pack(anchor=ctk.W, padx=20, pady=(0, 10))
        
        self.csv_remove = ctk.CTkButton(
            self.csv_button_frame,
            text="-",
            command=self.remove_csv_clicked,
            font=("Roboto", 18),
            height=30,
            width=30,
            text_color=Theme.GRAY_BUTTON_TEXT,
            fg_color=Theme.GRAY_BUTTON,
            hover_color=Theme.GRAY_BUTTON_HOVER,
            state="disabled"
        )
        self.csv_remove.pack(side=ctk.LEFT, padx=(0, 3))
        
        self.csv_add = ctk.CTkButton(
            self.csv_button_frame,
            text="+",
            command=self.add_csv_clicked,
            font=("Roboto", 18),
            height=30,
            width=30,
            text_color=Theme.GRAY_BUTTON_TEXT,
            fg_color=Theme.GRAY_BUTTON,
            hover_color=Theme.GRAY_BUTTON_HOVER
        )
        self.csv_add.pack(side=ctk.LEFT)
        
        self.csv_scrollframe = ctk.CTkScrollableFrame(self)
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
        
        controller.load_imported_files()
        
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

    def add_csv_clicked(self):
        if env.OPERATING_SYSTEM == "Linux":
            try:
                file_path = subprocess.check_output(
                    [
                        'zenity', 
                        '--file-selection', 
                        '--title=Select a CSV file', 
                        '--file-filter=CSV files | *.csv'
                    ],
                    stderr=subprocess.DEVNULL
                ).decode('utf-8').strip()
            except subprocess.CalledProcessError:
                return
        else:
            file_path = filedialog.askopenfilename(title="Select a file", filetypes=[("GenBank files", "*.gb *.gbk")])
            
        if file_path:
            self.controller.add_csv(file_path)
            
    def show_already_imported_error(self):
        scaling = self.controller.main_ctrl.height_quo
        ErrorPopup(self.controller.main_ctrl.root, scaling, "File is already imported.")
                
    def show_invalid_file_extension_error(self):
        scaling = self.controller.main_ctrl.height_quo
        ErrorPopup(self.controller.main_ctrl.root, scaling, "File is not a CSV file.")
                
    def show_invalid_columns_error(self, column):
        scaling = self.controller.main_ctrl.height_quo
        ErrorPopup(self.controller.main_ctrl.root, scaling, f"Missing required column: {column}.")    
        
    def show_invalid_msic_error(self):
        scaling = self.controller.main_ctrl.height_quo
        ErrorPopup(self.controller.main_ctrl.root, scaling, "One or more MSIC values are out range ([-1;1]).")       
        
    def show_invalid_nucleotide_error(self):
        scaling = self.controller.main_ctrl.height_quo
        ErrorPopup(self.controller.main_ctrl.root, scaling, "One or more values in the 'ref' column are not nucleotides (a, c, g, t).")        
            
    def csv_clicked(self, button):
        self.controller.toggle_csv(button)
        
    def remove_csv_clicked(self):
        self.controller.remove_csv()

    def confirm_clicked(self):
        self.controller.confirm_files()
        self.on_close()
        
    def on_close(self):
        self.master.file_selection_button.configure(state="normal")
        self.destroy()
    

        
        