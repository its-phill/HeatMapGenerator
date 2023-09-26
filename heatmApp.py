import tkinter as tk
from tkinter import messagebox
from tkinter import font as tkfont
from tkinter import filedialog
from tkinter import simpledialog
import pandas as pd
import numpy as np
import seaborn as sb
import matplotlib.pyplot as plt
from time import sleep
from  matplotlib.colors import LinearSegmentedColormap
from pathlib import Path


home = str(Path.home())

def ninety_six_well():

    ##select an excel file using tKinter popup file explorer##
    excel_file = filedialog.askopenfilename()
    
    title = tk.Tk()
    title.withdraw()
    heatmap_name = simpledialog.askstring(title="Name Heatmap",prompt="Please Name your heatmap")
        
    ##covert xlsx to df##
    excel_file_df = pd.read_excel(excel_file,
                        index_col = None,
                        header = 1, usecols=['Position', 'Concentration']).astype(str)
        
    ctrl = True
    ctrl = messagebox.askyesno("Control Check","Does this dataset contain C01?")
    
    if ctrl == False:
        excel_file_df.loc[96] = ('C01', 'NaN')

    ##sorts xlsx df##
    excel_file_df = excel_file_df.sort_values('Position')
    excel_file_df[['Concentration', 'V_string']] = excel_file_df['Concentration'].str.extract(r'^(\d+\.\d+)(\D+)?$')
    excel_file_df['Concentration'] = excel_file_df['Concentration'].astype(float)
    excel_file_df = excel_file_df['Concentration'].astype(float)
    

    ## defines a function to create the 96well plate format and orgnaizes data appropriately ##
    def create_plate(value_list):
        num_rows = len(value_list) // 12 
        plate_df = pd.DataFrame(index=['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H'], columns=range(1, 13))
        for i in range(0, len(value_list)):
            row_index = chr(65 + i // 12)  
            col_index = i % 12 + 1
            column_name = f'Column_{col_index}'
            plate_df.loc[row_index, col_index] = value_list[i]
        return plate_df
    
    value_list = excel_file_df.tolist()
    df = create_plate(value_list).astype(float)
    

    plt.figure(figsize=(17,7))
    heatmap = sb.heatmap(df, robust = True, linewidths=.1, cmap=LinearSegmentedColormap.from_list('rg',["r", "w", "g"], N=256), annot=True, fmt='.2f', cbar=False, mask=df.isnull())
    heatmap.set_title(f'{heatmap_name}', fontsize=30)
    heatmap.tick_params(top=True, labeltop=True, bottom=False, labelbottom=False)
    plt.yticks(rotation = 0, fontsize=18)
    plt.xticks(rotation=0, fontsize=18)
    heatmap.figure.savefig(home + '\Heatmaps' + f'\{heatmap_name}' + '.png')
    
    
def three_eighty_four_well():
    ##select an excel file using tKinter popup file explorer##
    excel_file = filedialog.askopenfilename()
    
    title = tk.Tk()
    title.withdraw()
    heatmap_name = simpledialog.askstring(title="Name Heatmap",prompt="Please Name your heatmap")
        
    ##covert xlsx to df##
    excel_file_df = pd.read_excel(excel_file,
                        index_col = None,
                        header = 1, usecols=['Position', 'Concentration']).astype(str)

    ##sorts xlsx df##
    excel_file_df = excel_file_df.sort_values('Position')
    excel_file_df[['Concentration', 'V_string']] = excel_file_df['Concentration'].str.extract(r'^(\d+\.\d+)(\D+)?$')
    excel_file_df['Concentration'] = excel_file_df['Concentration'].astype(float)
    excel_file_df = excel_file_df['Concentration'].astype(float)
    def create_plate(value_list): 
        num_rows = len(value_list) // 24
        plate_df = pd.DataFrame(index=['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P'], columns=range(1, 25))
        for i in range(0, len(value_list)):
            row_index = chr(65 + i // 24)  
            col_index = i % 24 + 1
            column_name = f'Column_{col_index}'
            plate_df.loc[row_index, col_index] = value_list[i]
        return plate_df

    value_list = excel_file_df.tolist()
    df = create_plate(value_list).astype(float)
   
    plt.figure(figsize=(17,7))
    heatmap = sb.heatmap(df, robust = True, linewidths=.1, cmap=LinearSegmentedColormap.from_list('rg',["r", "w", "g"], N=256), annot=True, fmt='.1f', cbar=False, mask=df.isnull())
    heatmap.set_title(f'{heatmap_name}', fontsize=30)
    heatmap.tick_params(top=True, labeltop=True, bottom=False, labelbottom=False)
    plt.yticks(rotation = 0, fontsize=18)
    plt.xticks(rotation=0, fontsize=18)
    heatmap.figure.savefig(home + '\Heatmaps' + f'\{heatmap_name}' + '.png')
 
   


def exit_program():
    root.destroy()

# Create the main window
root = tk.Tk()
root.title("Heatmap Generator")

# Configure the window's appearance
root.geometry("300x200")
root.configure(bg="#F0F0F0")

# Define custom fonts
button_font = tkfont.Font(family="Helvetica", size=12, weight="bold")

# Create the buttons
button1 = tk.Button(root, text="96w plate", command=ninety_six_well, font=button_font, padx=10, pady=5)
button1.pack(pady=10)

button2 = tk.Button(root, text="384w plate", command=three_eighty_four_well, font=button_font, padx=10, pady=5)
button2.pack(pady=10)

exit_button = tk.Button(root, text="Exit", command=exit_program, font=button_font, padx=10, pady=5)
exit_button.pack(pady=10)

# Start the main loop
root.mainloop()



