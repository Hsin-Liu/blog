@echo off
REM =============================================================================
REM Video Batch Processor - Windows Batch Runner
REM 
REM Usage:
REM   run_batch.bat                              # Interactive mode
REM   run_batch.bat "C:\Videos" "C:\Output"     # Direct arguments
REM
REM For Task Scheduler:
REM   Create task with: run_batch.bat "C:\InputVideos" "C:\OutputDir"
REM =============================================================================

setlocal enabledelayedexpansion

REM =============================================================================
REM CONFIGURATION - Adjust these paths as needed
REM =============================================================================

REM Python executable (use full path for scheduled tasks)
set PYTHON_EXE=python

REM Input/Output directories
set INPUT_DIR=%1
set OUTPUT_DIR=%2

REM If no arguments provided, ask interactively
if "%INPUT_DIR%"=="" (
    echo ================================================
    echo Video Batch Processor
    echo ================================================
    echo.
    set /p INPUT_DIR="Input directory (videos): "
    set /p OUTPUT_DIR="Output directory: "
)

REM Validate inputs
if not exist "%INPUT_DIR%" (
    echo ERROR: Input directory not found: %INPUT_DIR%
    exit /b 1
)

REM Create output directory if needed
if not exist "%OUTPUT_DIR%" mkdir "%OUTPUT_DIR%"

echo.
echo ================================================
echo Video Batch Processor
echo ================================================
echo Input:   %INPUT_DIR%
echo Output:  %OUTPUT_DIR%
echo.

REM Get current date/time for logging
for /f "tokens=1-4 delims=/ " %%a in ('date /t') do (
    set DATE=%%a-%%b-%%c
)
for /f "tokens=1-4 delims=:." %%a in ('time /t') do (
    set TIME=%%a-%%b
)

REM Run batch processor
echo [%DATE% %TIME%] Starting batch processing...
echo.

cd /d "%~dp0"

%PYTHON_EXE% batch_processor.py --input-dir "%INPUT_DIR%" --output-dir "%OUTPUT_DIR%" --recursive

set EXIT_CODE=%ERRORLEVEL%

echo.
echo ================================================
if %EXIT_CODE%==0 (
    echo SUCCESS: Batch processing complete
) else (
    echo ERROR: Batch processing failed (exit code: %EXIT_CODE%)
)
echo ================================================

exit /b %EXIT_CODE%
