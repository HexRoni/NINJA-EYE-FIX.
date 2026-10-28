# NINJA EYE (fixed project layout)

## Windows
Double-click `run.bat`, or in PowerShell run:
```powershell
py -3 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe ninja_eye.py
```

## Linux / Kali
```bash
chmod +x run.sh
./run.sh
```

 password: `NINJA` (this is only a demonstration gate, not real security).

## Tests
```bash
python -m unittest discover -s tests -v
```

The supplied photo/sample data is retained. Review it before sharing publicly, as photos may contain personal metadata.
