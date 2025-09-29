# Browser Fingerprinting vs. Canvas Fingerprint Defender — Detection & Bypass

> **Student Project** — A practical exploration of detecting canvas fingerprinting noise injection and neutralizing it via an iframe-based bypass, with a minimal Selenium test harness.

---

## 🎯 What this project shows

1. **Detection** — How to detect if a privacy extension (e.g., Canvas Fingerprint Defender) is injecting noise into canvas reads by comparing repeated `toDataURL()` outputs and checking pixel values.
2. **Bypass** — How to recover **native** canvas methods using a **hidden iframe** and re-apply them to the main page to neutralize the injected noise.
3. **Automation** — A tiny Selenium script that loads the demo page and reports whether spoofing is detected, so results are repeatable and easy to verify.

This repository contains a small, reproducible demo with two HTML files and one Python script. Two Jupyter notebooks (analysis reports) are included as references to the methodology.

---

## 📁 Repository structure

```
.
├─ 1_Multi-Sample Averaging Technique.ipynb
├─ 2_Neutralizing the Extension via an Iframe Bypass.ipynb
├─ index.html
├─ index2.html
├─ detect_canvas_spoofing.py
└─ README.md
```

- **`index.html`** — Baseline detection page: draws a simple canvas, takes two snapshots, and checks a known pixel. If the privacy extension is active, the outputs differ and a flag is raised. fileciteturn0file1  
- **`index2.html`** — Bypass page: creates a hidden iframe, extracts native `toDataURL` / `getImageData` implementations, then restores them in the main page before generating the fingerprint. fileciteturn0file2  
- **`detect_canvas_spoofing.py`** — Minimal Selenium test harness that opens the local page and prints whether spoofing is active (based on the page title). fileciteturn0file0  
- **Notebooks** — High-level methodology and experiments:
  - *1_Multi-Sample Averaging Technique.ipynb* — Why averaging hashed canvas outputs fails (hashes are categorical, not numeric).
  - *2_Neutralizing the Extension via an Iframe Bypass.ipynb* — Detection + bypass experiments (hidden iframe method).  
  For a concise narrative, see the final report PDF that this README is based on (excluded from this repo by design). Key takeaways are summarized below. fileciteturn0file3

> **Note:** The PDF report is intentionally not included here to keep the repository lean for GitHub. The README summarizes the main results.

---

## ⚙️ Quick start

### 1) Serve the demo locally
Use any static server. With Python 3:

```bash
# From the repo root
python -m http.server 8000
# Visit http://localhost:8000/index.html or http://localhost:8000/index2.html
```

### 2) (Optional) Install Selenium + ChromeDriver
The script assumes a Linux-like path to ChromeDriver (`/usr/bin/chromedriver`). Adjust as needed.

```bash
pip install selenium
# Make sure chromedriver is installed and on your PATH or edit the script's path.
```

### 3) Run the detection harness
```bash
python detect_canvas_spoofing.py
```
The script loads `http://localhost:8000/index.html`, waits briefly, then reads the **document title** set by JavaScript:
- **"Spoofing Detected"** → Noise injection active.  
- **"No Spoofing"** → No modification detected.  
(You can switch the target to `index2.html` for the bypass demo.) fileciteturn0file0

---

## 🧪 How detection works (index.html)

- Draw a blue rectangle and text on a `<canvas>` and capture **two** snapshots with `toDataURL()`.
- Clear and redraw the exact same content and take the second snapshot.
- If an extension injects random noise **per read**, the two base64 outputs **will differ**.
- Additionally, read a **known pixel** (e.g., `[0,127,255,255]` at (5, 5)); if it’s altered, flag spoofing.  
Implementation in `index.html`. fileciteturn0file1

---

## 🛠️ How the bypass works (index2.html)

1. Create a **hidden iframe** dynamically after a short delay.
2. From the iframe’s clean context, copy **native** methods:
   - `HTMLCanvasElement.prototype.toDataURL`
   - `CanvasRenderingContext2D.prototype.getImageData`
3. Remove the iframe and **re-assign** these native methods to the main document.
4. Redraw and capture the fingerprint — it should now be **stable** (noise-free).  
Implementation in `index2.html`. fileciteturn0file2

> Timing matters: run the bypass after the extension hooks the main page, but before it can re-hook your restored methods.

---

## 📊 Results (summary)

- **Multi-sample averaging fails**: Canvas hashes are cryptographic; tiny pixel differences produce unrelated hashes, so arithmetic averaging is meaningless for reconstruction.  
- **Iframe bypass succeeds**: Restoring native methods via an iframe yields a **stable** canvas output, defeating noise injection on the tested setup.  
For the full rationale and experiment notes, see the summarized points derived from the final report. fileciteturn0file3

---

## 🔒 Ethics & responsible use

This project is for **research and education** only. Bypassing privacy protections without informed consent is unethical and may violate platform policies or local laws. Use only in controlled environments where you have permission.

---

## ❓FAQ

**Q: Why is the PDF not here?**  
A: To keep the repo light; the README contains the essential insights.

**Q: I get `selenium.common.exceptions` about ChromeDriver.**  
A: Ensure your Chrome/Chromium version matches ChromeDriver. Update the path in `detect_canvas_spoofing.py` or add it to PATH.

**Q: Will the bypass work against all extensions?**  
A: Behavior varies. Some extensions might also hook iframes or re-hook later; adjust timing and strategy accordingly.

---

## 📜 License

MIT License.

---
