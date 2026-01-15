# Quick Start Guide

## Method 1: Run with Python (Easiest)

### Step 1: Download Python
- Go to: https://www.python.org/downloads/
- Download Python 3.8 or higher
- **IMPORTANT**: Check "Add Python to PATH" during installation!

### Step 2: Run the Program
1. Double-click `run_simple.bat`
2. First run will install packages automatically (1-2 minutes)
3. Program will start with GUI window
4. Enter your settings and click "Start"!

## Method 2: Build EXE (No Python needed after build)

### Step 1: Install Python temporarily
- Follow Method 1, Step 1

### Step 2: Build EXE
1. Double-click `make_exe.bat`
2. Wait 5-10 minutes for build
3. Find `dist\NaverBandAutoPoster.exe`
4. Copy EXE to desktop
5. You can now uninstall Python!

### Step 3: Run EXE
- Double-click `NaverBandAutoPoster.exe` anywhere
- No Python required!

## Method 3: Manual Install (Developers)

```bash
pip install -r requirements.txt
python run.py
```

## Files to Use

- **run_simple.bat** - One-click run (with Python)
- **make_exe.bat** - Build standalone EXE
- **run.py** - Python script (manual)

## Requirements

- Python 3.8+ (for running or building)
- Chrome Browser (for automation)
- Internet connection

## Troubleshooting

**Q: "Python is not recognized"**
- Reinstall Python with "Add Python to PATH" checked
- Or use `py` command: `py run.py`

**Q: Package installation failed**
```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

**Q: Windows Defender warning for EXE**
- Click "More info" > "Run anyway"
- It's safe, just unsigned software

**Q: Login failed**
- Disable 2-factor authentication temporarily
- Handle CAPTCHA manually if appears

## Support

GitHub: https://github.com/rpaakdi1-spec/naver-band-auto-poster
Issues: https://github.com/rpaakdi1-spec/naver-band-auto-poster/issues
