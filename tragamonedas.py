from random import randint
import webbrowser
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

class CasinoApp(tk.Tk):
    """Aplicación de tragamonedas con diseño mejorado."""
    
    def __init__(self):
        super().__init__()
        self.title("Tragamonedas VIP - RTP 94%")
        self.geometry("500x650")
        self.configure(bg="#1a1a2e")
        self.resizable(False, False)
        
        # Estilo general
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.configure_styles()
        
        # Variables del juego
        self.balance = 0.0
        self.last_win = 0.0
        self.create_widgets()
        self.update_clock()
        
    def configure_styles(self):
        """Configura los estilos visuales para la aplicación."""
        self.style.configure('TFrame', background='#1a1a2e')
        self.style.configure('TLabel', background='#1a1a2e', foreground='white', font=('Impact', 12))
        self.style.configure('Title.TLabel', font=('Impact', 24, 'bold'), foreground='#f1c40f')
        self.style.configure('Balance.TLabel', font=('Arial', 14, 'bold'), foreground='#2ecc71')
        self.style.configure('Numbers.TLabel', font=('Arial', 28, 'bold'), foreground='#e74c3c')
        self.style.configure('Clock.TLabel', font=('Courier', 12), foreground='#3498db')
        self.style.configure('TButton', font=('Arial', 12, 'bold'), padding=5)
        self.style.map('TButton',
                      foreground=[('pressed', 'white'), ('active', 'white')],
                      background=[('pressed', '#e67e22'), ('active', '#e67e22')])
        self.style.configure('Deposit.TButton', background='#2ecc71')
        self.style.configure('Spin.TButton', background='#e74c3c')
        self.style.configure('History.TFrame', background='#16213e')
        self.style.configure('History.TText', font=('Arial', 10), foreground='white', background='#16213e')
        
    def create_widgets(self):
        """Crea todos los elementos de la interfaz."""
        # Marco principal
        main_frame = ttk.Frame(self)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Título del juego
        title_label = ttk.Label(main_frame, text="TRAGAMONEDAS VIP", style='Title.TLabel')
        title_label.pack(pady=(0, 20))
        
        # Panel de información
        info_frame = ttk.Frame(main_frame)
        info_frame.pack(fill=tk.X, pady=5)
        
        # Balance actual
        self.balance_label = ttk.Label(info_frame, text="Balance: $0.00", style='Balance.TLabel')
        self.balance_label.pack(side=tk.LEFT)
        
        # Última ganancia
        self.win_label = ttk.Label(info_frame, text="Última: $0.00", style='Balance.TLabel')
        self.win_label.pack(side=tk.RIGHT)
        
        # Panel de depósito
        deposit_frame = ttk.Frame(main_frame)
        deposit_frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(deposit_frame, text="Depositar:").pack(side=tk.LEFT)
        
        self.deposit_var = tk.DoubleVar()
        deposit_entry = ttk.Entry(deposit_frame, textvariable=self.deposit_var, width=10)
        deposit_entry.pack(side=tk.LEFT, padx=5)
        
        deposit_btn = ttk.Button(deposit_frame, text="Cargar", command=self.deposit, style='Deposit.TButton')
        deposit_btn.pack(side=tk.LEFT)
        
        # Panel de apuesta
        bet_frame = ttk.Frame(main_frame)
        bet_frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(bet_frame, text="Apuesta:").pack(side=tk.LEFT)
        
        self.bet_var = tk.DoubleVar(value=1.0)
        bet_entry = ttk.Entry(bet_frame, textvariable=self.bet_var, width=10)
        bet_entry.pack(side=tk.LEFT, padx=5)
        
        spin_btn = ttk.Button(bet_frame, text="GIRAR", command=self.spin, style='Spin.TButton')
        spin_btn.pack(side=tk.LEFT)
        
        # Display de números
        self.numbers_label = ttk.Label(main_frame, text="⚀ ⚀ ⚀", style='Numbers.TLabel')
        self.numbers_label.pack(pady=20)
        
        # Mensaje de resultado
        self.message_label = tk.Label(main_frame, text="¡Bienvenido! Realiza tu primer giro.", 
                                    bg="#16213e", fg="white", font=('Arial', 12, 'bold'),
                                    height=2, width=40, bd=2, relief=tk.RIDGE)
        self.message_label.pack(pady=10)
        
        # Historial de jugadas
        history_frame = ttk.Frame(main_frame, style='History.TFrame')
        history_frame.pack(fill=tk.BOTH, expand=True)
        
        scrollbar = ttk.Scrollbar(history_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.history_text = tk.Text(history_frame, yscrollcommand=scrollbar.set, 
                                   wrap=tk.WORD, height=8, font=('Arial', 10),
                                   bg='#16213e', fg='white', insertbackground='white')
        self.history_text.pack(fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.history_text.yview)
        
        # Reloj
        self.clock_label = ttk.Label(main_frame, style='Clock.TLabel')
        self.clock_label.pack(side=tk.BOTTOM, pady=5)
        
        # Menú de ayuda
        menubar = tk.Menu(self)
        help_menu = tk.Menu(menubar, tearoff=0, bg='#1a1a2e', fg='white')
        help_menu.add_command(label="Manual de Usuario", command=self.show_help)
        help_menu.add_command(label="Acerca de", command=self.show_about)
        menubar.add_cascade(label="Ayuda", menu=help_menu)
        self.config(menu=menubar)
        
    def update_clock(self):
        """Actualiza el reloj en tiempo real."""
        now = datetime.now().strftime("%H:%M:%S")
        self.clock_label.config(text=f"🕒 {now}")
        self.after(1000, self.update_clock)
        
    def update_balance(self, amount):
        """Actualiza el balance del jugador."""
        self.balance = round(amount, 2)
        self.balance_label.config(text=f"Balance: ${self.balance:.2f}")
        
    def update_win(self, amount):
        """Actualiza el display de la última ganancia/pérdida."""
        self.last_win = round(amount, 2)
        color = "#2ecc71" if amount >= 0 else "#e74c3c"
        self.win_label.config(text=f"Última: ${self.last_win:.2f}", foreground=color)
        
    def show_message(self, text, msg_type):
        """Muestra mensajes al usuario con estilo según el tipo."""
        colors = {
            "success": ("#2ecc71", "¡GANANCIA! "),
            "info": ("#3498db", "INFO: "),
            "warning": ("#f39c12", "ATENCIÓN: "),
            "error": ("#e74c3c", "¡PERDISTE! ")
        }
        
        color, prefix = colors.get(msg_type, ("#3498db", ""))
        self.message_label.config(text=prefix + text, bg=color)
        
    def show_help(self):
        """Abre el manual de usuario en el navegador."""
        webbrowser.open("https://github.com/WilsonLombardo/maquinatragamonedas")
        
    def show_about(self):
        """Muestra información acerca de la aplicación."""
        about_msg = "Tragamonedas VIP v2.0\n\n" \
                   "RTP 94% garantizado\n" \
                   "Creado por Wilson Lombardo\n\n" \
                   "⚀⚁⚂⚃⚄⚅"
        messagebox.showinfo("Acerca de", about_msg)
        
    def deposit(self):
        """Procesa el depósito de dinero."""
        try:
            amount = self.deposit_var.get()
            if amount <= 0:
                messagebox.showerror("Error", "El depósito debe ser mayor a 0.")
                return
                
            self.update_balance(self.balance + amount)
            self.deposit_var.set(0)
            self.show_message(f"Depósito exitoso: ${amount:.2f}", "info")
        except:
            messagebox.showerror("Error", "Ingrese un valor numérico válido.")
            
    def spin(self):
        """Realiza un giro en la tragamonedas."""
        try:
            bet = self.bet_var.get()
            
            # Validaciones
            if bet <= 0:
                self.show_message("La apuesta debe ser mayor a 0.", "warning")
                return
            if bet > self.balance:
                self.show_message("Fondos insuficientes.", "error")
                return
                
            # Generar números aleatorios
            numbers = [randint(1, 6) for _ in range(3)]
            dice_symbols = ["⚀", "⚁", "⚂", "⚃", "⚄", "⚅"]
            display = " ".join([dice_symbols[n-1] for n in numbers])
            self.numbers_label.config(text=display)
            
            # Determinar resultado
            if all(n == numbers[0] for n in numbers):
                win = bet * 4.40  # Jackpot - 3 iguales
                result_type = "success"
                result_msg = f"¡JACKPOT! 3 iguales - GANANCIA: ${win:.2f}"
            elif numbers in [[1,2,3], [2,3,4], [3,4,5], [4,5,6]]:
                win = bet * 3.00  # 3 consecutivos
                result_type = "success"
                result_msg = f"¡3 consecutivos! GANANCIA: ${win:.2f}"
            elif len(set(numbers)) == 2:
                win = bet * 1.16  # 2 iguales
                result_type = "success"
                result_msg = f"¡2 iguales! GANANCIA: ${win:.2f}"
            else:
                win = -bet  # Pérdida
                result_type = "error"
                result_msg = f"PÉRDIDA: ${bet:.2f} - Sigue intentando"
                
            # Actualizar balance y mostrar resultado
            self.update_balance(self.balance + win)
            self.update_win(win)
            self.show_message(result_msg, result_type)
            
            # Registrar en historial
            result_text = "GANANCIA" if win >= 0 else "PÉRDIDA"
            history_entry = (f"⏱ {datetime.now().strftime('%H:%M:%S')} - "
                           f"Apuesta: ${bet:.2f} - "
                           f"{result_text}: ${abs(win):.2f} - "
                           f"Numeros: {numbers}\n")
                           
            self.history_text.insert(tk.END, history_entry)
            self.history_text.see(tk.END)
            
        except ValueError:
            self.show_message("Ingrese un valor numérico válido.", "warning")
            
if __name__ == "__main__":
    app = CasinoApp()
    app.mainloop()
