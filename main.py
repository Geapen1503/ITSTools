import sys
import tkinter as tk
from tkinter import ttk
from tkinter import PhotoImage
from tkinter.scrolledtext import ScrolledText
import subprocess
import os
import ctypes
import threading


class PasswordPrompt:
    def __init__(self, root, callback):
        self.root = root
        self.callback = callback
        self.root.title("Mot de passe requis")
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        window_width = int(screen_width * 0.2)
        window_height = int(screen_height * 0.15)
        x_position = (screen_width - window_width) // 2
        y_position = (screen_height - window_height) // 2
        root.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")
        self.root.resizable(False, False)
        self.root.configure(bg="#2B2D30")
        self.label = ttk.Label(self.root, text="Entrez le mot de passe :", font=("Arial", 12))
        self.label.pack(pady=10)
        icon_path = resource_path("img/ico.png")
        icon = PhotoImage(file=icon_path)
        root.iconphoto(True, icon)
        self.password_entry = ttk.Entry(self.root, show="*", font=("Arial", 12))
        self.password_entry.pack(pady=5, padx=10, fill=tk.X)
        self.submit_button = ttk.Button(self.root, text="Valider", command=self.check_password)
        self.submit_button.pack(pady=10)

    def check_password(self):
        password = self.password_entry.get()
        if password == "root":
            self.root.destroy()
            self.callback()
        else:
            self.label.config(text="Mot de passe incorrect. Réessayez.", foreground="red")


class ShellApp:
    def __init__(self, root):
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        window_width = int(screen_width * 0.7)
        window_height = int(screen_height * 0.56)
        x_position = (screen_width - window_width) // 2
        y_position = (screen_height - window_height) // 2
        root.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")
        self.root = root
        self.root.title("ITS Tools 🕺🪩")
        self.root.configure(bg="#2B2D30")
        icon_path = resource_path("img/ico.png")
        icon = PhotoImage(file=icon_path)
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
            ("Change Wallpaper", lambda: change_wallpaper(resource_path("img/wallpaper.jpg"))),
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
        self.loading_label = tk.Label(root, text="", font=("Arial", 12), bg="#2B2D30", fg="white")
        self.loading_label.pack(pady=5)
        self.loading_animation = None
        self.animation_running = False

    def execute_command(self, command):
        self.output_text.insert(tk.END, f"{command}\n")
        self.start_loading_animation()
        self.root.update_idletasks()
        self.run_shell_command(command)

    def run_shell_command(self, command):
        def execute():
            try:
                process = subprocess.Popen(
                    command,
                    shell=True,
                    text=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    creationflags=subprocess.CREATE_NO_WINDOW
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
            self.stop_loading_animation()

        threading.Thread(target=execute, daemon=True).start()

    def start_loading_animation(self):
        self.animation_running = True
        self.loading_text = ["", ".", "..", "..."]
        self.loading_index = 0

        def animate():
            if not self.animation_running:
                return
            self.loading_label.config(text=f"Exécution en cours{self.loading_text[self.loading_index]}")
            self.loading_index = (self.loading_index + 1) % len(self.loading_text)
            self.loading_animation = self.root.after(500, animate)

        animate()

    def stop_loading_animation(self):
        self.animation_running = False
        if self.loading_animation:
            self.root.after_cancel(self.loading_animation)
            self.loading_animation = None
        self.loading_label.config(text="")

    def execute_from_shell(self, event):
        user_input = self.output_text.get("input_start", tk.END).strip()
        if not user_input:
            return "break"
        self.output_text.insert(tk.END, "\n")
        self.run_shell_command(user_input)
        return "break"

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
        return True
    except:
        return False


def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


def run_as_admin():
    if not is_admin():
        try:
            ctypes.windll.shell32.ShellExecuteW(
                None, "runas", sys.executable, " ".join(sys.argv), None, 1
            )
        except:
            pass
        sys.exit()


def set_dpi_aware():
    ctypes.windll.shcore.SetProcessDpiAwareness(1)


def main():
    def launch_shell():
        root = tk.Tk()
        app = ShellApp(root)
        root.mainloop()

    password_root = tk.Tk()
    PasswordPrompt(password_root, launch_shell)
    password_root.mainloop()


run_as_admin()
set_dpi_aware()

if __name__ == "__main__":
    main()
