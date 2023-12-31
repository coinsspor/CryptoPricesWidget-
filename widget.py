import tkinter as tk
import tkinter.simpledialog
import tkinter.messagebox
import tkinter.filedialog
import requests
import threading
import pygame
import ssl

class CryptoPriceWidget:
    def __init__(self, root):
        self.root = root
        self.root.title("Crypto Prices Widget by coinsspor")
        self.refresh_rate = 5  # Default refresh rate
        self.font_size = 25  # Default font size
        self.root.configure(bg='black')  # Set background color of the window to black
        self.cryptos = {'BTC': None, 'MINA': None}  # Default cryptos
        self.alarms = {}  # Alarms
        self.alarm_sounds = {'upper': None, 'lower': None}  # Alarm sounds for upper and lower limits
        self.alarm_duration = 5  # Default alarm duration in seconds
        self.selected_source = 'Mexc'  # Default data source
        self.available_sources = ['Mexc', 'Binance', 'OKX', 'Kraken']

        pygame.init()
        self.label_style = {'font': ("Arial", self.font_size), 'bg': 'black', 'fg': 'yellow'}
        self.create_widgets()
        self.create_menu()
        self.update_prices()

    def create_widgets(self):
        self.labels = {}
        for crypto in self.cryptos:
            self.labels[crypto] = tk.Label(self.root, text=f"Loading {crypto}/USDT Price...", **self.label_style)
            self.labels[crypto].pack(pady=10)

    def create_menu(self):
        menu_bar = tk.Menu(self.root)
        self.root.config(menu=menu_bar)

        settings_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Settings", menu=settings_menu)

        self.always_on_top = tk.BooleanVar()
        settings_menu.add_checkbutton(label="Always on Top", onvalue=1, offvalue=0, 
                                      variable=self.always_on_top, command=self.toggle_always_on_top)

        settings_menu.add_command(label="Set Refresh Rate", command=self.set_refresh_rate)
        settings_menu.add_command(label="Set Font Size", command=self.set_font_size)
        settings_menu.add_command(label="Manage Cryptos", command=self.manage_cryptos)
        settings_menu.add_command(label="Select Data Source", command=self.select_data_source)

        alarm_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Alarms", menu=alarm_menu)
        alarm_menu.add_command(label="Manage Alarms", command=self.manage_alarms)

    def select_data_source(self):
        source_win = tk.Toplevel(self.root)
        source_win.title("Select Data Source")
        source_win.configure(bg='black')

        tk.Label(source_win, text="Select a data source:", bg='black', fg='yellow').pack(pady=(10, 0))

        self.source_var = tk.StringVar(value=self.selected_source)
        for source in self.available_sources:
            b = tk.Radiobutton(source_win, text=source, variable=self.source_var, 
                               value=source, bg='black', fg='yellow', command=self.update_data_source)
            b.pack(anchor=tk.W)

    def update_data_source(self):
        self.selected_source = self.source_var.get()
        self.update_prices()

    def set_refresh_rate(self):
        new_rate = tkinter.simpledialog.askinteger("Set Refresh Rate", "Enter refresh rate (seconds):", parent=self.root)
        if new_rate and new_rate > 0:
            self.refresh_rate = new_rate

    def set_font_size(self):
        new_size = tkinter.simpledialog.askinteger("Set Font Size", "Enter font size:", parent=self.root)
        if new_size and new_size > 0:
            self.font_size = new_size
            for label in self.labels.values():
                label.config(font=("Arial", self.font_size))

    def toggle_always_on_top(self):
        self.root.attributes("-topmost", self.always_on_top.get())

    def manage_cryptos(self):
        manage_win = tk.Toplevel(self.root)
        manage_win.title("Manage Cryptos")
        manage_win.configure(bg='black')

        tk.Label(manage_win, text="Enter crypto symbol (e.g., BTC):", bg='black', fg='yellow').pack(pady=(10, 0))

        self.crypto_entry = tk.Entry(manage_win)
        self.crypto_entry.pack(pady=10)

        add_button = tk.Button(manage_win, text="Add Crypto", command=self.add_crypto)
        add_button.pack(pady=(0, 10))
        remove_button = tk.Button(manage_win, text="Remove Crypto", command=self.remove_crypto)
        remove_button.pack(pady=10)

    def add_crypto(self):
        symbol = self.crypto_entry.get().upper()
        if symbol and symbol not in self.cryptos:
            self.cryptos[symbol] = None
            self.labels[symbol] = tk.Label(self.root, text=f"Loading {symbol}/USDT Price...", **self.label_style)
            self.labels[symbol].pack(pady=10)
            self.update_prices()

    def remove_crypto(self):
        symbol = self.crypto_entry.get().upper()
        if symbol in self.cryptos:
            del self.cryptos[symbol]
            self.labels[symbol].pack_forget()
            del self.labels[symbol]

    def manage_alarms(self):
        alarm_win = tk.Toplevel(self.root)
        alarm_win.title("Manage Alarms")
        alarm_win.configure(bg='black')

        row = 0
        for crypto in self.cryptos:
            tk.Label(alarm_win, text=crypto, bg='black', fg='yellow').grid(row=row, column=0, padx=10, pady=5)

            tk.Label(alarm_win, text="Upper limit:", bg='black', fg='yellow').grid(row=row, column=1, padx=10, pady=5)
            upper_limit_var = tk.StringVar(value=self.alarms.get(crypto, {}).get('upper', ''))
            tk.Entry(alarm_win, textvariable=upper_limit_var).grid(row=row, column=2, padx=10, pady=5)

            tk.Label(alarm_win, text="Lower limit:", bg='black', fg='yellow').grid(row=row, column=3, padx=10, pady=5)
            lower_limit_var = tk.StringVar(value=self.alarms.get(crypto, {}).get('lower', ''))
            tk.Entry(alarm_win, textvariable=lower_limit_var).grid(row=row, column=4, padx=10, pady=5)

            set_button = tk.Button(alarm_win, text="Set Alarm", command=lambda c=crypto, u=upper_limit_var, l=lower_limit_var: self.set_alarm(c, u.get(), l.get()))
            set_button.grid(row=row, column=5, padx=10, pady=5)

            delete_button = tk.Button(alarm_win, text="Delete Alarm", command=lambda c=crypto: self.delete_alarm(c))
            delete_button.grid(row=row, column=6, padx=10, pady=5)

            row += 1

        # Alarm sound selections
        row += 1
        tk.Label(alarm_win, text="Upper Limit Alarm Sound:", bg='black', fg='yellow').grid(row=row, column=0, padx=10, pady=5)
        upper_sound_button = tk.Button(alarm_win, text="Select Sound for Upper Limit", command=lambda: self.select_alarm_sound('upper'))
        upper_sound_button.grid(row=row, column=1, padx=10, pady=5, columnspan=2)

        row += 1
        tk.Label(alarm_win, text="Lower Limit Alarm Sound:", bg='black', fg='yellow').grid(row=row, column=0, padx=10, pady=5)
        lower_sound_button = tk.Button(alarm_win, text="Select Sound for Lower Limit", command=lambda: self.select_alarm_sound('lower'))
        lower_sound_button.grid(row=row, column=1, padx=10, pady=5, columnspan=2)

        # Duration settings
        row += 1
        tk.Label(alarm_win, text="Duration (seconds):", bg='black', fg='yellow').grid(row=row, column=0, padx=10, pady=5)
        duration_var = tk.StringVar(value=str(self.alarm_duration))
        duration_entry = tk.Entry(alarm_win, textvariable=duration_var)
        duration_entry.grid(row=row, column=1, padx=10, pady=5)

        save_button = tk.Button(alarm_win, text="Save Settings", command=lambda d=duration_var: self.save_alarm_settings(d.get()))
        save_button.grid(row=row, column=2, padx=10, pady=5, columnspan=2)
    # ... (Birinci parçanın devamı)

    def set_alarm(self, crypto, upper, lower):
        try:
            upper = float(upper) if upper else None
            lower = float(lower) if lower else None
            if crypto not in self.alarms:
                self.alarms[crypto] = {}
            self.alarms[crypto]['upper'] = upper
            self.alarms[crypto]['lower'] = lower
            tkinter.messagebox.showinfo("Alarm Set", f"Alarm for {crypto} set.")
        except ValueError:
            tkinter.messagebox.showerror("Error", "Please enter a valid number.")

    def delete_alarm(self, crypto):
        if crypto in self.alarms:
            del self.alarms[crypto]
            tkinter.messagebox.showinfo("Alarm Deleted", f"Alarm for {crypto} deleted.")

    def select_alarm_sound(self, alarm_type):
        filename = tkinter.filedialog.askopenfilename(title=f"Select Sound for {alarm_type.capitalize()} Limit Alarm", filetypes=[("Audio Files", "*.wav *.mp3")])
        if filename:
            self.alarm_sounds[alarm_type] = filename

    def save_alarm_settings(self, duration):
        try:
            self.alarm_duration = int(duration)
        except ValueError:
            tkinter.messagebox.showerror("Error", "Please enter a valid number for duration.")

    def get_current_price(self, symbol):
        try:
            if self.selected_source == 'Mexc':
                url = f"https://www.mexc.com/open/api/v2/market/ticker?symbol={symbol}_USDT"
            elif self.selected_source == 'Binance':
                url = f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}USDT"
            elif self.selected_source == 'OKX':
                url = f"https://www.okx.com/api/spot/v3/instruments/{symbol}-USDT/ticker"
            elif self.selected_source == 'Kraken':
                url = f"https://api.kraken.com/0/public/Ticker?pair={symbol}USD"

            response = requests.get(url)
            data = response.json()

            if self.selected_source in ['Mexc', 'Binance']:
                return float(data['data'][0]['last']) if self.selected_source == 'Mexc' else float(data['price'])
            elif self.selected_source == 'OKX':
                return float(data['last'])
            elif self.selected_source == 'Kraken':
                return float(data['result'][list(data['result'].keys())[0]]['c'][0])

        except Exception as e:
            print(f"Error fetching price for {symbol}: {e}")
            return None

    def update_prices(self):
        if hasattr(self, 'timer'):
            self.timer.cancel()

        for symbol in self.cryptos.keys():
            price = self.get_current_price(symbol)
            if price:
                display_price = f"{symbol}/USDT: ${price:.4f}" if symbol != 'BTC' else f"{symbol}/USDT: ${int(price)}"
                self.labels[symbol].config(text=display_price)

        self.check_alarms()
        self.timer = threading.Timer(self.refresh_rate, self.update_prices)
        self.timer.start()

    def check_alarms(self):
        for crypto, alarm in self.alarms.items():
            current_price = self.get_current_price(crypto)
            if current_price:
                if 'upper' in alarm and alarm['upper'] and current_price >= alarm['upper']:
                    self.play_alarm(self.alarm_sounds['upper'])
                    tkinter.messagebox.showinfo("Price Alert", f"{crypto} has reached the upper limit of {alarm['upper']}")
                if 'lower' in alarm and alarm['lower'] and current_price <= alarm['lower']:
                    self.play_alarm(self.alarm_sounds['lower'])
                    tkinter.messagebox.showinfo("Price Alert", f"{crypto} has reached the lower limit of {alarm['lower']}")

    def play_alarm(self, sound_file):
        if sound_file:
            try:
                pygame.mixer.music.load(sound_file)
                pygame.mixer.music.play()
                threading.Timer(self.alarm_duration, pygame.mixer.music.stop).start()
            except Exception as e:
                print(f"Error playing alarm sound: {e}")

def main():
    root = tk.Tk()
    app = CryptoPriceWidget(root)
    root.mainloop()

if __name__ == "__main__":
    main()
