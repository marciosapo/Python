import tkinter as tk
import pyautogui
import pygetwindow as gw
import win32gui
import win32con
from tkinter import messagebox, filedialog
from tkinter import ttk
import pytesseract
from PIL import Image
import mss
from playsound import playsound

# Configure Tesseract path (update if needed)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

data_array = []  # Array for keys to press
isRunning = False
delay_time = 500
sound_file = None  # Path to the sound file

def choose_sound_file():
    """Open a file dialog to select a sound file."""
    global sound_file
    file_path = filedialog.askopenfilename(
        title="Choose a Sound File",
        filetypes=(("Audio Files", "*.mp3 *.wav"), ("All Files", "*.*"))
    )
    if file_path:
        sound_file = file_path
        sound_label.config(text=f"Selected Sound: {file_path}")
        messagebox.showinfo("Sound Selected", f"Selected sound file: {file_path}")
    else:
        messagebox.showinfo("No File Selected", "No sound file was chosen.")

def focus_window(window_title):
    window = gw.getWindowsWithTitle(window_title)
    if window:
        win32gui.ShowWindow(window[0]._hWnd, win32con.SW_RESTORE)
        win32gui.SetForegroundWindow(window[0]._hWnd)
        return True
    else:
        messagebox.showinfo("Error", f"Janela nome '{window_title}' não encontrada!")
        return False

def is_window_focused(window_title):
    current_window = gw.getActiveWindow()
    if current_window and current_window.title == window_title:
        return True
    return False

def update_window_list():
    windows = gw.getAllTitles()
    windows = [win for win in windows if win]
    window_combobox['values'] = windows
    if windows:
        window_combobox.current(0)

def on_button(on_btn):
    global isRunning
    if not isRunning:
        if len(data_array) == 0:
            messagebox.showinfo("Error", "Não existe numa tecla inserida!")
            return
        window_title = window_combobox.get()
        if not focus_window(window_title):
            return
        isRunning = True
        on_btn.config(text="ON")
        key_presser(0)
    else:
        isRunning = False
        on_btn.config(text="OFF")

def key_presser(index):
    global isRunning

    if isRunning and index < len(data_array):
        window_title = window_combobox.get()
        if is_window_focused(window_title):
            pyautogui.press(data_array[index])
        root.after(delay_time, key_presser, index + 1)
    elif index >= len(data_array):
        if isRunning:
            key_presser(0)

def capture_and_detect_text():
    """Capture a window region and detect text."""
    global sound_file
    window_title = window_combobox.get()
    if not window_title:
        messagebox.showinfo("Error", "Por favor selecione uma janela!")
        return

    window = gw.getWindowsWithTitle(window_title)
    if not window:
        messagebox.showinfo("Error", f"Janela nome '{window_title}' não encontrada!")
        return

    window = window[0]
    left, top, right, bottom = window.left, window.top, window.right, window.bottom

    with mss.mss() as sct:
        region = {"left": left, "top": top, "width": right - left, "height": bottom - top}
        screenshot = sct.grab(region)
        img = Image.frombytes("RGB", screenshot.size, screenshot.rgb)

    extracted_text = pytesseract.image_to_string(img)
    print(f"Texto extraído: {extracted_text}")  # For debugging

    # Check for specified text in the extracted text
    search_text = text_entry.get()
    if search_text and search_text in extracted_text:
        if sound_file:
            playsound(sound_file)
        else:
            messagebox.showwarning("No Sound", "No sound file selected. Please choose a sound file.")
        messagebox.showinfo("Success", f"Texto encontrado: '{search_text}'")

def add_keys_to_array():
    user_input = key_entry.get()
    if user_input:
        items = user_input.split(",")
        items = [item.strip() for item in items]
        data_array.extend(items)
        array_display.config(text=f"Teclas: {data_array}")
        key_entry.delete(0, tk.END)

def update_delay(delay_entry):
    global delay_time
    try:
        delay_time = int(delay_entry.get())
        messagebox.showinfo("Success", f"O delay foi alterado para {str(delay_time)}")
        delay_entry.delete(0, tk.END)
        delay_entry.insert(0, str(delay_time))
    except ValueError:
        messagebox.showerror("Error", "Adiciona um delay válido")

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Key Presser - Criado por Márcio Carvalho")

    # Window selection
    window_label = tk.Label(root, text="Qual a Janela a focar:")
    window_label.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

    window_combobox = ttk.Combobox(root, width=30)
    window_combobox.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

    refresh_btn = tk.Button(root, text="Atualizar Lista de Janelas", command=update_window_list)
    refresh_btn.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

    # Key press inputs
    key_label = tk.Label(root, text="Insere teclas separadas por vírgula:")
    key_label.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

    key_entry = tk.Entry(root, width=30)
    key_entry.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

    add_key_btn = tk.Button(root, text="Adiciona Teclas", command=add_keys_to_array)
    add_key_btn.grid(row=5, column=0, columnspan=2, padx=10, pady=10)

    # Text detection inputs
    text_label = tk.Label(root, text="Texto para detetar:")
    text_label.grid(row=6, column=0, columnspan=2, padx=10, pady=10)

    text_entry = tk.Entry(root, width=30)
    text_entry.grid(row=7, column=0, columnspan=2, padx=10, pady=10)

    detect_text_btn = tk.Button(root, text="Detectar Texto", command=capture_and_detect_text)
    detect_text_btn.grid(row=8, column=0, columnspan=2, padx=10, pady=10)

    # Sound selection
    sound_btn = tk.Button(root, text="Escolher Som", command=choose_sound_file)
    sound_btn.grid(row=9, column=0, columnspan=2, padx=10, pady=10)

    sound_label = tk.Label(root, text="Selected Sound: None")
    sound_label.grid(row=10, column=0, columnspan=2, padx=10, pady=10)

    # Array and delay
    array_display = tk.Label(root, text="Teclas: []", anchor="w")
    array_display.grid(row=11, column=0, columnspan=2, padx=10, pady=10)

    delay_entry = tk.Entry(root, width=30)
    delay_entry.grid(row=12, column=0, columnspan=2, padx=10, pady=10)
    delay_entry.insert(0, str(delay_time))

    set_delay_btn = tk.Button(root, text="Definir Atraso", command=lambda: update_delay(delay_entry))
    set_delay_btn.grid(row=13, column=0, columnspan=2, padx=10, pady=10)

    update_window_list()

    root.mainloop()

