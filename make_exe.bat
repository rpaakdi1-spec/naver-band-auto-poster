@echo off
title Build EXE File

echo ================================================
echo Naver Band Auto Poster - Build EXE
echo ================================================
echo.
echo Python must be installed for building.
echo After build, EXE file can run without Python!
echo.
pause

echo.
echo [Step 1/3] Installing packages...
pip install -r requirements.txt
pip install pyinstaller

echo.
echo [Step 2/3] Building EXE... (5-10 minutes)
pyinstaller --clean --noconfirm build_exe.spec

echo.
echo [Step 3/3] Done!
echo.
echo ================================================
echo EXE file location:
echo   dist\NaverBandAutoPoster.exe
echo ================================================
echo.
echo You can now copy the EXE file to desktop!
echo.
pause
