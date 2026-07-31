import subprocess
from pathlib import Path
from config.styles import Theme
from ui.components.info_icon import InfoIcon
import config.environment as env

class GenbankSelectionController:
    def __init__(self, main_ctrl):
        self.main_ctrl = main_ctrl
        self.view = None
        
        self.genbank_files = []
        self.selected_genbank = -1
        self.selected_csv = {}
        
    def connect_view(self, view):
        self.view = view
        
    def load_imported_genbanks(self):
        for key in self.view.master.controller.genbank_links.keys():
            self.add_genbank(key)
        
    def load_csvs(self):
        csv_files = self.view.master.controller.file_list
        for file_path in csv_files:
            self.view.pack_csv_button(Path(file_path).name, file_path, file_path)   
        
    # Adds GenBank to list
    def add_genbank(self, file_path):
        if file_path not in self.genbank_files:
            self.selected_csv[file_path] = []
            self.genbank_files.append(file_path)
            self.view.pack_genbank_button(Path(file_path).name, file_path, file_path)
        else:
            self.view.show_already_imported_error()
        
    # Removes GenBank from list
    def remove_genbank(self):
        if self.selected_genbank == -1:
            return
        selected = self.selected_csv[self.genbank_files[self.selected_genbank]]
        for button in self.view.csv_buttons:
            if button.file_path in selected:
                button.set_selected(False)
        self.csvs_set_disabled_all()
            
        self.selected_csv.pop(self.genbank_files[self.selected_genbank])
        self.genbank_files.pop(self.selected_genbank)
        self.view.genbank_buttons[self.selected_genbank].destroy()
        self.view.genbank_buttons.pop(self.selected_genbank)
        self.selected_genbank = -1
        self.view.genbank_remove.configure(state="disabled")
        
    def csvs_set_disabled_all(self):
        for button in self.view.csv_buttons:
            button.set_enabled(False)
                
    def update_csvs_enabled(self, genbank_file_path):
        selected = self.selected_csv[genbank_file_path]
        for button in self.view.csv_buttons:
            if button.file_path in selected or not button.selected:
                button.set_enabled(True)
            else:
                button.set_enabled(False)
                       
    def toggle_genbank(self, button):
        button_index = self.view.genbank_buttons.index(button)
    
        if self.selected_genbank != button_index:
            if self.selected_genbank != -1:
                prev_button = self.view.genbank_buttons[self.selected_genbank]
                prev_button.set_selected(False)
                      
            self.selected_genbank = button_index
            button.set_selected(True)
            self.view.genbank_remove.configure(state="normal")
            self.update_csvs_enabled(button.file_path)
            
        else:        
            self.selected_genbank = -1
            button.set_selected(False)
            self.view.genbank_remove.configure(state="disabled")  
            self.csvs_set_disabled_all() 
        
    def toggle_csv(self, button):
        if self.selected_genbank != -1:
            if not button.selected:                            
                self.selected_csv[self.genbank_files[self.selected_genbank]].append(button.file_path)
                button.set_selected(True)
            else:
                self.selected_csv[self.genbank_files[self.selected_genbank]].remove(button.file_path)
                button.set_selected(False)
            
    def pass_genbank_binds(self):
        plot_controller = self.view.master.controller
        
        plot_controller.genbank_links = self.selected_csv
        plot_controller.genbank_uploaded = True
        plot_controller.preview_plot()
    
                    