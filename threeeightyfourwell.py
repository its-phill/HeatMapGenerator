import tkinter as tk
from tkinter import filedialog
from tkinter import simpledialog
import pandas as pd
import seaborn as sb
import matplotlib.pyplot as plt
from pathlib import Path

##sets home path to later save the heatmap to a desktop folder called 'Heatmaps'
home = str(Path.home())

##define 384 functionality 
def three_eighty_four_well():
    ##select an excel file using tKinter popup file explorer##
    excel_file = filedialog.askopenfilename()
    ##creates and manages a tkinter window pop-ups prompting users 
    ##for heatmap name variable that is later used for naming the heatmapp 
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
        #num_rows = len(value_list) // 24
        plate_df = pd.DataFrame(index=['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P'], columns=range(1, 25))
        for i in range(0, len(value_list)):
            row_index = chr(65 + i // 24)  
            col_index = i % 24 + 1
            #column_name = f'Column_{col_index}'
            plate_df.loc[row_index, col_index] = value_list[i]
        return plate_df
    ##takes sorted df and converts to list then passes the list into the create plate function to generate the proper dataframe
    value_list = excel_file_df.tolist()
    df = create_plate(value_list).astype(float)
    ##generate the heatmap using seaborn and save the png to a folder on the desktop
    plt.figure(figsize=(17,7))
    heatmap = sb.heatmap(df, robust = True, linewidths=.1, cmap="YlOrRd", annot=True, fmt='.1f', cbar=False, mask=df.isnull())
    heatmap.set_title(f'{heatmap_name}', fontsize=30)
    heatmap.tick_params(top=True, labeltop=True, bottom=False, labelbottom=False)
    plt.yticks(rotation = 0, fontsize=18)
    plt.xticks(rotation=0, fontsize=18)
    heatmap.figure.savefig(home + '\Desktop\Heatmaps' + f'\{heatmap_name}' + '.png')

