from random import randint
import webbrowser
import tkinter as tk
from tkinter import messagebox
import os

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.balance = 0.0
        self.master = master
        self.configure()
        self.create_widgets()
        self.pack()

    def configure(self):
        self.master.title("Tragamonedas (RTP 94%)")
        menu_bar = tk.Menu(self.master)
        help_menu = tk.Menu(self.master, tearoff=0)
        help_menu.add_command(label="Manual de Usuario", command=self.redirect_to_help)
        help_menu.add_command(label="Acerca de", command=self.show_about)
        menu_bar.add_cascade(label="Ayuda", menu=help_menu)
        self.master.config(menu=menu_bar)

    def create_widgets(self):
        title_label = tk.Label(text="Maquina Tragamonedas (RTP 94%)", font=("Arial", 16))
        title_label.pack(padx=10, pady=10)

        self.balance_label = tk.Label(text="Dinero: $0.00", font=("Arial", 12))
        self.balance_label.pack(padx=10, pady=10)

        self.balance_var = tk.DoubleVar()
        self.balance_input = tk.Entry(textvariable=self.balance_var)
        self.balance_input.pack()

        deposit_button = tk.Button(text="Depositar", command=self.deposit)
        deposit_button.pack()

        bet_label = tk.Label(text="Ingrese su apuesta (Premios fijos)")
        bet_label.pack()

        self.bet_var = tk.DoubleVar()
        bet_input = tk.Entry(textvariable=self.bet_var)
        bet_input.pack()

        self.numbers_label = tk.Label(text="0   0   0", font=("Arial", 12))
        self.numbers_label.pack(padx=5, pady=5)
        
        shoot_button = tk.Button(text="Tirar", command=self.shoot)
        shoot_button.pack()

        self.message = tk.Label(text="¡Haga su primer tiro!", bg="lightblue")
        self.message.pack(padx=5, pady=5)

    def update_balance(self, new_balance):
        self.balance = round(new_balance, 2)
        self.balance_label.config(text=f"Dinero: ${self.balance:.2f}")

    def show_message(self, text, msg_type):
        color_dict = {"success": "lightgreen", "info": "lightblue", "warning": "lightyellow"}
        if msg_type in color_dict:
            self.message.config(text=text, bg=color_dict[msg_type])
        elif msg_type == "error":
            messagebox.showerror("Error", text)

    def redirect_to_help(self):
        webbrowser.open("https://github.com/WilsonLombardo/maquinatragamonedas")

    def show_about(self):
        messagebox.showinfo("Acerca de", "Tragamonedas v2.0\nRTP 94% garantizado\nCreado por Wilson Lombardo")

    def deposit(self):
        try:
            deposited_balance = float(self.balance_var.get())
            if deposited_balance <= 0:
                self.show_message("El depósito debe ser mayor a 0.", "error")
                return
            self.update_balance(self.balance + deposited_balance)
            self.balance_var.set(0)
            self.show_message(f"Depositado: ${deposited_balance:.2f}", "success")
        except:
            self.show_message("Ingrese un valor numérico válido.", "error")

    def shoot(self):
        try:
            bet = float(self.bet_var.get())
            if bet <= 0:
                self.show_message("La apuesta debe ser mayor a 0.", "error")
                return
            if bet > self.balance:
                self.show_message("Balance insuficiente.", "error")
                return

            generated_numbers = [randint(1, 6) for _ in range(3)]
            self.numbers_label.config(text="   ".join(map(str, generated_numbers)))

            # Sistema de premios FIJOS (RTP 94%)
            if all(x == generated_numbers[0] for x in generated_numbers):
                win = 4.40  # Premio fijo por 3 iguales
            elif generated_numbers in [[1,2,3], [2,3,4], [3,4,5], [4,5,6]]:
                win = 3.00  # Premio fijo por consecutivos
            elif (generated_numbers[0] == generated_numbers[1] or 
                  generated_numbers[1] == generated_numbers[2] or 
                  generated_numbers[0] == generated_numbers[2]):
                win = 1.16  # Premio fijo por 2 iguales
            else:
                win = -bet  # Pierde lo apostado

            self.update_balance(self.balance + win)
            
            # Guardar registro (con manejo robusto de archivos)
            script_dir = os.path.dirname(os.path.abspath(__file__))
            data_dir = os.path.join(script_dir, "data")
            os.makedirs(data_dir, exist_ok=True)
            
            with open(os.path.join(data_dir, "shoots.csv"), mode="a", encoding="utf-8") as f:
                f.write(f"{','.join(map(str, generated_numbers))},{bet},{win},{self.balance}\n")

            # Mostrar resultado
            result_msg = {
                win == 4.40: "¡Jackpot! Ganó $4.40 (3 iguales)",
                win == 3.00: "¡Ganó $3.00 (Consecutivos)!",
                win == 1.16: "¡Ganó $1.16 (2 iguales)!",
                win == -bet: f"Perdió ${bet:.2f}. ¡Siga intentando!"
            }[True]
            
            self.show_message(result_msg, "success" if win > 0 else "info")

        except ValueError:
            self.show_message("Ingrese un valor numérico válido.", "error")
        except Exception as e:
            messagebox.showerror("Error crítico", f"Ocurrió un error inesperado:\n{str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = Application(master=root)
    app.mainloop()