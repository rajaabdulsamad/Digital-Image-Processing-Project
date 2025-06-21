import tkinter as tk
from tkinter import filedialog, messagebox
import cv2
import numpy as np
from PIL import Image, ImageTk
import matplotlib.pyplot as plt

class ImageProcessorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Digital Image Processing Project")
        self.root.geometry("800x600")
        
        self.image = None
        self.processed_image = None
        self.image_label = tk.Label(root)
        self.image_label.pack(pady=10)
        
        btn_frame = tk.Frame(root)
        btn_frame.pack(pady=10)
        
        tk.Button(btn_frame, text="Load Image", command=self.load_image).grid(row=0, column=0, padx=5)
        tk.Button(btn_frame, text="Grayscale", command=self.apply_grayscale).grid(row=0, column=1, padx=5)
        tk.Button(btn_frame, text="Edge Detection", command=self.apply_edge_detection).grid(row=0, column=2, padx=5)
        tk.Button(btn_frame, text="Blur", command=self.apply_blur).grid(row=0, column=3, padx=5)
        tk.Button(btn_frame, text="Histogram Equalization", command=self.apply_histogram_eq).grid(row=0, column=4, padx=5)
        tk.Button(btn_frame, text="Save Image", command=self.save_image).grid(row=0, column=5, padx=5)
        
    def load_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.png *.jpeg")])
        if file_path:
            self.image = cv2.imread(file_path)
            self.processed_image = self.image.copy()
            self.display_image(self.processed_image)
    
    def display_image(self, img):
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img_pil = Image.fromarray(img_rgb)
        img_pil = img_pil.resize((400, 400), Image.Resampling.LANCZOS)
        img_tk = ImageTk.PhotoImage(img_pil)
        self.image_label.configure(image=img_tk)
        self.image_label.image = img_tk
    
    def apply_grayscale(self):
        if self.image is None:
            messagebox.showerror("Error", "No image loaded!")
            return
        self.processed_image = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        self.processed_image = cv2.cvtColor(self.processed_image, cv2.COLOR_GRAY2BGR)
        self.display_image(self.processed_image)
    
    def apply_edge_detection(self):
        if self.image is None:
            messagebox.showerror("Error", "No image loaded!")
            return
        gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        self.processed_image = cv2.Canny(gray, 100, 200)
        self.processed_image = cv2.cvtColor(self.processed_image, cv2.COLOR_GRAY2BGR)
        self.display_image(self.processed_image)
    
    def apply_blur(self):
        if self.image is None:
            messagebox.showerror("Error", "No image loaded!")
            return
        self.processed_image = cv2.GaussianBlur(self.image, (5, 5), 0)
        self.display_image(self.processed_image)
    
    def apply_histogram_eq(self):
        if self.image is None:
            messagebox.showerror("Error", "No image loaded!")
            return
        img_yuv = cv2.cvtColor(self.image, cv2.COLOR_BGR2YUV)
        img_yuv[:,:,0] = cv2.equalizeHist(img_yuv[:,:,0])
        self.processed_image = cv2.cvtColor(img_yuv, cv2.COLOR_YUV2BGR)
        self.display_image(self.processed_image)
    
    def save_image(self):
        if self.processed_image is None:
            messagebox.showerror("Error", "No image to save!")
            return
        file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg")])
        if file_path:
            cv2.imwrite(file_path, self.processed_image)
            messagebox.showinfo("Success", "Image saved successfully!")

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageProcessorApp(root)
    root.mainloop()