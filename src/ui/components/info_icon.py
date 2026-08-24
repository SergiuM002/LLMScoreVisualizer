import customtkinter as ctk
from ui.components.tool_tip_mixin import ToolTipMixin

class InfoIcon(ctk.CTkLabel, ToolTipMixin):
    def __init__(self, master, message, bg_color="transparent", **kwargs):
        super().__init__(
            master, 
            text="?", 
            width=20, 
            height=20, 
            corner_radius=10,
            bg_color=bg_color,
            fg_color="gray30", 
            text_color="white",
            font=("Arial", 12, "bold"),
            **kwargs
        )
        
        self.setup_tooltip(message)