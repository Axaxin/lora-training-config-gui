import tkinter as tk
from tkinter import filedialog, messagebox
import json
import os
import subprocess
import threading



def load_configs():
    config_files = os.listdir("gui_configs")
    selected_config=configs_var.get()
    if not selected_config:
        configs_var.set("Select a config")
    configs_menu["menu"].delete(0, "end")
    for config in config_files:
        configs_menu["menu"].add_command(label=config, command=lambda conf=config: (configs_var.set(conf), load_config_to_form()))


def load_config_to_form():
    selected_config = configs_var.get()
    if selected_config == "Select a config":
        blank_config()
        return
    with open(os.path.join("gui_configs", selected_config), "r") as config_file:
        config_data = json.load(config_file)
    pretrained_model_var.set(config_data["pretrained_model"])
    train_data_dir_var.set(config_data["train_data_dir"])
    output_name_var.set(config_data["output_name"])
    output_dir_var.set(config_data["output_dir"])
    resolution_width_var.set(config_data["resolution_width"])
    resolution_height_var.set(config_data["resolution_height"])
    batch_size_var.set(config_data["batch_size"])
    max_train_epochs_var.set(config_data["max_train_epochs"])
    network_dim_var.set(config_data["network_dim"])
    network_alpha_var.set(config_data["network_alpha"])
    lr_var.set(config_data["lr"])
    unet_lr_var.set(config_data["unet_lr"])
    text_encoder_lr_var.set(config_data["text_encoder_lr"])
    save_model_as_var.set(config_data["save_model_as"])

import shutil

def save_config():
    new_config = {
        "pretrained_model": pretrained_model_var.get(),
        "train_data_dir": train_data_dir_var.get(),
        "output_name": output_name_var.get(),
        "output_dir": output_dir_var.get(),
        "resolution_width": resolution_width_var.get(),
        "resolution_height": resolution_height_var.get(),
        "batch_size": batch_size_var.get(),
        "max_train_epochs": max_train_epochs_var.get(),
        "network_dim": network_dim_var.get(),
        "network_alpha": network_alpha_var.get(),
        "lr": lr_var.get(),
        "unet_lr": unet_lr_var.get(),
        "text_encoder_lr": text_encoder_lr_var.get(),
        "save_model_as": save_model_as_var.get(),
    }
    selected_config = configs_var.get()
    if selected_config == "Select a config":
        messagebox.showerror("Error", "Please select a config to save.")
        return
    elif selected_config == "New config":
        config_save_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")], initialdir=os.getcwd()+'/gui_configs')
        if config_save_path:
            with open(config_save_path, "w") as config_file:
                json.dump(new_config, config_file)
            # 更新下拉菜单
            newconfigname=config_save_path.split('/')[-1]
            configs_var.set(newconfigname)
            load_configs()
    else:
        result = messagebox.askyesnocancel("Overwrite config", f"Do you want to overwrite {selected_config}?")
        if result is None:
            return
        elif result:
            config_name = selected_config
            with open(os.path.join("gui_configs", f"{config_name}"), "w") as config_file:
                json.dump(new_config, config_file)
        else:
            config_save_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")], initialdir=os.getcwd()+'/gui_configs')
            if config_save_path:
                with open(config_save_path, "w") as config_file:
                    json.dump(new_config, config_file)
                # 更新下拉菜单
                newconfigname=config_save_path.split('/')[-1]
                configs_var.set(newconfigname)
                load_configs()
                load_config_to_form()

def delete_config():
    selected_config = configs_var.get()
    if selected_config == "Select a config":
        return
    result = messagebox.askyesno("Delete config", f"Are you sure you want to delete {selected_config}?")
    if result:
        os.remove(os.path.join("gui_configs", selected_config))
        configs_var.set("Select a config")
        load_configs()
        load_default_config()

def blank_config():
    pretrained_model_var.set("")
    train_data_dir_var.set("")
    output_name_var.set("")
    output_dir_var.set("")
    resolution_width_var.set("")
    resolution_height_var.set("")
    batch_size_var.set("")
    max_train_epochs_var.set("")
    network_dim_var.set("")
    network_alpha_var.set("")
    lr_var.set("")
    unet_lr_var.set("")
    text_encoder_lr_var.set("")
    save_model_as_var.set("safetensors")

def load_default_config():
    load_config_to_form()

def new_blank_config():
    blank_config()
    configs_var.set('New config')

def reset_default():
    pretrained_model_var.set("./sd_models/model.ckpt")
    train_data_dir_var.set("./train/aki")
    output_name_var.set("aki")
    output_dir_var.set("./output")
    resolution_width_var.set("512")
    resolution_height_var.set("512")
    batch_size_var.set("1")
    max_train_epochs_var.set("10")
    network_dim_var.set("32")
    network_alpha_var.set("32")
    lr_var.set("1e-4")
    unet_lr_var.set("1e-4")
    text_encoder_lr_var.set("1e-5")
    save_model_as_var.set("safetensors")


def execute_script():
    # Run the updated script
    try:
        run_button.config(state=tk.DISABLED)
        script_path="lora_train_script_modified.ps1"
        subprocess.run(["powershell.exe", "-ExecutionPolicy", "Unrestricted", f".\\{script_path}"])
    finally:
        run_button.config(state=tk.NORMAL)

def execute_script_threaded():
    # Update the script with new parameters
    script_path = "lora_train_script.ps1"
    with open(script_path, "r") as file:
        script_content = file.read()
        script_content = script_content.replace("$pretrained_model = \"./sd-models/model.ckpt\"", f"$pretrained_model = \"{pretrained_model_var.get()}\"")
        script_content = script_content.replace("$train_data_dir = \"./train/aki\"", f"$train_data_dir = \"{train_data_dir_var.get()}\"")
        script_content = script_content.replace("$output_name = \"aki\"", f"$output_name = \"{output_name_var.get()}\"")
        script_content = script_content.replace("$output_dir = \"./output\"", f"$output_dir = \"{output_dir_var.get()}\"")
        script_content = script_content.replace("$resolution = \"512,512\"", f"$resolution = \"{resolution_width_var.get()},{resolution_height_var.get()}\"")
        script_content = script_content.replace("$batch_size = 1", f"$batch_size = {batch_size_var.get()}")
        script_content = script_content.replace("$max_train_epoches = 10", f"$max_train_epoches = {max_train_epochs_var.get()}")
        script_content = script_content.replace("$network_dim = 32", f"$network_dim = {network_dim_var.get()}")
        script_content = script_content.replace("$network_alpha = 32", f"$network_alpha = {network_alpha_var.get()}")
        script_content = script_content.replace("$lr = \"1e-4\"", f"$lr = \"{lr_var.get()}\"")
        script_content = script_content.replace("$unet_lr = \"1e-4\"", f"$unet_lr = \"{unet_lr_var.get()}\"")
        script_content = script_content.replace("$text_encoder_lr = \"1e-5\"", f"$text_encoder_lr = \"{text_encoder_lr_var.get()}\"")
        script_content = script_content.replace("$save_model_as = \"safetensors\"", f"$save_model_as = \"{save_model_as_var.get()}\"")

    script_path="lora_train_script_modified.ps1"
    with open(script_path, "w") as file:
        file.write(script_content)
    script_thread = threading.Thread(target=execute_script)
    script_thread.start()

def browse_pretrained_model():
    selected_path = filedialog.askopenfilename()
    if selected_path:
        pretrained_model_var.set(selected_path)

def browse_train_data_directory():
    selected_path = filedialog.askdirectory()
    if selected_path:
        train_data_dir_var.set(selected_path)

def browse_output_directory():
    selected_path = filedialog.askdirectory()
    if selected_path:
        output_dir_var.set(selected_path)





#Main Window

root = tk.Tk()
root.title("Lora Train GUI")

#Configurations Menu

configs_frame = tk.Frame(root)
configs_frame.grid(row=0, column=0, sticky="w")

configs_label = tk.Label(configs_frame, text="Configurations:")
configs_label.pack(side="left")

configs_var = tk.StringVar(root)
configs_menu = tk.OptionMenu(configs_frame, configs_var, "Select a config")
configs_menu.pack(side="left")

load_configs_button = tk.Button(configs_frame, text="New", command=new_blank_config)
load_configs_button.pack(side="left")

save_configs_button = tk.Button(configs_frame, text="Save", command=save_config)
save_configs_button.pack(side="left")

delete_configs_button = tk.Button(configs_frame, text="Delete", command=delete_config)
delete_configs_button.pack(side="left")

load_default_config_button = tk.Button(configs_frame, text="Reset", command=reset_default)
load_default_config_button.pack(side="left")

#Parameters

parameters_frame = tk.Frame(root)
parameters_frame.grid(row=1, column=0, sticky="w")

# ...
pretrained_model_button = tk.Button(parameters_frame, text="Browse", command=browse_pretrained_model)
pretrained_model_button.grid(row=0, column=2, sticky="w")

train_data_dir_button = tk.Button(parameters_frame, text="Browse", command=browse_train_data_directory)
train_data_dir_button.grid(row=1, column=2, sticky="w")

output_dir_button = tk.Button(parameters_frame, text="Browse", command=browse_output_directory)
output_dir_button.grid(row=3, column=2, sticky="w")


pretrained_model_label = tk.Label(parameters_frame, text="Pretrained Model:")
pretrained_model_label.grid(row=0, column=0, sticky="e")
pretrained_model_var = tk.StringVar()
pretrained_model_entry = tk.Entry(parameters_frame, textvariable=pretrained_model_var)
pretrained_model_entry.grid(row=0, column=1, sticky="w")

train_data_dir_label = tk.Label(parameters_frame, text="Train Data Directory:")
train_data_dir_label.grid(row=1, column=0, sticky="e")
train_data_dir_var = tk.StringVar()
train_data_dir_entry = tk.Entry(parameters_frame, textvariable=train_data_dir_var)
train_data_dir_entry.grid(row=1, column=1, sticky="w")

output_name_label = tk.Label(parameters_frame, text="Output Name:")
output_name_label.grid(row=2, column=0, sticky="e")
output_name_var = tk.StringVar()
output_name_entry = tk.Entry(parameters_frame, textvariable=output_name_var)
output_name_entry.grid(row=2, column=1, sticky="w")

output_dir_label = tk.Label(parameters_frame, text="Output Directory:")
output_dir_label.grid(row=3, column=0, sticky="e")
output_dir_var = tk.StringVar()
output_dir_entry = tk.Entry(parameters_frame, textvariable=output_dir_var)
output_dir_entry.grid(row=3, column=1, sticky="w")

resolution_width_label = tk.Label(parameters_frame, text="Resolution Width:")
resolution_width_label.grid(row=4, column=0, sticky="e")
resolution_width_var = tk.StringVar()
resolution_width_entry = tk.Entry(parameters_frame, textvariable=resolution_width_var)
resolution_width_entry.grid(row=4, column=1, sticky="w")

resolution_height_label = tk.Label(parameters_frame, text="Resolution Height:")
resolution_height_label.grid(row=5, column=0, sticky="e")
resolution_height_var = tk.StringVar()
resolution_height_entry = tk.Entry(parameters_frame, textvariable=resolution_height_var)
resolution_height_entry.grid(row=5, column=1, sticky="w")

batch_size_label = tk.Label(parameters_frame, text="Batch Size:")
batch_size_label.grid(row=6, column=0, sticky="e")
batch_size_var = tk.StringVar()
batch_size_entry = tk.Entry(parameters_frame, textvariable=batch_size_var)
batch_size_entry.grid(row=6, column=1, sticky="w")

max_train_epochs_label = tk.Label(parameters_frame, text="Max Train Epochs:")
max_train_epochs_label.grid(row=7, column=0, sticky="e")
max_train_epochs_var = tk.StringVar()
max_train_epochs_entry = tk.Entry(parameters_frame, textvariable=max_train_epochs_var)
max_train_epochs_entry.grid(row=7, column=1, sticky="w")

network_dim_label = tk.Label(parameters_frame, text="Network Dim:")
network_dim_label.grid(row=8, column=0, sticky="e")
network_dim_var = tk.StringVar()
network_dim_entry = tk.Entry(parameters_frame, textvariable=network_dim_var)
network_dim_entry.grid(row=8, column=1, sticky="w")

network_alpha_label = tk.Label(parameters_frame, text="Network Alpha:")
network_alpha_label.grid(row=9, column=0, sticky="e")
network_alpha_var = tk.StringVar()
network_alpha_entry = tk.Entry(parameters_frame, textvariable=network_alpha_var)
network_alpha_entry.grid(row=9, column=1, sticky="w")

lr_label = tk.Label(parameters_frame, text="Learning Rate:")
lr_label.grid(row=10, column=0, sticky="e")
lr_var = tk.StringVar()
lr_entry = tk.Entry(parameters_frame, textvariable=lr_var)
lr_entry.grid(row=10, column=1, sticky="w")

unet_lr_label = tk.Label(parameters_frame, text="UNET Learning Rate:")
unet_lr_label.grid(row=11, column=0, sticky="e")
unet_lr_var = tk.StringVar()
unet_lr_entry = tk.Entry(parameters_frame, textvariable=unet_lr_var)
unet_lr_entry.grid(row=11, column=1, sticky="w")

text_encoder_lr_label = tk.Label(parameters_frame, text="Text EncoderLearning Rate:")
text_encoder_lr_label.grid(row=12, column=0, sticky="e")
text_encoder_lr_var = tk.StringVar()
text_encoder_lr_entry = tk.Entry(parameters_frame, textvariable=text_encoder_lr_var)
text_encoder_lr_entry.grid(row=12, column=1, sticky="w")

save_model_as_label = tk.Label(parameters_frame, text="Save Model As:")
save_model_as_label.grid(row=13, column=0, sticky="e")
save_model_as_var = tk.StringVar()
save_model_as_var.set("safetensors")
save_model_as_ck1 = tk.Radiobutton(parameters_frame, text="safetensors", variable=save_model_as_var, value="safetensors")
save_model_as_ck1.grid(row=13, column=1, sticky="w")
save_model_as_ck2 = tk.Radiobutton(parameters_frame, text="ckpt", variable=save_model_as_var, value="ckpt")
save_model_as_ck2.grid(row=14, column=1, sticky="w")
save_model_as_ck3 = tk.Radiobutton(parameters_frame, text="pt", variable=save_model_as_var, value="pt")
save_model_as_ck3.grid(row=15, column=1, sticky="w")

#Run Button

run_button = tk.Button(root, text="Start Training", command=execute_script_threaded)
run_button.grid(row=3, column=1, sticky="e")

info_text = "Note: To stop training, just close the powershell window."
info_label = tk.Label(root, text=info_text)
info_label.grid(row=3, column=0, sticky="w")



#Initialize configs and form
load_configs()
load_default_config()

root.mainloop()
