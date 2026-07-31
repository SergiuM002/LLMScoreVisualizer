import customtkinter as ctk
from config.styles import Theme

class PlotSelection(ctk.CTkFrame):
    def __init__(self, controller, master, **kwargs):   
        super().__init__(master, fg_color="transparent", **kwargs)
        
        self.master = master
        self.controller = controller   
        
        self.plot_buttons = []
        
        self.select_plot_label = ctk.CTkLabel(
            self,
            text="Select a Plot Type:",
            font=("Roboto", 18),
            text_color=Theme.GENERAL_LABEL
        )
        self.select_plot_label.pack(pady=20, padx=20)
        
        self.scroll_frame = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.scroll_frame.pack(fill="both", expand=True)  
        
        self.msic_profile = ctk.CTkFrame(
            self.scroll_frame, 
            height=180,
            width=180,
            fg_color=Theme.GRAY_BUTTON,
        )
        
        self.msic_profile.pack_propagate(False)
        self.msic_profile.pack(anchor=ctk.W, padx=(80, 30), pady=50)
        
        self.msic_profile_label = ctk.CTkLabel(
            self.msic_profile, 
            text="MSIC-Profile",
            text_color=Theme.GRAY_BUTTON_TEXT
        )
        self.msic_profile_label.pack(pady=5)
        self.plot_buttons.append(self.msic_profile)
        
        self.controller.apply_bindings(self)
        
        
    
        
        
        
        