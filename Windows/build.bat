@echo off
echo Building AI Image Generator...
echo.

REM Activate the Python virtual environment
echo Activating Python virtual environment...

REM Try different common virtual environment locations
if exist "image-generator\Scripts\activate.bat" (
    call image-generator\Scripts\activate.bat
    echo Activated virtual environment from .\image-generator\
    goto :env_found
)

if exist "venv\Scripts\activate.bat" (
    call venv\Scripts\activate.bat
    echo Activated virtual environment from .\venv\
    goto :env_found
)

if exist "env\Scripts\activate.bat" (
    call env\Scripts\activate.bat
    echo Activated virtual environment from .\env\
    goto :env_found
)

if exist "..\image-generator\Scripts\activate.bat" (
    call ..\image-generator\Scripts\activate.bat
    echo Activated virtual environment from ..\image-generator\
    goto :env_found
)

echo Error: Could not find Python virtual environment
echo Please make sure your virtual environment is in one of these locations:
echo   - .\image-generator\
echo   - .\venv\
echo   - .\env\
echo   - ..\image-generator\
echo.
echo Or modify this script to point to your virtual environment location
pause
exit /b 1

:env_found
REM Check if environment activation was successful
if "%VIRTUAL_ENV%"=="" (
    echo Error: Failed to activate Python virtual environment
    echo Make sure the environment exists and is properly configured
    pause
    exit /b 1
)

echo Virtual environment activated: %VIRTUAL_ENV%

REM Install PyInstaller if not already installed
echo Installing PyInstaller...
pip install pyinstaller

REM Clean previous builds
echo Cleaning previous builds...
if exist "build" rmdir /s /q "build"
if exist "dist" rmdir /s /q "dist"

REM Build the executable using the spec file
echo Building executable...
pyinstaller --clean app.spec

REM Check if build was successful
if exist "dist\AI_Image_Generator.exe" (
    echo.
    echo =====================================
    echo Build completed successfully!
    echo Executable created: dist\AI_Image_Generator.exe
    echo =====================================
    echo.
    echo To run the application:
    echo dist\AI_Image_Generator.exe
    echo.
) else (
    echo.
    echo =====================================
    echo Build failed! Check the output above for errors.
    echo =====================================
    echo.
    pause
    exit /b 1
)

pause