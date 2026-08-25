import platform
import os
import json
import customtkinter as ctk
from tkinter import font as tkfont
from screeninfo import get_monitors
from ui.views.plot_selection import PlotSelection
from controllers.views.plot_selection_controller import PlotSelectionController 
from controllers.views.msic_profile_controller import MSICProfileController
from ui.views.msic_profile import MSICProfile
import config.environment as env
from config.fonts import Fonts

class MainController:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.withdraw()
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.title("LLMPipeLine")
        self.root.resizable(False, False)
        self.root.rowconfigure(0, weight=1)
        self.root.columnconfigure(0, weight=1)
        ctk.set_widget_scaling(1.0)
        ctk.set_window_scaling(1.0)
        
        self.current_monitor = get_monitors()[0]

        for m in get_monitors():
            if m.is_primary:
                self.current_monitor = m
                
        self.height_quo = self.current_monitor.height/1200
        self.fonts = Fonts(self.height_quo)

        self.original_window_height = 800
        self.original_window_width = 800
        
        self.current_window_height = self.original_window_height
        self.current_window_width = self.original_window_width

        self.root.wm_geometry("")

        self.root.geometry(f"{round(self.original_window_width*self.height_quo)}x{round(self.original_window_height*self.height_quo)}")

        self.views = {}
        
        self.plot_creation_view = None
        self.plot_creation_ctrl = None
        
        self.root.after(200, self.resize_window, self.root, self.current_monitor)
        
        self.plot_selection_ctrl = PlotSelectionController(self)
        self.plot_selection_view = PlotSelection(self.plot_selection_ctrl, self.root)

        self.plot_selection_view.grid(row=0, column=0, sticky=ctk.NSEW)
        
        self.show_plot_selection_screen()
        self.root.update_idletasks()
        self.root.deiconify()
        self.root.update()
        
        self.root.mainloop()
        
    def get_current_monitor(self):
        """Returns the monitor the app is on."""
        self.root.update_idletasks()
        parts = self.root.wm_geometry().split("+")
        win_x, win_y = int(parts[1]), int(parts[2])
        
        for monitor in get_monitors():
            if (monitor.x <= win_x < monitor.x + monitor.width and
                monitor.y <= win_y < monitor.y + monitor.height):
                
                return monitor

        return None
    
    def apply_window_size(self):
        self.root.geometry(f"{round(self.current_window_width*self.height_quo)}x{round(self.current_window_height*self.height_quo)}")
        ctk.set_widget_scaling(self.height_quo)
        self.root.update()   
        
    def resize_window(self, window, current_monitor):
        """Resize window based on monitor resolution."""
        last_monitor = current_monitor
        
        new_monitor = self.get_current_monitor()
        
        if new_monitor is not None:
            current_monitor = new_monitor
                
        if (current_monitor != last_monitor):
            self.height_quo = current_monitor.height / 1200
            
            self.apply_window_size()
            self.fonts.resize_text(self.height_quo)
            
            if self.plot_creation_view is not None and self.plot_creation_ctrl.fig is not None:
                self.plot_creation_view.controller.preview_plot()
        
        self.root.after(100, self.resize_window, window, current_monitor)     
        
    def show_plot_selection_screen(self):
        """Changes view to plot selection screen."""
        self.root.withdraw()
        
        if self.plot_creation_view is not None:
            self.plot_creation_view.pack_forget()
            self.plot_creation_view.destroy()
            self.plot_creation_view = None
            self.plot_creation_ctrl = None
        
        
        self.current_window_width = self.original_window_width
        self.current_window_height = self.original_window_height
        
        self.apply_window_size()

        self.plot_selection_view.tkraise()
        self.root.deiconify()
        
    def show_plot_creation_screen(self, selection):
        """Changes view to plot creation screen."""
        self.root.withdraw()
        
        if env.OPERATING_SYSTEM == "Linux":
            self.root.unbind_all("<Button-4>")   
            self.root.unbind_all("<Button-5>")
            
        match selection:
            case "MSIC-Profile":
                self.plot_creation_ctrl = MSICProfileController(self)
                self.plot_creation_view = MSICProfile(self.plot_creation_ctrl, self.root)
            case _:
                self.plot_creation_ctrl = MSICProfileController(self)
                self.plot_creation_view = MSICProfile(self.plot_creation_ctrl, self.root)
                
        self.plot_creation_view.grid(row=0, column=0, sticky=ctk.NSEW)
        
        self.root.deiconify()
        
    def on_closing(self):
        """Cleanup on closing the program."""
        self.root.destroy()
        
        try:
            self.root.withdraw()
        except Exception:
            pass
                
        for after_id in self.root.tk.eval('after info').split():
            try:
                self.root.after_cancel(after_id)
            except Exception:
                pass
                
        try:
            self.root.quit()
        except Exception:
            pass 
        
        try:
            self.root.destroy()  
        except Exception:
            pass