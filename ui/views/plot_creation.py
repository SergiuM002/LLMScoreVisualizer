import subprocess
import customtkinter as ctk
from customtkinter import filedialog
from config.styles import Theme
from CTkMessagebox import CTkMessagebox
from ui.views.csv_import_menu import CSVImportMenu
from controllers.views.csv_import_menu_controller import CSVImportMenuController
import config.environment as env

class PlotCreation(ctk.CTkFrame):   
    def __init__(self, controller, master, **kwargs):   
        super().__init__(master, fg_color="transparent", **kwargs)
        
        self.controller = controller
        
        controller.set_window_size()
    
        self.button_frame1 = ctk.CTkFrame(self, fg_color="transparent")
        self.button_frame1.pack(fill="x", padx=20, pady=(20, 0))
        
        self.back_button = ctk.CTkButton(
            self.button_frame1,
            height=30,
            text="Back",
            font=("Roboto", 15),
            text_color=Theme.GREEN_BUTTON_TEXT,
            fg_color=Theme.GREEN_BUTTON,
            hover_color=Theme.GREEN_BUTTON_HOVER,
            command=controller.main_ctrl.show_plot_selection_screen
        )
        self.back_button.pack(side=ctk.LEFT, anchor=ctk.N, pady=10)
        
        self.confirm_frame = ctk.CTkFrame(self.button_frame1, fg_color="transparent")
        self.confirm_frame.pack(side=ctk.RIGHT, anchor="s")
        
        self.save_plots_button = ctk.CTkButton(
            self.confirm_frame,
            height=30,
            text="Save All Plots",
            font=("Roboto", 15),
            text_color=Theme.GREEN_BUTTON_TEXT,
            fg_color=Theme.GREEN_BUTTON,
            hover_color=Theme.GREEN_BUTTON_HOVER,
            command=self.save_plots_button_clicked
        )
        self.save_plots_button.pack(side=ctk.BOTTOM, pady=5)
        
        self.file_selection_button = ctk.CTkButton(
            self.confirm_frame,
            height=30,
            text="Import CSVs",
            font=("Roboto", 15),
            fg_color=Theme.GRAY_BUTTON,
            text_color=Theme.GRAY_BUTTON_TEXT,
            hover_color=Theme.GRAY_BUTTON_HOVER,
            command=self.import_csvs
        )
        self.file_selection_button.pack(side=ctk.BOTTOM, padx=5, pady=5)        
        
        self.extension_selection = ctk.StringVar(value=".pdf")
        self.save_plots_extension = ctk.CTkComboBox(
            self.button_frame1,
            width=70,
            height=25,
            state="readonly",
            variable=self.extension_selection,
            values=[".pdf", ".png", ".jpg"],
            font=("Roboto", 13),
            text_color=("gray20", "white"),
        )
        self.save_plots_extension.pack(side=ctk.RIGHT, anchor=ctk.S, pady=5, padx=3)
        
        self.divider = ctk.CTkFrame(self, fg_color=("gray80", "#444444"), height=2)
        self.divider.pack(fill="x", padx=15, pady=20)
        
        self.plot_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.plot_frame.pack(fill="both", expand=True)
        
    def show_no_file_error(self):
        scaling = self.controller.main_ctrl.height_quo
        CTkMessagebox(
            master=self.controller.main_ctrl.root,
            title="Error",
            message="No imported files found.",
            icon="cancel",
            width=int(400*scaling),
            height=int(200*scaling),
            button_width=int(130*scaling),
            button_height=int(40*scaling),
            button_color=Theme.GREEN_BUTTON,
            button_hover_color=Theme.GREEN_BUTTON_HOVER
        )  
        
    def import_csvs(self):
        self.file_selection_button.configure(state="disabled")
        CSVImportMenu(CSVImportMenuController(self.controller.main_ctrl), self)
        
    def preview_plot_clicked(self):
        if len(self.controller.file_list) == 0:
            self.show_no_file_error()
            
        self.controller.preview_plot()
        
    def save_plots_button_clicked(self):
        if len(self.controller.file_list) == 0:
            self.show_no_file_error()
                    
        output_path = ""
        
        if env.OPERATING_SYSTEM == "Linux": 
            try:
                output_path = subprocess.check_output(
                    [
                        'zenity', 
                        '--file-selection', 
                        '--directory', 
                        '--title=Select a Path', 
                    ],
                    stderr=subprocess.DEVNULL
                ).decode('utf-8').strip()
            except subprocess.CalledProcessError:
                return None
        else:
            output_path = filedialog.askdirectory(title="Select a Path") 
            
        self.controller.save_all_plots(self, output_path)
        
   
        
    