from pathlib import Path
import csv

class CSVImportMenuController:
    def __init__(self, main_ctrl):
        self.main_ctrl = main_ctrl
        
        self.view = None
        self.selected_csv = -1
        self.csv_files = []
        
        self.height_quo = 0
        
    def load_imported_files(self):
        for path in self.view.master.controller.file_list:
            self.add_csv(path)
        
    def set_window_size_and_pos(self):
        monitor = self.main_ctrl.get_current_monitor()
                
        window_width = round(300*self.main_ctrl.height_quo)
        window_height = round(400*self.main_ctrl.height_quo)  

        self.center_x = round(monitor.width/2) + monitor.x
        self.center_y = round(monitor.height/2) + monitor.y
        
        x = round(self.center_x - window_width/2)
        y = round(self.center_y - window_height/2)
        
        self.view.wm_geometry(f"{window_width}x{window_height}+{x}+{y}")
            
    def connect_view(self, view):
        self.view = view
        
    def add_csv(self, file_path):
        if file_path in self.csv_files:
            self.view.show_already_imported_error()
            return False   
        elif Path(file_path).suffix != ".csv":
            self.view.show_invalid_file_extension_error()
            return False
        elif not (result := self._valid_columns(file_path))[0]:
            self.view.show_invalid_columns_error(result[1])
            return False
        elif not self._msic_in_range(file_path):
            self.view.show_invalid_msic_error()  
            return False
        elif not self._valid_nucleotides(file_path):
            self.view.show_invalid_nucleotide_error()
            return False
        else:
            self.csv_files.append(file_path)
            self.view.pack_csv_button(Path(file_path).name, file_path, file_path)
            return True
            
    def toggle_csv(self, button):
        button_index = self.view.csv_buttons.index(button)
    
        if self.selected_csv != button_index:
            if self.selected_csv != -1:
                prev_button = self.view.csv_buttons[self.selected_csv]
                prev_button.set_selected(False)
                            
            self.selected_csv = button_index
            button.set_selected(True)
            self.view.csv_remove.configure(state="normal")
            
        else:
            self.selected_csv = -1
            button.set_selected(False)
            self.view.csv_remove.configure(state="disabled")
            
    def remove_csv(self):
        if self.selected_csv == -1:
            return
        self.csv_files.pop(self.selected_csv)
        self.view.csv_buttons[self.selected_csv].destroy()
        self.view.csv_buttons.pop(self.selected_csv)
        self.selected_csv = -1
        self.view.csv_remove.configure(state="disabled")
        
    def confirm_files(self):
        plot_controller = self.view.master.controller
        
        plot_controller.file_list = self.csv_files
        plot_controller.preview_plot()                    
        
    def _msic_in_range(self, file_path):
        with open(file_path, mode="r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                val = float(row["MSIC"])
                if not (-1 <= val <= 1):
                    return False
                
        return True
    
    def _valid_nucleotides(self, file_path):
        with open(file_path, mode="r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                val = str(row["ref"])
                if val.lower() not in ["a", "c", "g", "t"]:
                    return False
                        
        return True  
    
    def _valid_columns(self, file_path):
        with open(file_path, mode="r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            
            if "ref" not in reader.fieldnames:
                return (False, "ref")
            elif "MSIC" not in reader.fieldnames:
                return (False, "MSIC")
        
        return (True, "")
                    