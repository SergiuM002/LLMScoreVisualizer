import pandas as pd
import config.environment as env
from pathlib import Path
from abc import ABC, abstractmethod


class PlotCreationController(ABC):
    def __init__(self, main_ctrl):
        self.main_ctrl = main_ctrl
        
        self.file_list = []
        
        self.ax = None
        self.fig = None
        self.canvas = None
        self.csv_index = 0
        
    def set_window_size(self):
        monitor = self.main_ctrl.get_current_monitor()

        # Deals with scaling bs between operating systems
        if env.OPERATING_SYSTEM == "Windows":
            factor = 1
        else:
            factor = self.main_ctrl.height_quo
        
        window_width = round(1400*factor)
        window_height = round(850*factor)  

        self.center_x = round(monitor.width/2) + monitor.x
        self.center_y = round(monitor.height/2) + monitor.y
        
        x = round(self.center_x - window_width/2)
        y = round(self.center_y - window_height/2)
        
        self.main_ctrl.current_window_width = 1400
        self.main_ctrl.current_window_height = 850
        
        self.main_ctrl.root.wm_geometry(f"+{x}+{y}")
        self.main_ctrl.apply_window_size()
        
    def save_all_plots(self, view, output_path):       
        """Saves plots of all imported CSVs.""" 
        if not output_path:
            return
        
        for csv_path in self.file_list:
            with open(csv_path, "r") as csv_file:
                df = pd.read_csv(csv_file)
            
            genbank_file = None
                        
            for key in self.genbank_links.keys():
                if csv_path in self.genbank_links[key]:
                    genbank_file = key
                    break
             
            figure, _ = self.get_plot(df=df, csv_path=csv_path, genbank_file=genbank_file)
                
            file_name =  Path(csv_path).stem
            
            try:
                figure.savefig(f"{output_path}/{file_name}_MSICProfile{view.extension_selection.get()}", dpi=200)
            except Exception as e:
                self.view.show_plot_not_saved_error(e)
                
            
    def resize_plot(self):
        """Resizes plot based on monitor resolution."""
        if self.fig :
            self.fig.set_dpi(100 * self.main_ctrl.height_quo)
            
        if self.canvas:
            self.canvas.draw_idle()
            
        self.main_ctrl.root.after(100, self.resize_plot)
        
    @abstractmethod
    def get_plot(self, csv_file, genbank_file=None):
        pass
    
    @abstractmethod
    def preview_plot(self, csv_path=None):
        pass
    