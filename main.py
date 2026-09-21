from customtkinter import *
from CTkToolTip import *
import os

set_default_color_theme("assets/themes/red.json")

class AboutWindow(CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Window properties
        self.geometry(f"{640}x{240}")
        self.resizable(False, False)
        self.title("About")
        self.wm_attributes('-topmost', 'true')

class MainWindow(CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Window properties
        self.geometry(f"{960}x{720}")
        self.resizable(False, False)
        self.title("FSR Image Upscaler")
        self.iconbitmap("assets\img\icon.ico")

        # Additional windows
        self.about = None

        # Grid definitions
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=0)
        self.grid_columnconfigure(0, weight=1)

        # Frames
        self.frame_main = CTkFrame(self)
        self.frame_main.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
        self.frame_main.grid_columnconfigure(0, weight=0)
        self.frame_main.grid_columnconfigure(1, weight=1)

        self.frame_file_select = CTkFrame(self.frame_main, border_width=2)
        self.frame_file_select.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        self.frame_file_select.grid_columnconfigure(0, weight=1)  

        self.frame_output = CTkFrame(self.frame_main, border_width=2)
        self.frame_output.grid(row=1, column=0, padx=10, pady=(0, 10), sticky="nsew")
        self.frame_output.grid_columnconfigure(0, weight=1)       

        self.frame_scaling = CTkFrame(self.frame_main, border_width=2)
        self.frame_scaling.grid(row=2, column=0, padx=10, pady=(0, 10), sticky="nsew")
        self.frame_scaling.grid_columnconfigure(0, weight=1)

        self.frame_about = CTkFrame(self.frame_main, border_width=2)
        self.frame_about.grid(row=0, column=1, padx=(0,10), pady=10, sticky="nsew", rowspan=3)
        self.frame_about.grid_columnconfigure(0, weight=1)

        # Elements
        self.label_file_select = CTkLabel(self.frame_file_select, text="File Select", font=("Arial", 16, "bold"))
        self.label_file_select.grid(row=0, column=0, padx=20, pady=10, sticky="ew", columnspan=2)

        self.label_output = CTkLabel(self.frame_output, text="Output", font=("Arial", 16, "bold"))
        self.label_output.grid(row=0, column=0, padx=20, pady=10, sticky="ew", columnspan=2)

        self.label_scaling = CTkLabel(self.frame_scaling, text="Image Scaling", font=("Arial", 16, "bold"))
        self.label_scaling.grid(row=0, column=0, padx=20, pady=10, sticky="ew", columnspan=2)

        #self.window_label = CTkLabel(master=self, text="FSR Upscale GUI", font=("Ariel", 28))
        #self.window_label.grid(row=0, column=0, padx=10, pady=5, sticky="w", columnspan=2)

        # About
        self.label_about = CTkLabel(self.frame_about, text="About", font=("Arial", 16, "bold"))
        self.label_about.grid(row=0, column=0, padx=20, pady=10, sticky="ew", columnspan=2)

        # File select
        self.button_seg_file_select = CTkSegmentedButton(self.frame_file_select, values=["File","Folder"])
        self.button_seg_file_select.grid(row=1, column=0, padx=10, pady=(0,10), sticky="w")
        self.button_seg_file_select.set("File") 

        self.label_select = CTkLabel(self.frame_file_select, text="Select a file to upscale:")
        self.label_select.grid(row=2, column=0, padx=10, pady=0, sticky="w")

        self.entry_file_path = CTkEntry(self.frame_file_select, width=512, placeholder_text=r"C:\..\...\file.png")
        self.entry_file_path.grid(row=3, column=0, padx=10, pady=(0,10), sticky="w")

        self.button_open = CTkButton(self.frame_file_select, text="Open", width=48, command=self.select_onject)
        self.button_open.grid(row=3, column=1, padx=(0,10), pady=(0,10), sticky="e")
        self.button_open_tooltip = CTkToolTip(self.button_open, message="About this project")

        # Upscale amount
        self.button_seg_scale_by = CTkSegmentedButton(self.frame_scaling, values=["2x","4x","8x","Custom"])
        self.button_seg_scale_by.grid(row=1, column=0, padx=10, pady=10, sticky="w")
        self.button_seg_scale_by.set("2x") 
        #self.button_seg_scale_by_tooltip = CTkToolTip(self.button_seg_scale_by, message="Upscale image by amount")

        # Sharpening
        self.checkbox_sharp = CTkCheckBox(self.frame_scaling, text="Use sharpening", onvalue=True, offvalue=False, command=self.check_sharpness)
        self.checkbox_sharp.grid(row=2, column=0, pady=10, padx=10, sticky="w")
        self.checkbox_sharp_tooltip = CTkToolTip(self.checkbox_sharp , message="Upscale image by amount")

        self.slider_sharp = CTkSlider(self.frame_scaling, from_=0, to=100, command=self.slide_sharpness, number_of_steps=10, state=DISABLED)
        self.slider_sharp.set(20)
        self.slider_sharp.grid(row=3, column=0, pady=(0,10), padx=10)

        self.label_sharp_amount = CTkLabel(self.frame_scaling, text=(self.slider_sharp.get()/100))
        self.label_sharp_amount.grid(row=3, column=1, pady=(0,10), padx=10)

        self.checkbox_save_extra = CTkCheckBox(self.frame_scaling, text="Save as a separate file", state=DISABLED)
        self.checkbox_save_extra.grid(row=4, column=0, pady=(0,10), padx=10, sticky="w")
        self.checkbox_save_extra_tooltip = CTkToolTip(self.checkbox_save_extra, message='Save sharpened version as a separate file with "_Sharp" on the end')

        # Bottom elements
        self.frame_process = CTkFrame(self, fg_color="transparent")
        self.frame_process.grid(row=2, column=0, pady=0, padx=0, sticky="ew")
        self.frame_process.grid_rowconfigure(0, weight=1)
        self.frame_process.columnconfigure(0, weight=0)
        self.frame_process.columnconfigure(1, weight=0)
        self.frame_process.columnconfigure(2, weight=1)

        self.button_start = CTkButton(self.frame_process, width=128, text="Start")
        self.button_start.grid(row=2, column=0, padx=10, pady=(0, 10))
        self.button_start_tooltip = CTkToolTip(self.button_start, message="Start upscaling")

        self.progress_bar = CTkProgressBar(self.frame_process, orientation="horizontal", mode="determinate", width=256)
        self.progress_bar.set(1)
        self.progress_bar.grid(row=2, column=1, padx=10, pady=(0, 10))
        
        self.button_about = CTkButton(self.frame_process, text="About", width=48, command=self.open_about)
        self.button_about.grid(row=2, column=2, padx=10, pady=(0, 10), sticky="e")
        self.button_about_tooltip = CTkToolTip(self.button_about, message="About this project")

        # Running functions


    def select_onject(self):
        filename = filedialog.askopenfilename()
        if filename != "":
            self.entry_file_path.delete(0, 'end')
            self.entry_file_path.insert(0, filename)
        else:
            pass

    def check_sharpness(self):
        if self.checkbox_sharp.get():
            self.slider_sharp.configure(state=NORMAL)
            self.checkbox_save_extra.configure(state=NORMAL)
        else:
            self.slider_sharp.configure(state=DISABLED)
            self.checkbox_save_extra.configure(state=DISABLED)

    def slide_sharpness(self, value):
        if value<10:
            self.slider_sharp.set(10)
            value = 10
        self.label_sharp_amount.configure(text=value/100)

    def open_about(self):
        if self.about is None or not self.about.winfo_exists():
            self.about = AboutWindow(self)
        else:
            self.about.focus()
        
if __name__ == '__main__':
    App = MainWindow()
    App.mainloop()