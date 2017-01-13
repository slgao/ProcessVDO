@echo off
for %%a in (*.ui) do (
pyuic %%a -o ../py_gui/%%~na.py)
pause
