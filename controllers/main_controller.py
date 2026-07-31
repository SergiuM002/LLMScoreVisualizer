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

        self.original_window_height = 545
        self.original_window_width = 545
        
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
        
    # Resize window based on monitor resolution
    def resize_window(self, window, current_monitor):
        last_monitor = current_monitor
        
        new_monitor = self.get_current_monitor()
        
        if new_monitor is not None:
            current_monitor = new_monitor
                
        if (current_monitor != last_monitor):
            self.height_quo = current_monitor.height / 1200
            
            self.apply_window_size()
            self.fonts.resize_text(self.height_quo)
            
            if self.plot_creation_view and self.plot_creation_ctrl.fig is not None:
                self.plot_creation_view.controller.preview_plot()
        
        self.root.after(100, self.resize_window, window, current_monitor)

    def resize_widgets(self, parent, size_quo):
        for child in parent.winfo_children():
            self.resize_dimensions(child, size_quo)    
            self.resize_gaps(child, size_quo)
                
            if child.winfo_children():
                self.resize_widgets(child, size_quo)

    def resize_text(self, parent, size_quo):
        for child in parent.winfo_children():
            try:
                if "font" in child.keys():
                
                    raw_font = child.cget("font")
                    
                    if raw_font:
                        font_obj = tkfont.Font(font=raw_font)
                        
                        font_name = font_obj.actual("family")
                        current_size = font_obj.actual("size")  
                        
                        child.configure(font=(font_name, round(current_size*size_quo)))
            except:
                pass
                
            if child.winfo_children():
                self.resize_text(child, size_quo)
                
    def resize_dimensions(self, widget, size_quo):
        try:
            if "height" in widget.keys():
                if not hasattr(widget, "original_height"):
                    height = widget.cget("height")
                    
                    if height is not None:
                        widget.original_height = round(float(height))
                    else:
                        widget.original_height = widget.winfo_height()
                
                new_height = round(widget.original_height * size_quo)
                if new_height > 1:
                    widget.configure(height=new_height)
        except:
            pass
    
        try:
            if "width" in widget.keys():
                if not hasattr(widget, "original_width"):
                    width = widget.cget("width")
                    
                    if width is not None:
                        widget.original_width = round(float(width))
                    else:
                        widget.original_width = widget.winfo_width()
        
                new_width = round(widget.original_width * size_quo)
                if new_width > 1:
                    widget.configure(width=new_width)
        except Exception as e:
            print(e)  
            
    def resize_gaps(self, widget, size_quo):
        try:
            if not hasattr(widget, "original_pack_info"):
                info = widget.pack_info()
                
                widget.original_pack_info = {
                    "side": info.get("side", ctk.TOP), 
                    "anchor": info.get("anchor", ctk.CENTER),
                    "fill": info.get("fill", ""),
                    "padx": info.get("padx", 0),
                    "pady": info.get("pady", 0) 
                }
            
            if hasattr(widget.original_pack_info["padx"], "__iter__"):
                padx = widget.original_pack_info["padx"]
                padx = tuple([size_quo*x for x in padx])
            else:
                padx = widget.original_pack_info["padx"]  * size_quo
            if hasattr(widget.original_pack_info["pady"], "__iter__"):
                pady = widget.original_pack_info["pady"]
                pady = tuple([size_quo*x for x in pady])
            else:
                pady = widget.original_pack_info["pady"] * size_quo  
            
            widget.pack(
                side=widget.original_pack_info["side"], 
                anchor=widget.original_pack_info["anchor"], 
                fill=widget.original_pack_info["fill"], 
                padx=padx, 
                pady=pady
            )
        except:
            pass 
        
        if widget.winfo_children():
                self.resize_text(widget, size_quo)
          
    # Forces each widget to repaint itself (solves visual bugs)
    def force_coordinate_update(self, widget):
        for child in widget.winfo_children():
            if hasattr(child, "_draw"):
                child._draw()

            child.update() 
            
            if child.winfo_children():
                self.force_coordinate_update(child)   
             
    # Scroll logic
    def window_scroll(self, event, frame, dist):
        current_pos = frame._parent_canvas.yview()[0]
        step = 0.02
        
        if dist > 0:
            new_pos = current_pos + step
        else:
            new_pos = current_pos - step
        
        frame._parent_canvas.yview_moveto(max(new_pos, 0))
        return "break"      
        
    def show_plot_selection_screen(self):
        self.root.withdraw()
        
        if self.plot_creation_view is not None:
            self.plot_creation_view.pack_forget()
            self.plot_creation_view.destroy()
            self.plot_creation_ctrl = None
        
        if env.OPERATING_SYSTEM == "Linux":
            self.root.unbind_all("<Button-4>")   
            self.root.unbind_all("<Button-5>")
            self.root.bind_all("<Button-4>", lambda e:  self.window_scroll(e, self.plot_selection_view.scroll_frame, -1))          
            self.root.bind_all("<Button-5>", lambda e:  self.window_scroll(e, self.plot_selection_view.scroll_frame, 1))     
        
        self.current_window_width = self.original_window_width
        self.current_window_height = self.original_window_height
        
        self.apply_window_size()

        self.plot_selection_view.tkraise()
        self.root.deiconify()
        
    def show_plot_creation_screen(self, selection):
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