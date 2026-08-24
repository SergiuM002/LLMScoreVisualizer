import customtkinter as ctk

class ToolTipMixin():
    def setup_tooltip(self, message: str, delay_ms: int = 0):
        self.message = message
        self.delay_ms = delay_ms
        self.tooltip = None
        self._tooltip_timer = None
        
        self.bind("<Enter>", self.show_tooltip, add="+")
        self.bind("<Leave>", self.hide_tooltip, add="+")

    def show_tooltip(self, event=None):
        if self._tooltip_timer is not None:
            self.after_cancel(self._tooltip_timer)
            self._tooltip_timer = None

        if self.tooltip is None:
            self._tooltip_timer = self.after(self.delay_ms, self._display_tooltip)
        
    def _display_tooltip(self):
        if self.tooltip is not None:
            return
    
        x = self.winfo_rootx() + self.winfo_width() + 5
        y = self.winfo_rooty() + 5

        self.tooltip = ctk.CTkToplevel(self)
        self.tooltip.withdraw()
        self.tooltip.wm_overrideredirect(True)  
        
        label = ctk.CTkLabel(
            self.tooltip, 
            text=self.message, 
            fg_color="#3d3d3d", 
            padx=10, pady=5,
            corner_radius=6
        )
        label.pack()
        
        self.tooltip.update_idletasks()
        self.tooltip.wm_geometry(f"+{x}+{y}")
        self.tooltip.deiconify()
        self.tooltip.lift()

    def hide_tooltip(self, event=None):
        if event:
            hovered = self.winfo_containing(event.x_root, event.y_root)
            
            is_on_tooltip = False
            if self.tooltip:
                is_on_tooltip = (hovered == self.tooltip or str(hovered).startswith(str(self.tooltip) + "."))

            # Ignore false <Leave> events if the mouse is still on self or internal children
            if hovered and not is_on_tooltip and (hovered == self or (str(hovered).startswith(str(self) + "."))):
                return
            
        if self._tooltip_timer is not None:
            self.after_cancel(self._tooltip_timer)
            self._tooltip_timer = None
            
        if self.tooltip:
            self.tooltip.destroy()
            self.tooltip = None