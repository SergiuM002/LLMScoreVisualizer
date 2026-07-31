import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
from matplotlib.lines import Line2D
from matplotlib.widgets import Cursor
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from Bio import SeqIO
from Bio.SeqFeature import CompoundLocation
import customtkinter as ctk
import tkinter as tk
from ui.views.plot_creation import PlotCreation
from ui.views.genbank_selection import GenbankSelection
from controllers.views.genbank_selection_controller import GenbankSelectionController
from ui.components.navigation_toolbar import NavigationToolbar
from controllers.components.navigation_toolbar_controller import NavigationToolbarController
from config.styles import Theme

class MSICProfile(PlotCreation):   
    def __init__(self, controller, master, **kwargs):   
        super().__init__(controller, master, **kwargs)
        
        self.controller = controller
        self.custom_toolbar = None
        
        controller.connect_view(self)
        
        self.rolling_frame = ctk.CTkFrame(self.button_frame1, fg_color="transparent")
        self.rolling_frame.pack(side=ctk.RIGHT, fill="y", padx=(0, 5), pady=5)
        
        self.rolling_label = ctk.CTkLabel(
            self.rolling_frame,
            font=("Roboto", 16),
            text_color=("gray20", "white"),
            text="Rolling Mean"
        )
        self.rolling_label.pack(pady=(0, 20))
        
        self.rolling_entry_frame = ctk.CTkFrame(self.rolling_frame, fg_color="transparent")
        self.rolling_entry_frame.pack(fill="x", pady=(0, 10))
        
        vcmd_rolling_entries = (self.register(self.controller.validate_positive_int), '%P')
        
        self.rolling_step_label = ctk.CTkLabel(
            self.rolling_entry_frame,
            font=("Roboto", 12),
            text_color=("gray20", "white"),
            text="Step"
        )
        self.rolling_step_label.pack(side=ctk.LEFT)
        
        self.step_var = ctk.StringVar(value="1")
        self.rolling_step_entry = ctk.CTkEntry(
            self.rolling_entry_frame,
            textvariable=self.step_var,
            width=60,
            height=25,
            validate="key",
            validatecommand=vcmd_rolling_entries
        )
        self.rolling_step_entry.pack(side=ctk.LEFT, padx=(5, 0))
        
        self.rolling_window_label = ctk.CTkLabel(
            self.rolling_entry_frame,
            font=("Roboto", 12),
            text_color=("gray20", "white"),
            text="Window"
        )
        
        self.window_var = ctk.StringVar(value="20")
        self.rolling_window_entry = ctk.CTkEntry(
            self.rolling_entry_frame,
            textvariable=self.window_var,
            width=60,
            height=25,
            validate="key",
            validatecommand=vcmd_rolling_entries
        )
        self.rolling_window_entry.pack(side=ctk.RIGHT, padx=(5, 0))
        self.rolling_window_label.pack(side=ctk.RIGHT)
        
        self.rolling_slider_frame = ctk.CTkFrame(self.rolling_frame, fg_color="transparent")
        self.rolling_slider_frame.pack()
    
        self.rolling_width_label = ctk.CTkLabel(
            self.rolling_slider_frame,
            text="Line width",
            font=("Roboto", 12),
            text_color=("gray20", "white")
        )
        self.rolling_width_label.pack(side=ctk.LEFT)
        
        self.rolling_slider = ctk.CTkSlider(
            self.rolling_slider_frame,
            width=120,
            height=15,
            button_color=Theme.GREEN_BUTTON,
            button_hover_color=Theme.GREEN_BUTTON_HOVER,
            command=self.update_entry_from_slider
        )
        self.rolling_slider.pack(side=ctk.LEFT, padx=(0, 3))
        
        vcmd_rolling_slider = (self.register(self.controller.validate_width), '%P')
        
        self.width_var = ctk.StringVar(value="1.0")
        self.width_var.trace_add("write", self.update_slider_from_entry)
        self.rolling_entry = ctk.CTkEntry(
            self.rolling_slider_frame, 
            width=40,
            textvariable=self.width_var,
            validate="key",
            validatecommand=vcmd_rolling_slider
        )
        self.rolling_entry.pack(side=ctk.LEFT)
        
        self.region_frame1 = ctk.CTkFrame(self.button_frame1, fg_color="transparent")
        self.region_frame1.pack(side=ctk.RIGHT, fill="y", padx=(0, 25), pady=5)
        
        self.genbank_label = ctk.CTkLabel(
            self.region_frame1,
            text="Annotation",
            font=("Roboto", 16),
            text_color=Theme.GENERAL_LABEL
        )
        self.genbank_label.pack(pady=(0, 20))
        
        self.genbank_upload_text = ctk.StringVar(self.region_frame1, "not imported ✕")
        self.genbank_upload_label = ctk.CTkLabel(
            self.region_frame1,
            textvariable=self.genbank_upload_text,
            font=("Roboto", 12),
            text_color=Theme.GENERAL_LABEL
        )
        self.genbank_upload_label.pack(pady=(0, 5))
        
        self.region_frame2 = ctk.CTkFrame(self.region_frame1, fg_color="transparent")
        self.region_frame2.pack()
        self.region_frame2.grid_columnconfigure(0, weight=1)
        self.region_frame2.grid_columnconfigure(1, weight=1)
        
        self.genbank_button = ctk.CTkButton(
            self.region_frame2,
            text="Import genbank",
            command=self.import_genbank_clicked,
            height=30,
            font=("Roboto", 15),
            text_color=Theme.GREEN_BUTTON_TEXT,
            fg_color=Theme.GREEN_BUTTON,
            hover_color=Theme.GREEN_BUTTON_HOVER,
        )
        self.genbank_button.grid(row=0, column=0, padx=5)
        
        self.reverse_ann = ctk.BooleanVar(value=False)
        self.reverse_ann_checkbox = ctk.CTkCheckBox(
            self.region_frame2,
            text="reverse annotation",
            font=("Roboto", 14),
            checkbox_height=18,
            checkbox_width=18,
            fg_color=Theme.GREEN_BUTTON,
            hover_color=Theme.GREEN_BUTTON_HOVER,
            variable=self.reverse_ann,
            border_color=("gray45", "gray55"),
            text_color=Theme.GENERAL_LABEL
        )
        self.reverse_ann_checkbox.grid(row=0, column=1, padx=5)
 
    def import_genbank_clicked(self):
        self.genbank_button.configure(state="disabled")
        GenbankSelection(GenbankSelectionController(self.controller.main_ctrl), self)
        
    def update_slider_from_entry(self, *args):
        try:
            raw_val = self.width_var.get()
            if raw_val in ["", ".", "-"]: 
                return 
            
            val = float(raw_val)
            
            self.rolling_slider.set(val / 2)
        except ValueError:
            pass

    def update_entry_from_slider(self, slider_val):
        entry_val = slider_val * 2
        
        self.width_var.set(f"{entry_val:.2f}")
        
    def show_interactive_view(self, fig):
        if self.custom_toolbar != None:
            self.custom_toolbar.pack_forget()
            self.custom_toolbar.destroy()
            self.base_bar.pack_forget()
            self.base_bar.destroy()
            self.tooltip.pack_forget()
            self.tooltip.destroy()
                
        self.canvas = FigureCanvasTkAgg(fig, master=self.plot_frame)
            
        self.canvas.draw()
        self.plot_widget = self.canvas.get_tk_widget()
        self.plot_widget.pack(expand=True, padx=20, pady=(10, 0))
        
        self.toolbar = NavigationToolbar2Tk(self.canvas, self.plot_frame)
        self.toolbar.pack_forget()
            
        self.custom_toolbar = NavigationToolbar(NavigationToolbarController(self.controller.main_ctrl, self.toolbar), self)
        self.custom_toolbar.pack(fill="x")
        
        self.cursor = Cursor(self.controller.ax, useblit=True, color='blue', linewidth=1)
        self.tooltip = ctk.CTkLabel(self, text="", padx=3, pady=3)
        
        if ctk.get_appearance_mode() == "Dark":
            text_bg ="#2b2b2b"
            text_fg="#DDDDDD"
        else:
            text_bg ="#DDDDDD"
            text_fg="#2b2b2b"     
        
        self.base_bar = tk.Text(
            self.plot_frame, 
            height=1, 
            borderwidth=0, 
            highlightthickness=0, 
            bg=text_bg, 
            fg=text_fg,
            font=self.controller.main_ctrl.fonts.roboto_fonts[22]
        )
        self.base_bar.tag_configure("center_align", justify='center')
        self.base_bar.tag_configure("highlight", foreground="red")
        self.base_bar.configure(state="disabled")
        self.base_bar.pack(pady=(0, 5))
            
    def apply_zoom(self, ax, middle_x, middle_y, new_width, new_height):
        ax.set_xlim([middle_x - new_width/2, middle_x + new_width/2])
        ax.set_ylim([middle_y - new_height/2, middle_y + new_height/2])
        ax.figure.canvas.draw_idle()
            
    def show_tooltip(self, xdata, msic_score, x, y):
        self.tooltip.lift()
        self.tooltip.configure(text=f"Pos: {xdata:.0f}, MSIC= {msic_score}")
        self.tooltip.place(x=x, y=y) 
            
    def update_base_bar(self, base_string, pos):
        self.base_bar.configure(state="normal")
        self.base_bar.delete("1.0", "end")

        if pos >= 0 and pos < len(base_string):
            self.base_bar.insert("1.0", base_string[max(0, pos-20) : pos+20].upper())
            self.base_bar.tag_add("center_align", "1.0", "end")
            pos_dist = pos - max(0, pos-20)
            self.base_bar.tag_add("highlight", f"1.{pos_dist}", f"1.{pos_dist + 1}")
            
        self.base_bar.configure(state="disabled")
        
        

        