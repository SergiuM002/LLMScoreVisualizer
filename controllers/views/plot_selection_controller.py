from config.styles import Theme
from customtkinter import CTkLabel

class PlotSelectionController:
    def __init__(self, main_ctrl):
        self.main_ctrl = main_ctrl
        
        self.plot_buttons = []
        
    def apply_bindings(self, view):
        for plot_button in view.plot_buttons:
            selection = None
            for label in plot_button.winfo_children():
                if isinstance(label, CTkLabel):
                    selection = label.cget("text")
                    
            plot_button.bind("<Enter>", lambda e, pb=plot_button: pb.configure(fg_color=Theme.GRAY_BUTTON_HOVER))
            plot_button.bind("<Leave>", lambda e, pb=plot_button: pb.configure(fg_color=Theme.GRAY_BUTTON))    
            plot_button.bind("<ButtonRelease-1>", lambda e, sel=selection: self.main_ctrl.show_plot_creation_screen(sel))
            
            for widget in plot_button.winfo_children():
                widget.bind("<Enter>", lambda e, pb=plot_button: pb.configure(fg_color=Theme.GRAY_BUTTON_HOVER))
                widget.bind("<Leave>", lambda e, pb=plot_button: pb.configure(fg_color=Theme.GRAY_BUTTON))   
                widget.bind("<ButtonRelease-1>", lambda e, sel=selection: self.main_ctrl.show_plot_creation_screen(sel))
                