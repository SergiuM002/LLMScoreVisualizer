import customtkinter as ctk
from config.styles import Theme
import config.environment as env
from ui.components.image_frame import ImageFrame

class PlotSelection(ctk.CTkFrame):
    def __init__(self, controller, master, **kwargs):   
        super().__init__(master, fg_color="transparent", **kwargs)
        
        self.master = master
        self.controller = controller   
        
        self.plot_buttons = []
        
        self.select_plot_label = ctk.CTkLabel(
            self,
            text="Select a Plot Type:",
            font=("Roboto", 22),
            text_color=Theme.GENERAL_LABEL
        )
        self.select_plot_label.pack(pady=20, padx=20)
        
        self.scroll_frame = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.scroll_frame.pack(fill="both", expand=True) 
        
        self.button_frame = ctk.CTkFrame(self.scroll_frame, fg_color="transparent", width=650, height=650)
        self.button_frame.pack(expand=True)
        self.button_frame.grid_propagate(False)
        
        self.button_frame.columnconfigure((0, 1), weight=1, uniform="equal_cols")
        self.button_frame.rowconfigure((0, 1, 2,), weight=1, uniform="equal_rows") 
        
        self.msic_profile = ctk.CTkFrame(
            self.button_frame, 
            height=180,
            width=180,
            fg_color=Theme.GRAY_BUTTON,
        )
        
        self.msic_profile.pack_propagate(False)
        self.msic_profile.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        
        self.msic_profile_label = ctk.CTkLabel(
            self.msic_profile, 
            text="MSIC-Profile",
            text_color=Theme.GRAY_BUTTON_TEXT
        )
        self.msic_profile_label.pack(pady=10)
        
        self.msic_profile_image = ImageFrame(self.msic_profile, env.IMAGES_DIR / "MSIC_Preview.png", (240, 120))
        self.msic_profile_image.pack()
        
        self.plot_buttons.append(self.msic_profile)
        
        self.controller.apply_bindings(self)
        
        
    
        
        
        
        