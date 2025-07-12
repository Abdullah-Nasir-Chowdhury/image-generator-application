Write-Host "Building AI Image Generator..." -ForegroundColor Green
Write-Host ""

# Activate the Python virtual environment
Write-Host "Activating Python virtual environment..." -ForegroundColor Yellow

$envActivated = $false
$envPaths = @(
    "image-generator\Scripts\Activate.ps1",
    "venv\Scripts\Activate.ps1", 
    "env\Scripts\Activate.ps1",
    "..\image-generator\Scripts\Activate.ps1"
)

foreach ($envPath in $envPaths) {
    if (Test-Path $envPath) {
        try {
            & $envPath
            Write-Host "Activated virtual environment from $envPath" -ForegroundColor Green
            $envActivated = $true
            break
        }
        catch {
            Write-Host "Failed to activate environment at $envPath" -ForegroundColor Red
        }
    }
}

if (-not $envActivated) {
    Write-Host "Error: Could not find or activate Python virtual environment" -ForegroundColor Red
    Write-Host "Please make sure your virtual environment is in one of these locations:" -ForegroundColor Red
    Write-Host "  - .\image-generator\" -ForegroundColor Red
    Write-Host "  - .\venv\" -ForegroundColor Red
    Write-Host "  - .\env\" -ForegroundColor Red
    Write-Host "  - ..\image-generator\" -ForegroundColor Red
    Write-Host ""
    Write-Host "Or modify this script to point to your virtual environment location" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

# Check if environment activation was successful
if (-not $env:VIRTUAL_ENV) {
    Write-Host "Error: Failed to activate Python virtual environment" -ForegroundColor Red
    Write-Host "Make sure the environment exists and is properly configured" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host "Virtual environment activated: $env:VIRTUAL_ENV" -ForegroundColor Green

# Install PyInstaller if not already installed
Write-Host "Installing PyInstaller..." -ForegroundColor Yellow
pip install pyinstaller

# Clean previous builds
Write-Host "Cleaning previous builds..." -ForegroundColor Yellow
if (Test-Path "build") {
    Remove-Item -Recurse -Force "build"
}
if (Test-Path "dist") {
    Remove-Item -Recurse -Force "dist"
}

# Build the executable using the spec file
Write-Host "Building executable..." -ForegroundColor Yellow
pyinstaller --clean app.spec

# Check if build was successful
if (Test-Path "dist\AI_Image_Generator.exe") {
    Write-Host ""
    Write-Host "=====================================" -ForegroundColor Green
    Write-Host "Build completed successfully!" -ForegroundColor Green
    Write-Host "Executable created: dist\AI_Image_Generator.exe" -ForegroundColor Green
    Write-Host "=====================================" -ForegroundColor Green
    Write-Host ""
    Write-Host "To run the application:" -ForegroundColor Cyan
    Write-Host ".\dist\AI_Image_Generator.exe" -ForegroundColor Cyan
    Write-Host ""
} else {
    Write-Host ""
    Write-Host "=====================================" -ForegroundColor Red
    Write-Host "Build failed! Check the output above for errors." -ForegroundColor Red
    Write-Host "=====================================" -ForegroundColor Red
    Write-Host ""
}

Read-Host "Press Enter to exit"