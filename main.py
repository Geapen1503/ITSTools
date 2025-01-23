import sys
import tkinter as tk
from tkinter import ttk
from tkinter import PhotoImage
from tkinter.scrolledtext import ScrolledText
import subprocess
import os
import ctypes



"""
         **********************************************************************************         
      ****************************************************************************************      
    ********************************************************************************************    
  ************************************************************************************************  
 ************************************************************************************************** 
*********************************************+++++++++**********************************************
*************************************++=-::.............::-==+**************************************
********************************++=-:...  ....................::-=+*********************************
*****************************+=-:..  ....:::-----------:::.........-=++*****************************
**************************+=-:......:--=+++*************+++==-:... ...:=+***************************
************************+-:... .:-=++**************************+=-:.....:-=*************************
**********************+-......-=+**********************************+-:.....:=***********************
********************+-..  ..-+****************************************=:..  .:+*********************
******************+=:....:=+********************************************=-....:-********************
*****************+-....:-+***********************************************+=:...:=+******************
****************+:....:=***************************************************+-::-+*******************
***************=:...:-+*******************************************************+*********************
**************=:....-+*************************************************************+++**************
*************+:. .:=+*******+=::::--+***=::::::::::::::::::::::::::::-+*******=-::......:-=+********
************+-.  :-*********+-    .:+**+-..                         .:=****+-...          ..:-+*****
************=....-+*********+-    .:+**+-.............   ............:=**+=:.    .......     .:=****
***********+-...:=**********+-    .:+***=---------::..   ..:-------:--+**=..   ..:--=---:.. ..-=****
***********=:  .-+**********+-    .:+*************+=..   .-=************+-.. ..:=+******+=-:-=******
**********+-...:=***********+-    .:+**************=:.   .-+************=:   ..-***********+********
**********+:...-+***********+-    .:+**************=:.   .-+************=:   ..:=*******************
**********=:...-************+-    .:+**************=:.   .-+************+-..   ..:=+****************
*********+=....-************+-    .:+**************=:.   .-+*************=:..    ...:--=++**********
*********+=....-************+-    .:+**************=:.   .-+**************+-...      ...::-=+*******
**********=:...-************+-    .:+**************=:.   .-+****************+-:...      ....:=+*****
**********=:...-************+-    .:+**************=:.   .-+*******************+=-::...     ..:=****
**********+:...:+***********+-    .:+**************=:.   .-+************************+=:...   ..-+***
**********+-...:=***********+-    .:+**************=:.   .-+***************************+-..    :=***
***********=:...:+**********+-    .:+**************=:.   .-+****************************+-.    :=***
***********+-....=**********+-    .:+**************=:.   .-+************+=--=***********+-.    :=***
************=:...:=*********+-    .:+**************=:.   .-+***********=:....:-++*****+=-..  ..-+***
************+=:. .-+********+-    .:+**************=:.   .-+**********+-..  ....:::::::...   .:=****
*************+-. ..-+*******+-    .:+**************=:.   .-+***********+-:..   .........    .:+*****
**************+-....-+******+-.....:+**************=:.....-+*************+=:..............::=*******
***************+-....:=*****+=----==***************+==---=+*****************+=--::::::--==+*********
*****************-:...:-+***************************************************************************
******************=:....:=+*************************************************************************
*******************+-:....:=+***********************************************************************
*********************+-.....:-+*********************************************************************
***********************=-......-=+******************************************************************
*************************=-:.. ...:-=+***********************+++************************************
***************************+=-:.......:--==+++++++++++++==--::::=+**********************************
******************************+=-::.........:::::::::::.....  ..-+**********************************
**********************************+==-:...... ......    ....:--=+***********************************
***************************************+++==--:::::::---==++****************************************
****************************************************************************************************
 ************************************************************************************************** 
  ************************************************************************************************  
    ********************************************************************************************    
      ****************************************************************************************      
         **********************************************************************************         
                                                                                                """



class ShellApp:
    def __init__(self, root):
        #root.tk.call('tk', 'scaling', 2.0)

        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()

        window_width = int(screen_width * 0.7)
        window_height = int(screen_height * 0.55)

        x_position = (screen_width - window_width) // 2
        y_position = (screen_height - window_height) // 2

        root.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")

        self.root = root
        self.root.title("ITS Tools 🕺🪩")
        self.root.configure(bg="#2B2D30")

        icon = PhotoImage(file="./src/img/ico.png")
        root.iconphoto(True, icon)

        self.style = ttk.Style()
        self.style.configure(
            "TButton",
            font=("Arial", 12),
            padding=10,
            background="#57965C",
            foreground="black",
            relief="flat",
        )
        self.style.map("TButton", background=[("active", "#45A049")])

        self.output_text = ScrolledText(
            root,
            wrap=tk.WORD,
            height=30,
            width=90,
            font=("Consolas", 13, "bold"),
            bg="#202020",
            fg="#333333",
            borderwidth=0,
            relief="flat",
        )

        self.output_text = ScrolledText(root, wrap=tk.WORD, height=30, width=90, state=tk.NORMAL)
        self.output_text.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        self.output_text.bind("<Return>", self.execute_from_shell)
        self.output_text.bind("<BackSpace>", self.prevent_prompt_delete)
        self.output_text.bind("<Key>", self.prevent_edit)

        self.prompt = f"PS {os.getcwd()}> "
        self.output_text.insert(tk.END, self.prompt)
        self.output_text.mark_set("input_start", tk.END)

        button_frame = tk.Frame(root, bg="#2B2D30")
        button_frame.pack(padx=10, pady=10)

        commands = [
            ("CHK", "CHKDSK /F /R" if subprocess.os.name == "nt" else "fsck -f"),
            ("SFC", "sfc /scannow"),
            ("DISM", "DISM /Online /Cleanup-Image /RestoreHealth"),
            ("Change Wallpaper",
             lambda: change_wallpaper(os.path.abspath("C:/Users/Theo/PycharmProjects/ITSTools/src/img/wallpaper.jpg"))),
            ("(Acronis)", "whoami"),
            ("SFC", "whoami"),
            ("[HORUS]", "whoami"),
            ("IPCONFIG", "ipconfig /all" if subprocess.os.name == "nt" else "ifconfig -a"),
            ("PRIVATE NETWORK", "Get-NetConnectionProfile | Set-NetConnectionProfile -NetworkCategory Private"),
            ("Opti Interface", "whoami"),
            ("Déploiement Atera", "whoami"),
            ("Pare-feu Brother", "whoami"),
        ]

        cols = 6

        for index, (label, command) in enumerate(commands):
            row = index // cols
            col = index % cols
            btn = ttk.Button(button_frame, text=label, command=lambda cmd=command: self.execute_command(cmd))
            btn.grid(row=row, column=col, padx=5, pady=5)

    def execute_command(self, command):
        self.output_text.insert(tk.END, f"{command}\n")
        self.run_shell_command(command)

    def execute_from_shell(self, event):
        user_input = self.output_text.get("input_start", tk.END).strip()
        if not user_input:
            return "break"

        self.output_text.insert(tk.END, "\n")
        self.run_shell_command(user_input)
        return "break"

    def run_shell_command(self, command):
        try:
            process = subprocess.Popen(
                command, shell=True, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
            )
            stdout, stderr = process.communicate()

            if stdout:
                self.output_text.insert(tk.END, stdout)
            if stderr:
                self.output_text.insert(tk.END, stderr)
        except Exception as e:
            self.output_text.insert(tk.END, f"Erreur: {e}\n")

        self.output_text.insert(tk.END, f"\n{self.prompt}")
        self.output_text.mark_set("input_start", tk.END)
        self.output_text.see(tk.END)

    def prevent_prompt_delete(self, event):
        if self.output_text.index(tk.INSERT) < self.output_text.index("input_start"):
            return "break"
        return None

    def prevent_edit(self, event):
        if self.output_text.index(tk.INSERT) < self.output_text.index("input_start"):
            return "break"
        return None


def change_wallpaper(image_path):
    spi_setdeskwallpaper = 20
    spif_updateinifile = 0x01
    spif_sendwininichange = 0x02

    try:
        ctypes.windll.user32.SystemParametersInfoW(spi_setdeskwallpaper, 0, image_path,
                                                   spif_updateinifile | spif_sendwininichange)
        print(f"Succesfully changed wallpaper")
        return True
    except Exception as e:
        print(f"Error changing wallpaper: {e}")
        return False



def set_dpi_aware():
    ctypes.windll.shcore.SetProcessDpiAwareness(1)

set_dpi_aware()

if __name__ == "__main__":
    root = tk.Tk()
    app = ShellApp(root)
    root.mainloop()

