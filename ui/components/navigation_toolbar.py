import customtkinter as ctk
from pathlib import Path
from customtkinter import filedialog
import config.environment as env
import subprocess
from config.styles import Theme
from ui.components.tooltip_button import TooltipButton

class NavigationToolbar(ctk.CTkFrame):   
    def __init__(self, controller, master, **kwargs):   
        super().__init__(master, fg_color="transparent", **kwargs)
        
        self.controller = controller
        self.master = master
        
        controller.connect_view(self)
        
        self.prev_view_button = TooltipButton(
            self,
            height=30,
            width=30,
            text="\uf0e2",
            font=("FontAwesome", 20),
            anchor="center",
            fg_color=Theme.GRAY_BUTTON,
            text_color=Theme.GRAY_BUTTON_TEXT,
            hover_color=Theme.GRAY_BUTTON_HOVER,
            command=controller.toolbar.back,
            tooltip_message="switch to previous view"
        )
        self.prev_view_button.pack(side=ctk.LEFT, padx=(10, 0), pady=5)
        
        self.next_view_button = TooltipButton(
            self,
            height=30,
            width=30,
            text="\uf01e",
            font=("FontAwesome", 20),
            anchor="center",
            fg_color=Theme.GRAY_BUTTON,
            text_color=Theme.GRAY_BUTTON_TEXT,
            hover_color=Theme.GRAY_BUTTON_HOVER,
            command=controller.toolbar.forward,
            tooltip_message="switch to next view"
        )
        self.next_view_button.pack(side=ctk.LEFT, padx=(10, 0), pady=5)
        
        self.reset_view_button = TooltipButton(
            self,
            height=30,
            width=30,
            text="\uf021",
            font=("FontAwesome", 20),
            anchor="center",
            fg_color=Theme.GRAY_BUTTON,
            text_color=Theme.GRAY_BUTTON_TEXT,
            hover_color=Theme.GRAY_BUTTON_HOVER,
            command=controller.reset_view,
            tooltip_message="reset view"
        )
        self.reset_view_button.pack(side=ctk.LEFT, padx=(10, 0), pady=5)
             
        self.pan_button = TooltipButton(
            self,
            height=30,
            width=30,
            text="\uf047",
            font=("FontAwesome", 20),
            anchor="center",
            fg_color=Theme.GRAY_BUTTON,
            text_color=Theme.GRAY_BUTTON_TEXT,
            hover_color=Theme.GRAY_BUTTON_HOVER,
            command=self.pan_clicked,
            tooltip_message="toggle pan mode"
        )
        self.pan_button.pack(side=ctk.LEFT, padx=(10, 0), pady=5)
        
        self.zoom_on_rectangle_button = TooltipButton(
            self,
            height=30,
            width=30,
            text="\uf002",
            font=("FontAwesome", 20),
            anchor="center",
            fg_color=Theme.GRAY_BUTTON,
            text_color=Theme.GRAY_BUTTON_TEXT,
            hover_color=Theme.GRAY_BUTTON_HOVER,
            command=self.zoom_clicked,
            tooltip_message="toggle zoom on rectangle mode"
        )
        self.zoom_on_rectangle_button.pack(side=ctk.LEFT, padx=(10, 0), pady=5)
        
        self.configure_subplots_button = TooltipButton(
            self,
            height=30,
            width=30,
            text="\uf013",
            font=("FontAwesome", 20),
            fg_color=Theme.GRAY_BUTTON,
            text_color=Theme.GRAY_BUTTON_TEXT,
            hover_color=Theme.GRAY_BUTTON_HOVER,
            command=controller.toolbar.configure_subplots,
            tooltip_message="configure the figure"
        )
        self.configure_subplots_button.pack(side=ctk.LEFT, padx=(10, 0), pady=5)
        
        self.reset_subplots_button = TooltipButton(
            self,
            height=30,
            width=30,
            text="\uf122",
            font=("FontAwesome", 20),
            fg_color=Theme.GRAY_BUTTON,
            text_color=Theme.GRAY_BUTTON_TEXT,
            hover_color=Theme.GRAY_BUTTON_HOVER,
            command=self.reset_config_clicked,
            tooltip_message="reset figure configuration"
        )
        self.reset_subplots_button.pack(side=ctk.LEFT, padx=(10, 0), pady=5)
        
        self.save_button = TooltipButton(
            self,
            height=30,
            width=30,
            text="\uf0c7",
            font=("FontAwesome", 20),
            fg_color=Theme.GRAY_BUTTON,
            text_color=Theme.GRAY_BUTTON_TEXT,
            hover_color=Theme.GRAY_BUTTON_HOVER,
            command=self.save_clicked,
            tooltip_message="export this plot"
        )
        self.save_button.pack(side=ctk.LEFT, padx=(10, 0), pady=5)
        
        self.prev_plot_button = ctk.CTkButton(
            self,
            height=30,
            text="Previous Plot",
            font=("Roboto", 15),
            fg_color=Theme.GRAY_BUTTON,
            text_color=Theme.GRAY_BUTTON_TEXT,
            hover_color=Theme.GRAY_BUTTON_HOVER,
            command=self.prev_plot_clicked,
        )
        self.prev_plot_button.pack(side=ctk.LEFT, padx=(10, 0), pady=5)
        
        self.next_plot_button = ctk.CTkButton(
            self,
            height=30,
            text="Next Plot",
            font=("Roboto", 15),
            fg_color=Theme.GRAY_BUTTON,
            text_color=Theme.GRAY_BUTTON_TEXT,
            hover_color=Theme.GRAY_BUTTON_HOVER,
            command=self.next_plot_clicked,
        )
        self.next_plot_button.pack(side=ctk.LEFT, padx=(10, 0), pady=5)
        
        self.set_plot_control_buttons()
        
    def set_plot_control_buttons(self):
        plot_controller = self.master.controller
        
        if len(plot_controller.file_list) == 1:
            self.prev_plot_button.configure(state="disabled")
            self.next_plot_button.configure(state="disabled")
        elif plot_controller.csv_index == 0:
            self.prev_plot_button.configure(state="disabled")
            self.next_plot_button.configure(state="normal")
        elif plot_controller.csv_index == len(plot_controller.file_list)-1:
            self.prev_plot_button.configure(state="normal")
            self.next_plot_button.configure(state="disabled")
        else:
            self.prev_plot_button.configure(state="normal")
            self.next_plot_button.configure(state="normal")   
        
    def pan_clicked(self):
        self.controller.pan_toggle()
        
    def zoom_clicked(self):
        self.controller.zoom_toggle()
        
    def prev_plot_clicked(self):
        self.controller.show_prev_plot()
        
    def next_plot_clicked(self):
        self.controller.show_next_plot()
        
    def save_clicked(self):
        if env.OPERATING_SYSTEM == "Linux":
            try:
                output_path = subprocess.check_output(
                    [
                        "zenity",
                    "--file-selection",
                    "--save",
                    "--title=Save Your Plot",
                    "--confirm-overwrite",
                    "--file-filter=PDF Files (*.pdf) |*.pdf",
                    "--file-filter=PNG Files (*.png) |*.png",
                    "--file-filter=JPEG Files (*.jpg; *.jpeg) |*.jpg *.jpeg",
                    "--file-filter=All Files |*",
                    ],
                    stderr=subprocess.DEVNULL
                ).decode('utf-8').strip()
            except subprocess.CalledProcessError:
                return
        else:
            output_path = filedialog.asksaveasfilename(
                title="Save Your Plot",
                defaultextension=".pdf",
                filetypes=[
                    ("PDF Files", "*.pdf"),
                    ("PNG Files", "*.png"),
                    ("JPEG Files", "*.jpg *.jpeg"),                 
                    ("All Files", "*.*")
                ]
        ) 
        self.controller.save_plot(output_path)
        
    def reset_config_clicked(self):
        self.controller.reset_config()

    def set_color_activated(self, widget, activated: bool):
        if activated:
            widget.configure(
                fg_color=Theme.GREEN_BUTTON,
                text_color=Theme.GREEN_BUTTON_TEXT,
                hover_color=Theme.GREEN_BUTTON_HOVER,  
            )
        else:
            widget.configure(
                fg_color=Theme.GRAY_BUTTON,
                text_color=Theme.GRAY_BUTTON_TEXT,
                hover_color=Theme.GRAY_BUTTON_HOVER,  
            )