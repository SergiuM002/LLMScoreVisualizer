import customtkinter as ctk
from ui.components.tool_tip_mixin import ToolTipMixin

class TooltipButton(ctk.CTkButton, ToolTipMixin):
    """Button with tooltip."""
    def __init__(self, master, tooltip_message, **kwargs):
        super().__init__(master, **kwargs)
        
        self.setup_tooltip(tooltip_message, delay_ms=1000)