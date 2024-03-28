import tkinter as tk
from tkinter import filedialog
from tkinter import simpledialog
import pandas as pd
import seaborn as sb
import matplotlib.pyplot as plt
from pathlib import Path



home = str(Path.home())
print(home)

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
    
    ##sets initial ctrl state
    ctrl_exists = False
    ##searches position column for 'C01' and sets ctrl_exists to True indicating a ctrl is present in the dataset
    if excel_file_df['Position'].str.contains('C01').any(): 
        ctrl_exists = True
    ##if no c01 is found assigns a null value to that well position.
    if ctrl_exists == False:
        excel_file_df.loc[96] = ('C01', 'NaN')

    ##sorts xlsx df##
    excel_file_df = excel_file_df.sort_values('Position')
    excel_file_df[['Concentration', 'V_string']] = excel_file_df['Concentration'].str.extract(r'^(\d+\.\d+)(\D+)?$')
    excel_file_df['Concentration'] = excel_file_df['Concentration'].astype(float)
    excel_file_df = excel_file_df['Concentration'].astype(float)
    

    ## defines a function to create the 96well plate format and orgnaizes data appropriately ##
    def create_plate(value_list):
        #num_rows = len(value_list) // 12 
        plate_df = pd.DataFrame(index=['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H'], columns=range(1, 13))
        for i in range(0, len(value_list)):
            row_index = chr(65 + i // 12)  
            col_index = i % 12 + 1
            #column_name = f'Column_{col_index}'
            plate_df.loc[row_index, col_index] = value_list[i]
        return plate_df
    
    value_list = excel_file_df.tolist()
    df = create_plate(value_list).astype(float)
    
    ##builds heatmap using seaborn and saves it to a folder on the desktop called Heatmaps
    plt.figure(figsize=(17,7))
    heatmap = sb.heatmap(df, robust = True, linewidths=.1, cmap="YlOrRd", annot=True, fmt='.2f', cbar=False, mask=df.isnull())
    heatmap.set_title(f'{heatmap_name}', fontsize=30)
    heatmap.tick_params(top=True, labeltop=True, bottom=False, labelbottom=False)
    plt.yticks(rotation = 0, fontsize=18)
    plt.xticks(rotation=0, fontsize=18)
    heatmap.figure.savefig(home + '\Desktop\Heatmaps' + f'\{heatmap_name}' + '.png')
    