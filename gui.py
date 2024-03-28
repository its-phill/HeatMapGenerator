import tkinter as tk
from tkinter import font as tkfont
from ninetysixwell import ninety_six_well
from threeeightyfourwell import three_eighty_four_well
import sys

##define gui function called by main function
def gui():

    # def function attached to exit button to close both the script and the gui window
    def exit_program():
        root.quit()
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