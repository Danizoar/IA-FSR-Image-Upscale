from customtkinter import *
from CTkToolTip import *
from PIL import Image
import os
from threading import Thread

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
        self.geometry(f"{960}x{810}")
        self.resizable(False, False)
        self.title("FSR Image Upscaler")
        self.iconbitmap(r"assets\img\icon.ico")

        # Variables
        self.file_filepath = ""
        self.folder_filepath = ""
        self.log_entry_number = 0

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
        self.frame_main.grid_rowconfigure(0, weight=0)
        self.frame_main.grid_rowconfigure(1, weight=0)
        self.frame_main.grid_rowconfigure(2, weight=0)
        self.frame_main.grid_rowconfigure(3, weight=1)
        self.frame_main.grid_columnconfigure(0, weight=0)
        self.frame_main.grid_columnconfigure(1, weight=1)

        self.frame_file_select = CTkFrame(self.frame_main, border_width=2)
        self.frame_file_select.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        self.frame_file_select.grid_columnconfigure(0, weight=1)  

        self.frame_output = CTkFrame(self.frame_main, border_width=2)
        self.frame_output.grid(row=2, column=0, padx=10, pady=(0, 10), sticky="nsew")
        self.frame_output.grid_columnconfigure(0, weight=1)       

        self.frame_scaling = CTkFrame(self.frame_main, border_width=2)
        self.frame_scaling.grid(row=1, column=0, padx=10, pady=(0, 10), sticky="nsew")
        self.frame_scaling.grid_columnconfigure(0, weight=1)
        self.frame_scaling.grid_columnconfigure(1, weight=1)

        self.frame_about = CTkFrame(self.frame_main, border_width=2)
        self.frame_about.grid(row=0, column=1, padx=(0,10), pady=10, sticky="nsew", rowspan=3)
        self.frame_about.grid_columnconfigure(0, weight=1)

        # Elements
        self.label_output = CTkLabel(self.frame_output, text="Output", font=("Arial", 16, "bold"))
        self.label_output.grid(row=0, column=0, padx=20, pady=10, sticky="ew", columnspan=2)

        #self.window_label = CTkLabel(master=self, text="FSR Upscale GUI", font=("Ariel", 28))
        #self.window_label.grid(row=0, column=0, padx=10, pady=5, sticky="w", columnspan=2)

        # About
        self.image_app_icon = CTkImage(light_image=Image.open(r"assets\img\icon.ico"), dark_image=Image.open(r"assets\img\icon.ico"), size=(280, 280))
        self.label_app_icon = CTkLabel(self.frame_about, image=self.image_app_icon, text="")
        self.label_app_icon.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="ew")

        self.label_about = CTkLabel(self.frame_about, text="About", font=("Arial", 16, "bold"))
        self.label_about.grid(row=1, column=0, padx=20, pady=(0, 10), sticky="ew")

        self.label_about_text = CTkLabel(self.frame_about, justify="left", wraplength=300, text="GUI for FidelityFX-CLI what upscales images with AMD's FidelityFX Super Resolution (FSR) and Contrast Adaptive Sharpening (CAS) technologies.")
        self.label_about_text.grid(row=2, column=0, padx=20, pady=(0, 10), sticky="w")

        self.label_about_credits = CTkLabel(self.frame_about, justify="left", wraplength=300, text="FidelityFX-CLI: GPUOpen\nOriginal: SoyKhaler\nRework: Danizoar")
        self.label_about_credits.grid(row=3, column=0, padx=20, pady=(0, 10), sticky="w")

        self.label_about_version = CTkLabel(self.frame_about, justify="center", wraplength=300, text="Version 1.0")
        self.label_about_version.grid(row=4, column=0, padx=20, pady=(0, 10), sticky="sew")

        # File select
        self.label_file_select = CTkLabel(self.frame_file_select, text="File Select", font=("Arial", 16, "bold"))
        self.label_file_select.grid(row=0, column=0, padx=20, pady=10, sticky="ew", columnspan=2)

        self.frame_choose_type = CTkFrame(self.frame_file_select, fg_color="transparent")
        self.frame_choose_type.grid(row=1, column=0, padx=10, pady=(0, 5), sticky="nsew")

        self.label_choose_type = CTkLabel(self.frame_choose_type, text="Upscale the ")
        self.label_choose_type.grid(row=0, column=0, padx=0, pady=0, sticky="w")

        self.button_seg_file_select = CTkSegmentedButton(self.frame_choose_type, values=["File","Folder"], command=self.choose_type)
        self.button_seg_file_select.grid(row=0, column=1, padx=0, pady=0, sticky="w")
        self.button_seg_file_select.set("File") 

        self.label_select = CTkLabel(self.frame_file_select, text="Select a file to upscale:")
        self.label_select.grid(row=3, column=0, padx=10, pady=0, sticky="w")

        self.entry_file_path = CTkEntry(self.frame_file_select, width=512, placeholder_text=r"C:\..\..\file.png")
        self.entry_file_path.grid(row=4, column=0, padx=10, pady=(0,10), sticky="w")

        self.button_open = CTkButton(self.frame_file_select, text="Open", width=48, command=self.select_onject)
        self.button_open.grid(row=4, column=1, padx=(0,10), pady=(0,10), sticky="e")
        self.button_open_tooltip = CTkToolTip(self.button_open, message="About this project")

        # Image scaling
        self.label_scaling = CTkLabel(self.frame_scaling, text="Image Scaling", font=("Arial", 16, "bold"))
        self.label_scaling.grid(row=0, column=0, padx=20, pady=10, sticky="ew", columnspan=2)

        # Column frames
        self.frame_scaling_column_1 = CTkFrame(self.frame_scaling, fg_color="transparent")
        self.frame_scaling_column_1.grid(row=1, column=0, pady=(0, 10), padx=10, sticky="new")

        self.frame_scaling_column_2 = CTkFrame(self.frame_scaling, fg_color="transparent")
        self.frame_scaling_column_2.grid(row=1, column=1, pady=(0, 10), padx=10, sticky="new")

        # Upscale amount
        self.label_amount = CTkLabel(self.frame_scaling_column_1, text="Select upscale amount:")
        self.label_amount.grid(row=0, column=0, padx=0, pady=0, sticky="w")

        self.frame_scale = CTkFrame(self.frame_scaling_column_1, fg_color="transparent")
        self.frame_scale.grid(row=1, column=0, pady=(0, 10), padx=0, sticky="ew")
        
        self.button_seg_scale_by = CTkSegmentedButton(self.frame_scale, values=["2x","4x","8x","Custom"])
        self.button_seg_scale_by.grid(row=0, column=0, padx=(0, 10), pady=0, sticky="w")
        self.button_seg_scale_by.set("2x") 
        #self.button_seg_scale_by_tooltip = CTkToolTip(self.button_seg_scale_by, message="Upscale image by amount")

        self.entry_custom = CTkEntry(self.frame_scale, width=64, placeholder_text=r"0")
        self.entry_custom.grid(row=0, column=1, padx=(0, 10), pady=0, sticky="w")

        self.checkbox_alpha = CTkCheckBox(self.frame_scaling_column_1, text="Preserve alpha", onvalue=True, offvalue=False, command=self.check_sharpness)
        self.checkbox_alpha.grid(row=2, column=0, pady=10, padx=0, sticky="w")
        self.checkbox_alpha_tooltip = CTkToolTip(self.checkbox_alpha, message="Preserve alpha channel of an image (increases processing time)")

        # Sharpening
        self.checkbox_sharp = CTkCheckBox(self.frame_scaling_column_1, text="Use sharpening", onvalue=True, offvalue=False, command=self.check_sharpness)
        self.checkbox_sharp.grid(row=3, column=0, pady=10, padx=0, sticky="w")

        self.frame_sharp = CTkFrame(self.frame_scaling_column_1, fg_color="transparent")
        self.frame_sharp.grid(row=4, column=0, pady=0, padx=0, sticky="ew")

        self.slider_sharp = CTkSlider(self.frame_sharp, from_=0, to=100, command=self.slide_sharpness, number_of_steps=10, state=DISABLED)
        self.slider_sharp.set(20)
        self.slider_sharp.grid(row=0, column=0, pady=0, padx=(0, 10), sticky="w")

        self.label_sharp_amount = CTkLabel(self.frame_sharp, text=(self.slider_sharp.get()/100))
        self.label_sharp_amount.grid(row=0, column=1, pady=0, padx=0, sticky="w")

        # Downscaling
        self.checkbox_downscaling = CTkCheckBox(self.frame_scaling_column_2, text="Downscale the output", onvalue=True, offvalue=False, command=self.check_sharpness)
        self.checkbox_downscaling.grid(row=0, column=0, pady=10, padx=0, sticky="w")
        self.checkbox_downscaling_tooltip = CTkToolTip(self.checkbox_downscaling, message="Downscale the upscaled image to remove upscaling artefacts")

        self.label_downscale = CTkLabel(self.frame_scaling_column_2, text="Downscale by:")
        self.label_downscale.grid(row=1, column=0, padx=0, pady=0, sticky="w")

        self.frame_downscale = CTkFrame(self.frame_scaling_column_2, fg_color="transparent")
        self.frame_downscale.grid(row=2, column=0, pady=(0, 10), padx=0, sticky="ew")
        
        self.button_seg_downscale_by = CTkSegmentedButton(self.frame_downscale, values=["2x","4x","8x","Custom"])
        self.button_seg_downscale_by.grid(row=0, column=0, padx=(0, 10), pady=0, sticky="w")
        self.button_seg_downscale_by.set("2x") 
        #self.button_seg_downscale_by_tooltip = CTkToolTip(self.button_seg_downscale_by, message="Upscale image by amount")

        self.entry_custom_downscale = CTkEntry(self.frame_downscale, width=64, placeholder_text=r"0")
        self.entry_custom_downscale.grid(row=0, column=1, padx=(0, 10), pady=0, sticky="w")

        self.label_filter = CTkLabel(self.frame_scaling_column_2, text="Filter:")
        self.label_filter.grid(row=3, column=0, padx=0, pady=0, sticky="w")

        self.optionmenu_filter_pick = CTkOptionMenu(self.frame_scaling_column_2, values=["Nearest", "Box", "Bilenear", "Hamming", "Bicubic", "Lanczos"])
        self.optionmenu_filter_pick.grid(row=4, column=0, pady=(0, 10), padx=0, sticky="ew")
        self.optionmenu_filter_pick.set("Lanczos")

        # Output
        self.checkbox_save_extra = CTkCheckBox(self.frame_output, text="Save as a separate file", state=DISABLED)
        self.checkbox_save_extra.grid(row=6, column=0, pady=(0,10), padx=10, sticky="w")
        self.checkbox_save_extra_tooltip = CTkToolTip(self.checkbox_save_extra, message='Save sharpened version as a separate file with "_Sharp" on the end')

        # Console log
        self.frame_scrollable_log = CTkScrollableFrame(self.frame_main, fg_color=self._fg_color)
        self.frame_scrollable_log.grid(row=3, column=0, pady=(0,10), padx=10, sticky="nsew", columnspan=2)
        self.frame_scrollable_log.columnconfigure(0, weight=0)
        self.frame_scrollable_log.columnconfigure(1, weight=0)
        self.frame_scrollable_log.columnconfigure(2, weight=1)

        #self.table_output = CTkTable(self.frame_scrollable_log, row=2, column=2, corner_radius=0)
        #self.table_output.grid(row=0, column=0, pady=0, padx=0, sticky="nsew")

        # Bottom elements
        self.frame_process = CTkFrame(self, fg_color="transparent")
        self.frame_process.grid(row=2, column=0, pady=0, padx=0, sticky="ew")
        self.frame_process.grid_rowconfigure(0, weight=1)
        self.frame_process.columnconfigure(0, weight=0)
        self.frame_process.columnconfigure(1, weight=0)
        self.frame_process.columnconfigure(2, weight=1)

        self.button_start = CTkButton(self.frame_process, width=128, text="Start", command=self.on_start_press)
        self.button_start.grid(row=2, column=0, padx=10, pady=(0, 10))
        self.button_start_tooltip = CTkToolTip(self.button_start, message="Start upscaling")

        self.progress_bar = CTkProgressBar(self.frame_process, orientation="horizontal", mode="determinate", width=256)
        self.progress_bar.set(1)
        self.progress_bar.grid(row=2, column=1, padx=10, pady=(0, 10))
        
        self.button_about = CTkButton(self.frame_process, text="About", width=48, command=self.open_about)
        self.button_about.grid(row=2, column=2, padx=10, pady=(0, 10), sticky="e")
        self.button_about_tooltip = CTkToolTip(self.button_about, message="About this project")

        # Running functions
        self.add_log_entry("FSR Image Upscaler \nVersion 1.0")

    def add_log_entry(self, input):
        input = str(input)
        label_number = CTkLabel(self.frame_scrollable_log, width=32, text=str(self.log_entry_number))
        label_number.grid(row=self.log_entry_number, column=0, padx=(0, 5), pady=1, sticky="ew")

        label_log = CTkLabel(self.frame_scrollable_log, justify="left", wraplength=850, text=input)
        label_log.grid(row=self.log_entry_number, column=2, padx=(10, 0), pady=1, sticky="w")

        frame_divider = CTkFrame(self.frame_scrollable_log, width=5, height=label_log._desired_height)
        frame_divider.grid(row=self.log_entry_number, column=1, padx=0, pady=1, sticky="nsew")

        #frame_divider_line = CTkFrame(self.frame_scrollable_log, height=1)
        #frame_divider_line.grid(row=self.log_entry_number, column=0, padx=0, pady=0, sticky="new", columnspan=3)

        print(input)
        self.log_entry_number+=1

    def choose_type(self, value):
        self.entry_file_path.delete(0, 'end')
        if value=="File":
            self.label_select.configure(text="Select a file to upscale:")
            self.entry_file_path.configure(placeholder_text=r"C:\..\..\file.png")
            if self.file_filepath != "":
                self.entry_file_path.insert(0, self.file_filepath)

        else:
            self.label_select.configure(text="Select a folder to upscale:")
            self.entry_file_path.configure(placeholder_text=r"C:\..\..\folder")
            if self.folder_filepath != "":
                self.entry_file_path.insert(0, self.folder_filepath)
                
        #self.add_log_entry("Switched file type to: "+value)

    def select_onject(self):
        if self.button_seg_file_select.get() == "File":
            filename = filedialog.askopenfilename()
        else:
            filename = filedialog.askdirectory()

        if filename != "":
            self.entry_file_path.delete(0, 'end')
            self.entry_file_path.insert(0, filename)
            if self.button_seg_file_select.get() == "File":
                self.file_filepath = filename
            else:
                self.folder_filepath = filename
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
    
    def start(self):
        pass

    def on_start_press(self):
        self.start()

if __name__ == '__main__':
    App = MainWindow()
    App.mainloop()
