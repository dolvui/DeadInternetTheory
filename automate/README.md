## Put `.bat` file here to automate code as : 

```bat
@echo off
cd /d C:\Users\Noa\PycharmProjects\DeadInternetTheory\
call venv\Scripts\activate.bat
python main.py --sessions-path="sessions.json" --pix-credit=True
```