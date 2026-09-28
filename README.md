# 🎵 Python Techno Sequencer & Audio Tools

Ένα διαδραστικό Step Sequencer & Sound Synthesizer γραμμένο σε Python με περιβάλλον εργασίας **Tkinter**. Επιτρέπει τη δημιουργία techno patterns, την παραμετροποίηση ήχων μέσω φίλτρων, την παράλληλη αναπαραγωγή backing tracks, τον υπολογισμό διάρκειας με πολλαπλασιαστές, την εξαγωγή σε WAV, καθώς και τη συρραφή ηχητικών αρχείων εν σειρά.

---

## ✨ Χαρακτηριστικά (Features)

* **16 Synth Sound Channels**: Ενσωματωμένη συνθετική παραγωγή ήχων (Kick, Snare, Hi-Hats, Bass, Leads, Percussion, Laser, κ.ά.).
* **Dynamic Step Sequencer**: Επιλογή μήκους grid (32, 64, 128 steps) με δυνατότητα οριζόντιας και κατακόρυφης πλοήγησης (scrollbars & mousewheel support).
* **Smart Pattern Generator**: Γρήγορη συμπλήρωση βημάτων με ειδική συντακτική δομή (π.χ. `/4:6-18`, `1, 5, 6`, `3-10`).
* **Lowpass Filter Control**: Ρύθμιση Cutoff συχνότητας σε πραγματικό χρόνο μέσω DSP (SciPy Butterworth filter).
* **Live Duration & Multiplier**:
  * Επιλογή πολλαπλασιαστή διάρκειας ($1\times, 2\times, 3\times, 4\times, 8\times$).
  * Υπολογισμός και προβολή της τελικής διάρκειας σε δευτερόλεπτα σε πραγματικό χρόνο.
* **Parallel Track Playing**: Φόρτωση και ταυτόχρονη αναπαραγωγή εξωτερικού backing track (`.wav`, `.mp3`, `.ogg`).
* **WAV Exporting**: Εξαγωγή του pattern σε αρχείο `.wav` λαμβάνοντας υπόψη τον πολλαπλασιαστή διάρκειας.
* **Audio Concatenation**: Δυνατότητα επιλογής και συρραφής πολλαπλών αρχείων WAV **εν σειρά (διαδοχικά)** σε ένα τελικό αρχείο.

---

## 🛠️ Απαιτήσεις Συστήματος (Prerequisites)

* **Python 3.10+**
* Βιβλιοθήκες Python:
  * `pygame`
  * `scipy`
  * `numpy`
  * `tkinter` (συνήθως περιλαμβάνεται στην Python)

---

## 🚀 Εγκατάσταση & Εκτέλεση (Setup & Run)

### 1. Κλωνοποίηση του Repository
```bash
git clone [https://github.com/your-username/python-techno-sequencer.git](https://github.com/your-username/python-techno-sequencer.git)
cd python-techno-sequencer
