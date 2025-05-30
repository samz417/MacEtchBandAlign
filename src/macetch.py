# -*- coding: utf-8 -*-
"""
Created on Thu Mar  6 06:39:29 2025

@author: sz6168
"""

import sys
import os

def resource_path(filename):
    """Get absolute path to resource for PyInstaller"""
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, filename)
    return os.path.abspath(filename)

app_icon_path = resource_path("icon.ico")

import tkinter as tk
from tkinter import ttk
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import platform
from PIL import Image, ImageTk
figure_icons = []


# Data setup
matls = ["Si", "Ge", "4H-SiC", "β-Ga₂O₃", "GaN", "GaAs", "InP", "InAs", "GaSb", "GaP", "AlAs", "InSb", "AlSb", "AlN", "InN"]

cats = ["Au⁺/Au", "Au³⁺/Au", "Cu⁺/Cu", "Cu²⁺/Cu", "Ag⁺/Ag", "Ir³⁺/Ir", "Ni²⁺/Ni", "IrO₂/Ir", "NiₓSiᵧ", "Pt²⁺/Pt", "Pd²⁺/Pd",
        "Al³⁺/Al", "Ru²⁺/Ru", "Co²⁺/Co", "Fe²⁺/Fe", "Zn⁺/Zn", "Ti³⁺/Ti", "Cr³⁺/Cr", "WO₄²⁻/WO₂", "Graphene", "SWCNT", "TiN", 
        "Sn²⁺/Sn", "RuO₄/Ru²⁺", "WO₄²⁻/W₂O₅"]
cols = pd.Series(["Si", "Ge", "4H-SiC", "β-Ga₂O₃", "GaN", "GaAs", "InP", "InAs", "GaSb", "GaP", "AlAs", "InSb", "AlSb", "AlN", "InN", 
                  "", "Metal E°", "", "", "Oxidant E°"])
oxs = ["H₂O₂/H₂O", "MnO₄/Mn²⁺", "Cr₂O₇²⁻/Cr³⁺", "HNO₃/HNO₂", "S₂O₈²⁻/HSO₄⁺"]
VB = pd.DataFrame({'materials': cols, 'value': [-5.15,-4.661,-6.33,-8.8,-7.3,-5.5,-5.72,-5.254,-4.76,-5.91,-5.668,-4.9,-5.2,-6.8,-5.3, np.nan, np.nan, np.nan, np.nan, np.nan]}) #eV from ea + bg
CB = pd.DataFrame({'materials': cols, 'value': [-0.39,-0.44,-1.34,-0.8,-0.34,-0.37,-0.06,0.46,-0.38,-0.79,-0.94,0.28,-0.84,-3.84,0.16, np.nan, np.nan, np.nan, np.nan, np.nan]}) #V (electron affinity)
WF = pd.DataFrame({'materials': cats, 'value': [-5.47, -5.47, -5.10, -5.10, -4.64, 5.42, -5.64, -5.22, -5.22, -6.35, -4.71, -4.50, -4.42, -4.67, -4.55, -5.00, -3.63, -4.33, 4.5, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan]}) #eV
#print(len(WF))
OP = pd.DataFrame({'materials': cats, 'value': [1.692, 1.498, 0.521, 0.349, 0.8, 1.16, -0.257, 0.95,  0.84, 1.188, 0.951, -1.662, 0.455, -0.28, -0.447, -0.7618, -1.63, -0.913, 0.457, 0.3, 1.1, 0.9,  -0.532, 1.3, 0.801]}) #V
#print(len(OP))
OxP = pd.DataFrame({'materials': oxs, 'value':[1.763, 1.51, 1.36, 0.9, 2.123]}) #from Parsian band chart email

eV_bot = -9 #VB bottom
V_bot = -(eV_bot + 4.44)
V_top = -4.44 #CB top
eV_top = V_top + 4.44

CBev = CB.copy()
CBev["value"] = CB["value"] - 4.44

# GUI Setup
root = tk.Tk()
root.title("Material Selector")

# Detect platform
system = platform.system()

# Configure icon
try:
    if system == "Windows":
        icon_path = resource_path("icon.ico")
        print("Loading icon:", icon_path)
        print("Exists?", os.path.exists(icon_path))
        root.iconbitmap(icon_path)
    else:
        # Use .png for macOS/Linux
        icon_path = resource_path("icon.png")
        print("Loading icon (Mac):", icon_path)
        print("Exists?", os.path.exists(icon_path))
        icon = tk.PhotoImage(file=icon_path)
        root.iconphoto(True, icon)
except Exception as e:
    print("Icon load failed:", e)
    
def set_figure_icon(fig, ico_path=None, png_path=None):
    global figure_icons
    if ico_path is None:
        ico_path = resource_path("icon2.ico")
    if png_path is None:
        png_path = resource_path("icon2.png")
    
    try:
        manager = fig.canvas.manager
        window = manager.window  # This is a tk.Tk or tk.Toplevel object on TkAgg

        system = platform.system()
        if system == "Windows" and ico_path:
            # Use .ico for Windows
            window.iconbitmap(ico_path)
        elif png_path:
            # Use .png for macOS/Linux
            icon = tk.PhotoImage(master=window, file=png_path)
            window.iconphoto(True, icon)
            figure_icons.append(icon)
    except Exception as e:
        print("Failed to set figure icon:", e)

semi_dropdown_frame = tk.Frame(root)
lbl1 = tk.Label(semi_dropdown_frame, text="Semiconductor")
lbl1.pack(pady=5)
semi_dropdown_frame.pack(pady=10, fill = 'x', expand = True)


matl_dropdowns = []
selected_materials = []
metal_dropdowns = []
metal_op_checks = []
metal_wf_checks = []
selected_metals = []
ox_dropdowns = []
selected_oxs = []

def add_dropdown():
    if any(not var.get() for var in selected_materials):
        return 
    
    vals = [" "] + matls + ["Add..."]

    selected_material = tk.StringVar()
    selected_materials.append(selected_material)
    
    dropdown = ttk.Combobox(semi_dropdown_frame, textvariable=selected_material, values=vals, width = 25)
    dropdown.pack(pady=5, fill = 'x', expand = True)
    matl_dropdowns.append(dropdown)
    
    def on_select(event):
       if selected_material.get() == "Add...":
           dropdown.set("")
           open_popup()
    
    dropdown.bind("<<ComboboxSelected>>", lambda event: (add_dropdown(), on_select(event)))


def open_popup():
    popup = tk.Toplevel(root)
    popup.title("Add custom semiconductor")
    popup.geometry("200x150")
    
    tk.Label(popup, text="Material Name:").pack()
    material_name_entry = tk.Entry(popup)
    material_name_entry.pack()
    
    tk.Label(popup, text="Electron affinity (V):").pack()
    cb_entry = tk.Entry(popup)
    cb_entry.pack()
    
    tk.Label(popup, text="Bandgap (eV):").pack()
    vb_entry = tk.Entry(popup)
    vb_entry.pack()
    
    def add_material():
        name = material_name_entry.get()
        vb = -1*((float(cb_entry.get()) + 4.44) + float(vb_entry.get())) #eV
        cb = float(cb_entry.get()) # V
        
        if name and name not in matls:
            matls.append(name)
            VB.loc[len(VB)] = [name, vb]
            CB.loc[len(CB)] = [name, cb]
            for dropdown in matl_dropdowns:
                dropdown['values'] = matls + ["Add..."]
            dropdown.set(name)
        popup.destroy()
    
    tk.Button(popup, text="Add", command=add_material).pack()
    popup.mainloop()


add_dropdown()

metal_dropdown_frame = tk.Frame(root)
lbl2 = tk.Label(metal_dropdown_frame, text="Metal")
lbl2.pack(pady=5)
metal_dropdown_frame.pack(pady=10, fill = 'x', expand = True)


def add_dropdown2():
    if any(not var.get() for var in selected_metals):
        return 

    vals = [" "] + cats + ["Add..."]
    selected_metal = tk.StringVar()
    selected_metals.append(selected_metal)

    # Create a new container frame for dropdown + checkboxes
    container = tk.Frame(metal_dropdown_frame)
    container.pack(pady=5, fill='x', expand=True)

    dropdown2 = ttk.Combobox(container, textvariable=selected_metal, values=vals, width=25)
    dropdown2.pack(side='top', fill='x', expand=True)

    # Checkboxes in a subframe
    checkbox_frame = tk.Frame(container)
    checkbox_frame.pack(side='top', anchor='center', pady=2)

    op_var = tk.BooleanVar()
    wf_var = tk.BooleanVar()
    op_check = tk.Checkbutton(checkbox_frame, text="OP", variable=op_var)
    wf_check = tk.Checkbutton(checkbox_frame, text="WF", variable=wf_var)
    op_check.pack(side='left')
    wf_check.pack(side='left')
    metal_op_checks.append(op_var)
    metal_wf_checks.append(wf_var)

    metal_dropdowns.append(dropdown2)

    def on_select(event):
        if selected_metal.get() == "Add...":
            dropdown2.set("")
            open_popup2()

    dropdown2.bind("<<ComboboxSelected>>", lambda event: (add_dropdown2(), on_select(event)))


def open_popup2():
    popup = tk.Toplevel(root)
    popup.title("Add custom catalyst")
    popup.geometry("200x150")
    
    tk.Label(popup, text="Material Name:").pack()
    material_name_entry = tk.Entry(popup)
    material_name_entry.pack()
    
    tk.Label(popup, text="Work Function (eV):").pack()
    WF_entry = tk.Entry(popup)
    WF_entry.pack()
    
    tk.Label(popup, text="Oxidation Potential (V):").pack()
    OP_entry = tk.Entry(popup)
    OP_entry.pack()
    
    def add_material():
        name = material_name_entry.get()
        wf = float(WF_entry.get()) #eV
        op = float(OP_entry.get()) # V
        
        if name and name not in cats:
            cats.append(name)
            WF.loc[len(WF)] = [name, wf]
            OP.loc[len(OP)] = [name, op]
            for dropdown in metal_dropdowns:
                dropdown['values'] = cats + ["Add..."]
            dropdown.set(name)
        popup.destroy()
    
    tk.Button(popup, text="Add", command=add_material).pack()
    popup.mainloop()

add_dropdown2()

ox_dropdown_frame = tk.Frame(root)
lbl2 = tk.Label(ox_dropdown_frame, text="Oxidant")
lbl2.pack(pady=5)
ox_dropdown_frame.pack(pady=10, fill = 'x', expand = True)


def add_dropdown3():
    if any(not var.get() for var in selected_oxs):
        return 
    
    vals = [" "] +  oxs + ["Add..."]
    
    selected_ox = tk.StringVar()
    selected_oxs.append(selected_ox)
    
    dropdown3 = ttk.Combobox(ox_dropdown_frame, textvariable=selected_ox, values=vals, width = 25)
    dropdown3.pack(pady=5, fill = 'x', expand = True)
    ox_dropdowns.append(dropdown3)
    
    def on_select(event):
       if selected_ox.get() == "Add...":
           dropdown3.set("")
           open_popup3()
    
    dropdown3.bind("<<ComboboxSelected>>", lambda event: (add_dropdown3(), on_select(event)))

def open_popup3():
    popup = tk.Toplevel(root)
    popup.title("Add custom catalyst")
    popup.geometry("200x150")
    
    tk.Label(popup, text="Oxidant Name:").pack()
    material_name_entry = tk.Entry(popup)
    material_name_entry.pack()
    
    tk.Label(popup, text="Oxidation Potential (V):").pack()
    OxP_entry = tk.Entry(popup)
    OxP_entry.pack()
    
    def add_material():
        name = material_name_entry.get()
        oxp = float(OxP_entry.get()) # V
        
        if name and name not in oxs:
            oxs.append(name)
            OxP.loc[len(OxP)] = [name, oxp]
            for dropdown in ox_dropdowns:
                dropdown['values'] = oxs + ["Add..."]
            dropdown.set(name)
        popup.destroy()
    
    tk.Button(popup, text="Add", command=add_material).pack()
    popup.mainloop()

add_dropdown3()

def plot_selected_materials():
    materials = sorted([var.get() for var in selected_materials if var.get() and var.get() not in ("Add...", " ")], key=lambda x: matls.index(x))
    oxs_sel = sorted([var.get() for var in selected_oxs if var.get() and var.get() not in ("Add...", " ")], key=lambda x: oxs.index(x))
        
    metals_wf = []
    metals_op = []
    metal_labels = []

    for var, wf_chk, op_chk in zip(selected_metals, metal_wf_checks, metal_op_checks):
        val = var.get()
        if val and val not in ("Add...", " "):
            if wf_chk.get():
                metals_wf.append(val)
            if op_chk.get():
                metals_op.append(val)
            metal_labels.append(val)

    metals = sorted(set(metals_wf + metals_op), key=lambda x: cats.index(x))
    f_WF = WF[WF['materials'].isin(metals_wf)].copy()
    f_OP = OP[OP['materials'].isin(metals_op)].copy()

    # Combine all selections
    all_sel = materials + metal_labels + oxs_sel
    
    f_VB = VB[VB['materials'].isin(materials)].copy()
    f_CB = CB[CB['materials'].isin(materials)].copy()
    f_OxP = OxP[OxP['materials'].isin(oxs_sel)].copy()
    f_VB.loc[:, "heights"] = f_VB.value - eV_bot
    f_CB.loc[:, "heights"] = V_top - np.abs(f_CB.value)
    
    xtv = np.arange(len(all_sel)+1)
    
    total_x_items = len(all_sel)
    fig_width = max(6, total_x_items * 0.75)  # minimum width 6, scales with labels
    
    plt.rcParams["font.weight"] = "bold"
    plt.rcParams["axes.labelweight"] = "bold"
    plt.rcParams["axes.axisbelow"] = True
    fig, ax1 = plt.subplots(figsize=(fig_width, 6))
    ax1.set_ylabel("Potential Relative to NHE (V)", color='C2', rotation=90)
    ax1.tick_params(axis='y', labelcolor='C2')
    ax1.set_xlabel("")
    
    ax1.bar(xtv[:len(f_CB)], f_CB['heights'], bottom=f_CB.value, color='powderblue', label="Conduction Band")
    
    ax2 = ax1.twinx()
    ax1.set_yticks([-4.44, -3.5, -2.5, -1.5, -0.5, 0.5, 1.5, 2.5, 3.5, 4.5])
    ax1.set_ylim(V_bot, V_top)
    ax1.set_axisbelow(True)
    ax1.yaxis.grid(color='lightgray')
    ax2.set_yticks(np.linspace(eV_bot, eV_top, 10))
    ax2.set_ylim(eV_bot, eV_top)
    ax2.set_ylabel("Energy Relative to Vacuum (eV)", color='C5', rotation=270, labelpad=15)
    ax2.bar(xtv[:len(f_VB)], f_VB['heights'], bottom=eV_bot, color='darkseagreen', alpha=0.8, label="Valence Band")
    
    # Plot metals and oxidants as 0.1 eV bars in the same column
    bar_height = 0.1
    metal_offset = len(materials)
    for i, metal in enumerate(metal_labels):
        x_pos = xtv[metal_offset + i]
        if metal in f_WF['materials'].values:
            val = f_WF[f_WF['materials'] == metal].iloc[0]['value']
            ax2.bar(x_pos, bar_height, bottom=val, color='maroon', alpha=0.8, label="Work Function" if i == 0 else "")
        if metal in f_OP['materials'].values:
            val = f_OP[OP['materials'] == metal].iloc[0]['value']
            ax1.bar(x_pos, bar_height, bottom=val, color='goldenrod', alpha=0.8, label="Metal Oxidation Potential" if i == 0 else "")
    
    for i in range(len(f_OxP)):
        x_pos = xtv[len(materials) + len(metal_labels) + i]
        ax1.bar(x_pos, bar_height, bottom=f_OxP.iloc[i]['value'], color='royalblue', alpha=0.8, label="Oxidant Potential" if i == 0 else "")
           
    ax1.set_xticks(xtv)
    ax1.set_xticklabels(all_sel + [" "], rotation=0)
    plt.title("Band Structure for Selected Materials")
    
    # Handle legend items dynamically
    handles1, labels1 = ax1.get_legend_handles_labels()
    handles2, labels2 = ax2.get_legend_handles_labels()
    
    # Ensure legend items exist before swapping
    handles = handles1 + handles2
    labels = labels1 + labels2
    
    if len(handles) >= 5:
        handles[1], handles[2], handles[3], handles[4] = handles[3], handles[4], handles[1], handles[2]
        labels[1], labels[2], labels[3], labels[4] = labels[3], labels[4], labels[1], labels[2]
    
    if handles:
        plt.legend(handles=handles, labels=labels, loc='upper right')
    set_figure_icon(fig, ico_path=resource_path("icon2.ico"), png_path=resource_path("icon2.png"))
    plt.show(block=False)

plot_button = tk.Button(root, text="Plot", command=plot_selected_materials)
plot_button.pack(pady=10)

root.mainloop()

