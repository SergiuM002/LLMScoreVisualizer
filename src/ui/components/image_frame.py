import customtkinter as ctk
from PIL import Image

class ImageFrame(ctk.CTkFrame):
    def __init__(self, master, image_path, size, **kwargs):
        super().__init__(master, **kwargs)
        
        self.image = Image.open(image_path)
        
        self.ctk_image = ctk.CTkImage(
            light_image=self.image,
            dark_image=self.image,
            size=size
        )
        
        self.image_label = ctk.CTkLabel(self, text="", image=self.ctk_image)
        self.image_label.pack(expand=True)
        
    def _resize_image(self, event):
        if event.width <= 10 or event.height <= 10:
            return

        orig_w, orig_h = self.image.size
        aspect_ratio = orig_w / orig_h

        target_w, target_h = event.width, event.height

        if target_w / target_h > aspect_ratio:
            new_h = target_h
            new_w = int(new_h * aspect_ratio)
        else:
            new_w = target_w
            new_h = int(new_w / aspect_ratio)
            
        self.ctk_image.configure(size=(new_w, new_h))