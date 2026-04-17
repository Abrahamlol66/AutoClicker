import tkinter as tk
from tkinter import ttk, messagebox
import threading
import time
import sys
from pynput.mouse import Button, Controller
from pynput.keyboard import Listener, KeyCode, Key

class AutoclickerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("AutoClicker Pro Ultra")
        self.root.geometry("400x450")
        self.root.resizable(False, False)

        # Variables de control
        self.clicking = False
        self.holding_click = False  # Nuevo estado para click mantenido
        self.cps_var = tk.StringVar(value="10")
        self.click_button_var = tk.StringVar(value="Izquierdo")
        
        # Teclas de activación
        self.start_key = KeyCode.from_vk(117)  # F6 por defecto para autoclick
        self.key_label_var = tk.StringVar(value="F6")
        self.hold_key = KeyCode.from_vk(118)   # F7 por defecto para click mantenido
        self.hold_key_label_var = tk.StringVar(value="F7")
        
        self.setting_key_type = None  # Puede ser "start" o "hold"
        self.setting_key = False

        self.mouse = Controller()
        self.click_thread = None

        self.setup_ui()
        self.start_hotkey_listener()

    def log(self, message):
        """Añade un mensaje al área de log de la UI"""
        self.log_text.config(state="normal")
        self.log_text.insert(tk.END, f"[{time.strftime('%H:%M:%S')}] {message}\n")
        self.log_text.see(tk.END)
        self.log_text.config(state="disabled")

    def setup_ui(self):
        main_frame = ttk.Frame(self.root, padding="15")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Configuración
        config_frame = ttk.LabelFrame(main_frame, text=" Configuración ", padding="10")
        config_frame.pack(fill=tk.X, pady=5)

        ttk.Label(config_frame, text="Clicks por segundo:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.cps_entry = ttk.Entry(config_frame, textvariable=self.cps_var, width=10)
        self.cps_entry.grid(row=0, column=1, sticky=tk.E, pady=5)
        ttk.Label(config_frame, text="(Máx 100)", font=("Arial", 8)).grid(row=0, column=2, padx=5)

        ttk.Label(config_frame, text="Botón del mouse:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.button_combo = ttk.Combobox(config_frame, textvariable=self.click_button_var, 
                                        values=["Izquierdo", "Derecho"], state="readonly", width=12)
        self.button_combo.grid(row=1, column=1, sticky=tk.E, pady=5)

        ttk.Label(config_frame, text="Atajo Autoclick:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.hotkey_btn = ttk.Button(config_frame, textvariable=self.key_label_var, 
                                   command=lambda: self.wait_for_key("start"), width=12)
        self.hotkey_btn.grid(row=2, column=1, sticky=tk.E, pady=5)

        ttk.Label(config_frame, text="Atajo Click Mantenido:").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.hold_hotkey_btn = ttk.Button(config_frame, textvariable=self.hold_key_label_var, 
                                        command=lambda: self.wait_for_key("hold"), width=12)
        self.hold_hotkey_btn.grid(row=3, column=1, sticky=tk.E, pady=5)

        # Botones de Control Principal
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(fill=tk.X, pady=10)

        self.toggle_btn = tk.Button(btn_frame, text="INICIAR AUTOCLICK", font=("Arial", 10, "bold"), 
                                   bg="#4CAF50", fg="white", command=self.toggle_clicking, height=2)
        self.toggle_btn.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=2)

        self.hold_btn = tk.Button(btn_frame, text="MANTENER CLICK", font=("Arial", 10, "bold"), 
                                 bg="#2196F3", fg="white", command=self.toggle_holding_click, height=2)
        self.hold_btn.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=2)

        # Estado y Logs
        self.status_label = ttk.Label(main_frame, text="Estado: DETENIDO", font=("Arial", 10, "bold"))
        self.status_label.pack(pady=5)

        self.log_text = tk.Text(main_frame, height=8, state="disabled", font=("Consolas", 9))
        self.log_text.pack(fill=tk.BOTH, expand=True, pady=5)
        
        self.log("Aplicación iniciada.")
        self.log(f"Atajos: Autoclick ({self.key_label_var.get()}), Mantenido ({self.hold_key_label_var.get()})")

    def wait_for_key(self, key_type):
        self.setting_key = True
        self.setting_key_type = key_type
        if key_type == "start":
            self.key_label_var.set("...")
        else:
            self.hold_key_label_var.set("...")
        self.log(f"Esperando nueva tecla para {key_type}...")

    def start_hotkey_listener(self):
        def on_press(key):
            if self.setting_key:
                name = ""
                if hasattr(key, 'name'): name = key.name.upper()
                elif hasattr(key, 'char'): name = key.char.upper()
                else: name = str(key).replace("Key.", "").upper()
                
                if self.setting_key_type == "start":
                    self.start_key = key
                    self.key_label_var.set(name)
                else:
                    self.hold_key = key
                    self.hold_key_label_var.set(name)
                
                self.setting_key = False
                self.log(f"Tecla {self.setting_key_type} configurada: {name}")
                return

            if key == self.start_key:
                self.root.after(0, self.toggle_clicking)
            elif key == self.hold_key:
                self.root.after(0, self.toggle_holding_click)

        listener = Listener(on_press=on_press)
        listener.daemon = True
        listener.start()

    def toggle_clicking(self):
        if self.holding_click:
            self.toggle_holding_click()

        if not self.clicking:
            try:
                cps_val = float(self.cps_var.get())
                if cps_val <= 0: raise ValueError
                if cps_val > 100:
                    messagebox.showwarning("Límite excedido", "El máximo permitido es 100 CPS por seguridad.")
                    self.cps_var.set("100")
                    cps_val = 100.0
                
                self.clicking = True
                self.status_label.config(text="Estado: AUTOCLICK", foreground="green")
                self.toggle_btn.config(text="DETENER", bg="#f44336")
                
                # Iniciar el hilo de clickeo
                self.click_thread = threading.Thread(target=self.autoclick_loop, args=(cps_val,), daemon=True)
                self.click_thread.start()
                self.log(f"Iniciado: {cps_val} CPS ({self.click_button_var.get()})")
                
            except ValueError:
                messagebox.showerror("Error", "CPS debe ser un número mayor a 0")
        else:
            self.clicking = False
            self.status_label.config(text="Estado: DETENIDO", foreground="black")
            self.toggle_btn.config(text="INICIAR AUTOCLICK", bg="#4CAF50")
            self.log("Autoclick detenido.")

    def toggle_holding_click(self):
        if self.clicking:
            self.toggle_clicking()

        button = Button.left if self.click_button_var.get() == "Izquierdo" else Button.right
        
        if not self.holding_click:
            self.holding_click = True
            self.status_label.config(text="Estado: MANTENIENDO", foreground="blue")
            self.hold_btn.config(text="SOLTAR CLICK", bg="#f44336")
            self.mouse.press(button)
            self.log(f"Click mantenido activado ({self.click_button_var.get()})")
        else:
            self.holding_click = False
            self.status_label.config(text="Estado: DETENIDO", foreground="black")
            self.hold_btn.config(text="MANTENER CLICK", bg="#2196F3")
            self.mouse.release(button)
            self.log("Click mantenido desactivado.")

    def autoclick_loop(self, cps):
        button = Button.left if self.click_button_var.get() == "Izquierdo" else Button.right
        delay = 1.0 / cps
        
        while self.clicking:
            try:
                # Simular click completo (presionar y soltar)
                self.mouse.press(button)
                self.mouse.release(button)
                time.sleep(delay)
            except Exception as e:
                self.root.after(0, lambda: self.log(f"Error: {str(e)}"))
                break
        
        self.clicking = False

if __name__ == "__main__":
    root = tk.Tk()
    app = AutoclickerApp(root)
    root.mainloop()
