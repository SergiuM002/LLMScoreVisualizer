from pathlib import Path

class NavigationToolbarController:   
    def __init__(self, main_ctrl, toolbar, **kwargs):   
        self.toolbar = toolbar
        self.pan_active = False
        self.zoom_active = False
        
    def connect_view(self, view):
        self.view = view
        
    def show_prev_plot(self):
        plot_controller = self.view.master.controller
        
        if plot_controller.csv_index == 0:
            return
        else:
            plot_controller.csv_index -= 1
            
            plot_controller.preview_plot(plot_controller.file_list[plot_controller.csv_index])
        
    def show_next_plot(self):
        plot_controller = self.view.master.controller
                
        if plot_controller.csv_index == len(plot_controller.file_list)-1:
            return
        else:
            plot_controller.csv_index += 1
            
            plot_controller.preview_plot(plot_controller.file_list[plot_controller.csv_index])
                
    def pan_toggle(self):
        self.toolbar.pan()
        
        if self.pan_active:
            self.pan_active = False
            
            self.view.set_color_activated(self.view.pan_button, False)
        else:
            self.pan_active = True
            self.zoom_active = False
        
            self.view.set_color_activated(self.view.pan_button, True)
            self.view.set_color_activated(self.view.zoom_on_rectangle_button, False)
            
    def zoom_toggle(self):
        self.toolbar.zoom()
        
        if self.zoom_active:
            self.zoom_active = False
            
            self.view.set_color_activated(self.view.zoom_on_rectangle_button, False)
        else:
            self.zoom_active = True
            self.pan_active = False
        
            self.view.set_color_activated(self.view.zoom_on_rectangle_button, True)
            self.view.set_color_activated(self.view.pan_button, False)
            
    def save_plot(self, output_path):
        file_extension = Path(output_path).suffix.lower()
        if not file_extension:
            output_path = f"{output_path}.pdf"
        
        figure = self.view.master.controller.fig
        figure.savefig(output_path, dpi=200)
        

