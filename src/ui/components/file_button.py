import customtkinter as ctk
from config.styles import Theme
from ui.components.info_icon import InfoIcon

# The object the CSV and GenBank buttons use
class FileButton(ctk.CTkButton):
    def __init__(self, controller, master, filename, file_path, info=None, function=None, **kwargs):   
        self.normal_color = Theme.GRAY_BUTTON
        self.hover_color = Theme.GRAY_BUTTON_HOVER
        
        super().__init__(
            master, 
            text="",                        
            text_color=Theme.GRAY_BUTTON_TEXT,                       
            fg_color=Theme.GRAY_BUTTON, 
            hover_color=Theme.GRAY_BUTTON_HOVER,                        
            corner_radius=8, 
            border_width=0, 
            command=function,
            **kwargs
        )
       
        self.master = master
        self.controller = controller   
        self.filename = filename
        self.info = info
        self.file_path = file_path
        self.function = function
        
        self.selected = False
        self.enabled = True
        
        self.file_label = ctk.CTkLabel( 
            self,
            text=filename,
            font=("Roboto", 13),
            text_color=Theme.GRAY_BUTTON_TEXT,
            fg_color="transparent",
            bg_color="transparent"
        )
        self.file_label.grid(row=0, column=0, padx=(10, 5), sticky="w")
        
        if (info):
            self.infoicon = InfoIcon(self, message=info, bg_color=Theme.GRAY_BUTTON)
            self.infoicon.grid(row=0, column=1, padx=(0, 10), pady=6, sticky="w")
            
        self.bind("<Enter>", self._on_hover_start, add="+")
        self.bind("<Leave>", self._on_hover_end, add="+")
        self.file_label.bind("<Enter>", self._on_hover_start, add="+")
        self.file_label.bind("<Leave>", self._on_hover_end, add="+")
        
        if function:
            self.file_label.bind("<ButtonRelease-1>", lambda e: self.button_fuction())
            
    def button_fuction(self):
        if self.enabled:
            self.function()
            
    def set_enabled(self, enabled: bool):
        self.enabled = enabled
        
        if enabled:
            if self.selected:
                self.normal_color = Theme.GREEN_BUTTON
                self.hover_color = Theme.GREEN_BUTTON_HOVER
                self.configure(hover_color=Theme.GREEN_BUTTON_HOVER)  
            else:
                self.normal_color = Theme.GRAY_BUTTON
                self.hover_color = Theme.GRAY_BUTTON_HOVER
                self.configure(hover_color=Theme.GRAY_BUTTON_HOVER)  
        else:
            if self.selected:
                self.normal_color = Theme.BLUE_BUTTON
                self.hover_color = Theme.BLUE_BUTTON
                self.configure(hover_color=Theme.BLUE_BUTTON)   
            else:
                self.normal_color = Theme.GRAY_BUTTON
                self.hover_color = Theme.GRAY_BUTTON
                self.configure(hover_color=Theme.GRAY_BUTTON)     
            
        self._apply_color(self.normal_color)
            
    def set_selected(self, selected: bool):
        self.selected = selected
        
        if selected:
            self.normal_color = Theme.GREEN_BUTTON
            self.hover_color = Theme.GREEN_BUTTON_HOVER
            self.configure(hover_color=Theme.GREEN_BUTTON_HOVER)
        else:
            self.normal_color = Theme.GRAY_BUTTON
            self.hover_color = Theme.GRAY_BUTTON_HOVER
            self.configure(hover_color=Theme.GRAY_BUTTON_HOVER)
            
        self._apply_color(self.hover_color)        
        
    def _apply_color(self, color):
        self.configure(fg_color=color)
        self.file_label.configure(bg_color=color)
        if hasattr(self, "infoicon"):
            self.infoicon.configure(bg_color=color)
        
    def _on_hover_start(self, event=None):
        self._apply_color(self.hover_color)

    def _on_hover_end(self, event=None):
        self._apply_color(self.normal_color)