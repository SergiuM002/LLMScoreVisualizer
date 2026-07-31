import config.environment as env

class CollapsibleMultiselectController:
    def __init__(self, main_ctrl, options, options_info=None):
        self.main_ctrl = main_ctrl
        
        self.options = options
        self.options_info = options_info
        
        self.is_open = False
        self.view = None
        
    def connect_view(self, view):
        self.view = view
        
    def pack_options(self):
        try:
            if (len(self.options) == len(self.options_info)):
                has_infoboxes = True
            else:
                has_infoboxes = False
        except (TypeError):
            has_infoboxes = False
            
        for i in range(len(self.options)):
            if has_infoboxes:
                self.view.pack_option(has_infoboxes, self.options[i], self.options_info[i])
            else:
                self.view.pack_option(has_infoboxes, self.options[i], None)
            
        self.apply_universal_bindings()
        self.main_ctrl.force_coordinate_update(self.view.winfo_toplevel())
            
    def toggle(self):
        if self.is_open:
            self.view.collapse_list()
        else:
            self.view.expand_list()
        self.is_open = not self.is_open
        
    def get_canvas(self):
        for attr in ['canvas', '_canvas', '_parent_canvas']:
            if hasattr(self.view.content_frame, attr):
                return getattr(self.view.content_frame, attr)
        return None

    # Apply scroll binding to the widget and every child widget
    def apply_universal_bindings(self,):
        canvas = self.get_canvas()
        if not canvas: 
            return
        
        widgets = [self.view.content_frame, canvas]
        scrollbar = getattr(self.view.content_frame, "_scrollbar", None)
        if scrollbar:
            widgets.append(scrollbar)
        
        for option in self.view.option_frames:
            widgets.append(option)
            widgets.extend(option.winfo_children())
        for cb in self.view.checkboxes:
            widgets.append(cb)
            widgets.extend(cb.winfo_children())
        for w in widgets:
            if env.OPERATING_SYSTEM == "Linux":
                w.bind("<Button-4>", lambda e: self.view.scroll(-1))
                w.bind("<Button-5>", lambda e: self.view.scroll(1))
            else:
                w.bind("<MouseWheel>", self.view.scroll)
                
    def load_new_options(self, options, options_info=None):
        self.options = options
        self.options_info = options_info
        
        self.view.clean_old_options()
        
        self.pack_options()
        
        
            

            

            


            
        