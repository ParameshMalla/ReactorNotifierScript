@ECHO OFF
set /a x=1
:loop
echo %x%
python scrap.py
set /a x+=1
timeout /t 60
goto loop