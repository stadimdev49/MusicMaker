import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import pygame
import numpy as np
from scipy.signal import butter, lfilter
from scipy.io import wavfile

# Αρχικοποίηση Pygame Mixer
pygame.mixer.init(frequency=44100, size=-16, channels=1)
SAMPLE_RATE = 44100

def lowpass_filter(data, cutoff, fs=SAMPLE_RATE, order=4):
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    if normal_cutoff >= 1.0:
        return data
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    return lfilter(b, a, data)

def generate_synth_sound(sound_type, cutoff_freq=5000):
    if sound_type == "kick":
        duration = 0.2
        t = np.linspace(0, duration, int(SAMPLE_RATE * duration), endpoint=False)
        freq = 160 * np.exp(-t * 18) + 30
        wave = np.sin(2 * np.pi * freq * t) * np.exp(-t * 7)
    elif sound_type == "snare":
        duration = 0.12
        t = np.linspace(0, duration, int(SAMPLE_RATE * duration), endpoint=False)
        tone = np.sin(2 * np.pi * 220 * t)
        noise = np.random.uniform(-1, 1, len(t))
        wave = (tone * 0.3 + noise * 0.7) * np.exp(-t * 14)
    elif sound_type == "hihat_closed":
        duration = 0.04
        t = np.linspace(0, duration, int(SAMPLE_RATE * duration), endpoint=False)
        noise = np.random.uniform(-1, 1, len(t))
        wave = noise * np.exp(-t * 50)
    elif sound_type == "hihat_open":
        duration = 0.15
        t = np.linspace(0, duration, int(SAMPLE_RATE * duration), endpoint=False)
        noise = np.random.uniform(-1, 1, len(t))
        wave = noise * np.exp(-t * 15)
    elif sound_type == "clap":
        duration = 0.12
        t = np.linspace(0, duration, int(SAMPLE_RATE * duration), endpoint=False)
        noise = np.random.uniform(-1, 1, len(t))
        wave = noise * np.exp(-t * 12)
    elif sound_type == "rimshot":
        duration = 0.05
        t = np.linspace(0, duration, int(SAMPLE_RATE * duration), endpoint=False)
        wave = np.sin(2 * np.pi * 800 * t) * np.exp(-t * 30)
    elif sound_type == "cowbell":
        duration = 0.1
        t = np.linspace(0, duration, int(SAMPLE_RATE * duration), endpoint=False)
        wave = (np.sin(2 * np.pi * 540 * t) + np.sin(2 * np.pi * 800 * t)) * np.exp(-t * 15)
    elif sound_type == "percussion":
        duration = 0.08
        t = np.linspace(0, duration, int(SAMPLE_RATE * duration), endpoint=False)
        freq = 400 * np.exp(-t * 30)
        wave = np.sin(2 * np.pi * freq * t) * np.exp(-t * 20)
    elif sound_type == "tom_low":
        duration = 0.25
        t = np.linspace(0, duration, int(SAMPLE_RATE * duration), endpoint=False)
        freq = 110 * np.exp(-t * 10) + 40
        wave = np.sin(2 * np.pi * freq * t) * np.exp(-t * 8)
    elif sound_type == "tom_high":
        duration = 0.18
        t = np.linspace(0, duration, int(SAMPLE_RATE * duration), endpoint=False)
        freq = 220 * np.exp(-t * 12) + 80
        wave = np.sin(2 * np.pi * freq * t) * np.exp(-t * 10)
    elif sound_type == "bass":
        duration = 0.2
        t = np.linspace(0, duration, int(SAMPLE_RATE * duration), endpoint=False)
        wave = np.sign(np.sin(2 * np.pi * 110 * t)) * np.exp(-t * 6)
    elif sound_type == "sub_bass":
        duration = 0.25
        t = np.linspace(0, duration, int(SAMPLE_RATE * duration), endpoint=False)
        wave = np.sin(2 * np.pi * 55 * t) * np.exp(-t * 4)
    elif sound_type == "synth_bassline":
        duration = 0.22
        t = np.linspace(0, duration, int(SAMPLE_RATE * duration), endpoint=False)
        freq = 82.4 * (1 + 0.5 * np.exp(-t * 20))
        wave = np.sign(np.sin(2 * np.pi * freq * t)) * np.exp(-t * 5)
    elif sound_type == "synth_lead":
        duration = 0.15
        t = np.linspace(0, duration, int(SAMPLE_RATE * duration), endpoint=False)
        wave = np.sin(2 * np.pi * 440 * t) * np.exp(-t * 10)
    elif sound_type == "laser":
        duration = 0.15
        t = np.linspace(0, duration, int(SAMPLE_RATE * duration), endpoint=False)
        freq = 1200 * np.exp(-t * 30) + 100
        wave = np.sin(2 * np.pi * freq * t) * np.exp(-t * 12)
    else:  # crash
        duration = 0.6
        t = np.linspace(0, duration, int(SAMPLE_RATE * duration), endpoint=False)
        noise = np.random.uniform(-1, 1, len(t))
        wave = noise * np.exp(-t * 4)

    filtered_wave = lowpass_filter(wave, cutoff_freq, SAMPLE_RATE)
    audio = (filtered_wave * 32767).astype(np.int16)
    return pygame.mixer.Sound(buffer=audio)

current_cutoff = 5000
sound_types = [
    "kick", "snare", "hihat_closed", "hihat_open", "clap", "rimshot", 
    "cowbell", "percussion", "tom_low", "tom_high", "bass", "sub_bass", 
    "synth_bassline", "synth_lead", "laser", "crash"
]
labels = [
    "Kick", "Snare", "HH Closed", "HH Open", "Clap", "Rimshot", 
    "Cowbell", "Perc", "Tom Low", "Tom High", "Bass", "Sub Bass", 
    "Synth Bass", "Lead", "Laser", "Crash"
]

sounds = [generate_synth_sound(st, current_cutoff) for st in sound_types]

ROWS = len(sound_types)
COLS = 32
current_step = 0
is_playing = False
backing_track_sound = None

root = tk.Tk()
root.title("Python Techno Sequencer - Extended GUI")
root.geometry("1250x850")
root.config(bg="#1e1e1e")

root.rowconfigure(0, weight=1)
root.columnconfigure(0, weight=1)

# Main Container
container = tk.Frame(root, bg="#1e1e1e")
container.grid(row=0, column=0, columnspan=2, sticky="nsew")

container.rowconfigure(0, weight=1)
container.columnconfigure(0, weight=1)

# Canvas + Both Scrollbars (Horizontal & Vertical)
canvas = tk.Canvas(container, bg="#1e1e1e", highlightthickness=0)
scrollbar_h = ttk.Scrollbar(container, orient="horizontal", command=canvas.xview)
scrollbar_v = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)

scrollable_frame = tk.Frame(canvas, bg="#1e1e1e")

def on_frame_configure(event):
    canvas.configure(scrollregion=canvas.bbox("all"))

scrollable_frame.bind("<Configure>", on_frame_configure)
canvas_window = canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

def on_canvas_configure(event):
    canvas.itemconfig(canvas_window, minwidth=event.width)

canvas.bind('<Configure>', on_canvas_configure)
canvas.configure(xscrollcommand=scrollbar_h.set, yscrollcommand=scrollbar_v.set)

def _on_mousewheel(event):
    canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

canvas.bind_all("<MouseWheel>", _on_mousewheel)

canvas.grid(row=0, column=0, sticky="nsew")
scrollbar_v.grid(row=0, column=1, sticky="ns")
scrollbar_h.grid(row=1, column=0, sticky="ew")

buttons = []
step_state = []
pattern_entries = []

def parse_step_input(input_str, max_cols):
    steps_to_enable = set()
    input_str = input_str.strip()
    if not input_str:
        return steps_to_enable

    if input_str.startswith("/"):
        input_str = input_str[1:]

    parts = input_str.replace(',', ' ').split()
    for part in parts:
        if ':' in part:
            try:
                interval_str, range_str = part.split(':', 1)
                step_interval = int(interval_str)
                if step_interval <= 0:
                    continue

                if '-' in range_str:
                    start_str, end_str = range_str.split('-', 1)
                    start = int(start_str)
                    end = int(end_str)
                else:
                    start = int(range_str)
                    end = max_cols

                start_idx = max(1, start) - 1
                end_idx = min(max_cols, end)

                for idx in range(start_idx, end_idx, step_interval):
                    steps_to_enable.add(idx)
            except ValueError:
                continue

        elif '-' in part:
            try:
                start_str, end_str = part.split('-', 1)
                start = int(start_str)
                end = int(end_str)
                for idx in range(start, end + 1):
                    if 1 <= idx <= max_cols:
                        steps_to_enable.add(idx - 1)
            except ValueError:
                continue

        else:
            try:
                idx = int(part)
                if 1 <= idx <= max_cols:
                    steps_to_enable.add(idx - 1)
            except ValueError:
                continue

    return steps_to_enable

def apply_pattern(row_idx):
    entry_val = pattern_entries[row_idx].get()
    selected_indices = parse_step_input(entry_val, COLS)
    
    for c in range(COLS):
        is_active = c in selected_indices
        step_state[row_idx][c] = is_active
        color = "#e74c3c" if is_active else "#333333"
        buttons[row_idx][c].config(bg=color)

def clear_row(row_idx):
    pattern_entries[row_idx].delete(0, tk.END)
    for c in range(COLS):
        step_state[row_idx][c] = False
        buttons[row_idx][c].config(bg="#333333")

def update_duration_display(*args):
    try:
        bpm = float(bpm_slider.get())
        cols = int(steps_var.get())
        mult = int(mult_var.get())
        
        base_sec = (60.0 / (bpm * 4)) * cols
        total_sec = base_sec * mult
        lbl_duration.config(text=f"Αρχική: {base_sec:.2f}s | Τελική ({mult}x): {total_sec:.2f}s")
    except Exception:
        pass

def init_grid():
    global buttons, step_state, pattern_entries, COLS
    for widget in scrollable_frame.winfo_children():
        widget.destroy()
    
    try:
        COLS = int(steps_var.get())
    except:
        COLS = 32

    buttons = [[None for _ in range(COLS)] for _ in range(ROWS)]
    step_state = [[False for _ in range(COLS)] for _ in range(ROWS)]
    pattern_entries = []

    scrollable_frame.columnconfigure(0, weight=0)
    for c in range(COLS):
        scrollable_frame.columnconfigure(c + 1, weight=1)

    for r in range(ROWS):
        scrollable_frame.rowconfigure(r, weight=1)

        row_ctrl_frame = tk.Frame(scrollable_frame, bg="#1e1e1e")
        row_ctrl_frame.grid(row=r, column=0, sticky="w", padx=5, pady=2)

        lbl = tk.Label(row_ctrl_frame, text=labels[r], fg="white", bg="#1e1e1e", font=("Arial", 9, "bold"), width=10, anchor="w")
        lbl.pack(side="left")

        entry = tk.Entry(row_ctrl_frame, width=9, bg="#2c3e50", fg="white", insertbackground="white", font=("Arial", 8))
        entry.pack(side="left", padx=2)
        entry.bind("<Return>", lambda e, row=r: apply_pattern(row))
        pattern_entries.append(entry)

        btn_set = tk.Button(row_ctrl_frame, text="Set", bg="#34495e", fg="white", font=("Arial", 7, "bold"),
                            command=lambda row=r: apply_pattern(row))
        btn_set.pack(side="left", padx=1)

        btn_clr = tk.Button(row_ctrl_frame, text="X", bg="#7f8c8d", fg="white", font=("Arial", 7, "bold"),
                            command=lambda row=r: clear_row(row))
        btn_clr.pack(side="left", padx=1)

        for c in range(COLS):
            pad_x = 4 if (c + 1) % 16 == 0 else 1
            btn = tk.Button(scrollable_frame, text="", bg="#333333",
                            command=lambda row=r, col=c: toggle_btn(row, col))
            btn.grid(row=r, column=c+1, padx=(1, pad_x), pady=2, sticky="nsew")
            buttons[r][c] = btn

    update_duration_display()

def toggle_btn(r, c):
    step_state[r][c] = not step_state[r][c]
    new_color = "#e74c3c" if step_state[r][c] else "#333333"
    buttons[r][c].config(bg=new_color)

def step_loop():
    global current_step, is_playing
    if not is_playing:
        return

    prev_step = (current_step - 1) % COLS

    for r in range(ROWS):
        rest_color = "#e74c3c" if step_state[r][prev_step] else "#333333"
        buttons[r][prev_step].config(bg=rest_color)

    for r in range(ROWS):
        if step_state[r][current_step]:
            sounds[r].play()
        buttons[r][current_step].config(bg="#f1c40f")

    current_step = (current_step + 1) % COLS
    
    bpm = bpm_slider.get()
    delay = int(60000 / (bpm * 4))
    root.after(delay, step_loop)

def start_sequencer():
    global is_playing
    if not is_playing:
        is_playing = True
        if backing_track_sound:
            backing_track_sound.play()
        step_loop()

def stop_sequencer():
    global is_playing, current_step
    is_playing = False
    current_step = 0
    pygame.mixer.stop()
    for r in range(ROWS):
        for c in range(COLS):
            rest_color = "#e74c3c" if step_state[r][c] else "#333333"
            buttons[r][c].config(bg=rest_color)

def update_filter(val):
    global sounds
    cutoff = float(val)
    sounds = [generate_synth_sound(st, cutoff) for st in sound_types]

def load_parallel_track():
    global backing_track_sound
    file_path = filedialog.askopenfilename(filetypes=[("Audio Files", "*.wav *.ogg *.mp3")])
    if file_path:
        backing_track_sound = pygame.mixer.Sound(file_path)
        messagebox.showinfo("Επιτυχία", "Το παράλληλο τραγούδι φορτώθηκε επιτυχώς!")

def export_wav():
    bpm = bpm_slider.get()
    step_duration = 60.0 / (bpm * 4)
    base_duration = step_duration * COLS
    
    multiplier = int(mult_var.get())
    total_duration = base_duration * multiplier
    total_samples = int(SAMPLE_RATE * total_duration)
    
    base_samples = int(SAMPLE_RATE * base_duration)
    single_loop_audio = np.zeros(base_samples, dtype=np.float32)
    
    for r in range(ROWS):
        raw_sound_bytes = sounds[r].get_raw()
        sound_array = np.frombuffer(raw_sound_bytes, dtype=np.int16).astype(np.float32) / 32767.0
        
        for c in range(COLS):
            if step_state[r][c]:
                start_sample = int(c * step_duration * SAMPLE_RATE)
                end_sample = start_sample + len(sound_array)
                if end_sample > base_samples:
                    single_loop_audio[start_sample:] += sound_array[:base_samples - start_sample]
                else:
                    single_loop_audio[start_sample:end_sample] += sound_array

    # Επανάληψη του pattern ανάλογα με τον πολλαπλασιαστή
    mixed_audio = np.tile(single_loop_audio, multiplier)

    max_val = np.max(np.abs(mixed_audio))
    if max_val > 0:
        mixed_audio = mixed_audio / max_val

    output_data = (mixed_audio * 32767).astype(np.int16)
    file_path = filedialog.asksaveasfilename(defaultextension=".wav", filetypes=[("WAV files", "*.wav")])
    if file_path:
        wavfile.write(file_path, SAMPLE_RATE, output_data)
        messagebox.showinfo("Επιτυχία", f"Αποθηκεύτηκε στο:\n{file_path}\nΣυνολική Διάρκεια: {total_duration:.2f} δευτερόλεπτα")

def concatenate_wav_files():
    """Συρραφή πολλαπλών αρχείων WAV εν σειρά (διαδοχικά)"""
    file_paths = filedialog.askopenfilenames(
        title="Επιλέξτε αρχεία WAV για συρραφή εν σειρά",
        filetypes=[("WAV files", "*.wav")]
    )
    if not file_paths:
        return

    combined_audio = []
    target_sr = SAMPLE_RATE

    for path in file_paths:
        sr, data = wavfile.read(path)
        
        # Αν είναι stereo, μετατροπή σε mono
        if len(data.shape) > 1:
            data = data.mean(axis=1)
            
        # Κανονικοποίηση σε float32
        if data.dtype == np.int16:
            data = data.astype(np.float32) / 32767.0
        elif data.dtype == np.int32:
            data = data.astype(np.float32) / 2147483647.0
            
        combined_audio.append(data)

    final_audio = np.concatenate(combined_audio)
    
    # Κανονικοποίηση για αποφυγή distortion
    max_val = np.max(np.abs(final_audio))
    if max_val > 0:
        final_audio = final_audio / max_val

    output_data = (final_audio * 32767).astype(np.int16)
    save_path = filedialog.asksaveasfilename(
        title="Αποθήκευση Συρραμμένου Αρχείου",
        defaultextension=".wav", 
        filetypes=[("WAV files", "*.wav")]
    )
    if save_path:
        wavfile.write(save_path, target_sr, output_data)
        total_sec = len(output_data) / target_sr
        messagebox.showinfo("Επιτυχία", f"Η συρραφή ολοκληρώθηκε!\nΑρχεία: {len(file_paths)}\nΣυνολική Διάρκεια: {total_sec:.2f} δευτερόλεπτα")

# --- Instructions Panel ---
help_frame = tk.LabelFrame(root, text=" 💡 Οδηγίες Επιλογής Διαστημάτων ", fg="#f39c12", bg="#2c3e50", font=("Arial", 9, "bold"))
help_frame.grid(row=1, column=0, columnspan=2, sticky="we", padx=10, pady=2)

help_text = (
    "• /4:6-18  → Ανά 4 διαστήματα, από το 6ο έως το 18ο (δηλ. 6, 10, 14, 18)\n"
    "• /4:3     → Ανά 4 διαστήματα, ξεκινώντας από το 3ο μέχρι το τέλος\n"
    "• 1, 5, 6  → Μεμονωμένα διαστήματα |  3-10 → Συνεχόμενα από 3 έως 10"
)
tk.Label(help_frame, text=help_text, fg="white", bg="#2c3e50", justify="left", font=("Consolas", 8)).pack(anchor="w", padx=5, pady=2)

# --- Dynamic Controls Layout ---
controls_frame = tk.Frame(root, bg="#1e1e1e")
controls_frame.grid(row=2, column=0, columnspan=2, sticky="we", padx=10, pady=2)

bpm_slider = tk.Scale(controls_frame, from_=60, to=200, orient="horizontal", label="BPM", bg="#2c3e50", fg="white", highlightbackground="#1e1e1e", command=lambda v: update_duration_display())
bpm_slider.set(125)
bpm_slider.pack(side="left", padx=5, fill="x", expand=True)

filter_slider = tk.Scale(controls_frame, from_=200, to=12000, orient="horizontal", label="Filter Cutoff (Hz)", bg="#2c3e50", fg="white", highlightbackground="#1e1e1e", command=update_filter)
filter_slider.set(5000)
filter_slider.pack(side="left", padx=5, fill="x", expand=True)

# Dynamic Length Selection & Multiplier Frame
length_frame = tk.Frame(root, bg="#1e1e1e")
length_frame.grid(row=3, column=0, columnspan=2, sticky="we", padx=10, pady=2)

tk.Label(length_frame, text="Steps:", fg="white", bg="#1e1e1e").pack(side="left", padx=2)
steps_var = tk.StringVar(value="32")
steps_dropdown = ttk.Combobox(length_frame, textvariable=steps_var, values=["32", "64", "128"], width=4, state="readonly")
steps_dropdown.pack(side="left", padx=2)

btn_update_grid = tk.Button(length_frame, text="Apply Length", bg="#e67e22", fg="white", font=("Arial", 8, "bold"), command=init_grid)
btn_update_grid.pack(side="left", padx=5)

tk.Label(length_frame, text="Multiplier:", fg="white", bg="#1e1e1e").pack(side="left", padx=(15, 2))
mult_var = tk.StringVar(value="1")
mult_dropdown = ttk.Combobox(length_frame, textvariable=mult_var, values=["1", "2", "3", "4", "8"], width=3, state="readonly")
mult_dropdown.pack(side="left", padx=2)
mult_dropdown.bind("<<ComboboxSelected>>", update_duration_display)

lbl_duration = tk.Label(length_frame, text="Διάρκεια: --s", fg="#f1c40f", bg="#1e1e1e", font=("Arial", 9, "bold"))
lbl_duration.pack(side="left", padx=15)

# Action Buttons
btn_start = tk.Button(root, text="PLAY", bg="#2ecc71", fg="white", font=("Arial", 9, "bold"), command=start_sequencer)
btn_start.grid(row=4, column=0, sticky="we", padx=5, pady=2)

btn_stop = tk.Button(root, text="STOP", bg="#c0392b", fg="white", font=("Arial", 9, "bold"), command=stop_sequencer)
btn_stop.grid(row=4, column=1, sticky="we", padx=5, pady=2)

btn_load = tk.Button(root, text="LOAD PARALLEL TRACK", bg="#9b59b6", fg="white", font=("Arial", 9, "bold"), command=load_parallel_track)
btn_load.grid(row=5, column=0, sticky="we", padx=5, pady=2)

btn_concat = tk.Button(root, text="CONCAT WAV FILES (IN SERIES)", bg="#16a085", fg="white", font=("Arial", 9, "bold"), command=concatenate_wav_files)
btn_concat.grid(row=5, column=1, sticky="we", padx=5, pady=2)

btn_export = tk.Button(root, text="EXPORT WAV", bg="#3498db", fg="white", font=("Arial", 9, "bold"), command=export_wav)
btn_export.grid(row=6, column=0, columnspan=2, sticky="we", padx=5, pady=4)

# Initialize starting grid
init_grid()

root.mainloop()