@echo off
setlocal enabledelayedexpansion

set "APP_NAME=Scraping Manhwa Manga"
set "AUTO_ZIP_NAME=Auto Zip"

echo [1.1] PyInstaller : %APP_NAME% 
pyinstaller --onefile --noconsole --name="%APP_NAME%" --splash logo.png --icon "assets/logo.ico" --add-data "assets;assets" main.py

echo [1.2] PyInstaller : %AUTO_ZIP_NAME%
pyinstaller --onefile --console --name="%AUTO_ZIP_NAME%" --icon "assets/ziprar.ico" --add-data "assets;assets" script/auto_zip_the_series.py

echo [2] Cleaning temporary file (.spec and build)...

if exist "%APP_NAME%.spec"      del /f /q "%APP_NAME%.spec"
if exist "%AUTO_ZIP_NAME%.spec" del /f /q "%AUTO_ZIP_NAME%.spec"
if exist "build" rd /s /q "build"
if exist "_pyi_splash" rd /s /q "_pyi_splash"

echo [3] Done
pause