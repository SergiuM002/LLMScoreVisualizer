from config.styles import Theme
from customtkinter import CTkLabel

class PlotSelectionController:
    def __init__(self, main_ctrl):
        self.main_ctrl = main_ctrl
        
        self.plot_buttons = []
        
    def _get_all_children(self, widget):
        descendants = []
        for child in widget.winfo_children():
            descendants.append(child)
            descendants.extend(self._get_all_children(child))
        return descendants
        
    def apply_bindings(self, view):
        for plot_button in view.plot_buttons:
            all_widgets = [plot_button] + self._get_all_children(plot_button)
            
            selection = None
            for widget in all_widgets:
                if isinstance(widget, CTkLabel) and widget.cget("text") != "":
                    selection = widget.cget("text")
                    break
                    
            for widget in all_widgets:
                widget.bind(
                    "<Enter>", 
                    lambda e, pb=plot_button: pb.configure(fg_color=Theme.GRAY_BUTTON_HOVER)
                )
                widget.bind(
                    "<Leave>", 
                    lambda e, pb=plot_button: pb.configure(fg_color=Theme.GRAY_BUTTON)
                )
                widget.bind(
                    "<ButtonRelease-1>", 
                    lambda e, sel=selection: self.main_ctrl.show_plot_creation_screen(sel)
                )