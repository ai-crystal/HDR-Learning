@echo off
setlocal
cd /d "%~dp0"
set "PY=D:\DevTools\Anaconda3\python.exe"
if not exist "%PY%" set "PY=python"

"%PY%" -c "import markdown, pymupdf, PIL" >nul 2>nul
if errorlevel 1 (
  echo Installing Python dependencies ...
  "%PY%" -m pip install --quiet markdown pymupdf pillow
)

if "%~1"=="" (
  call :one beginner || exit /b 1
  call :one color-science || exit /b 1
  call :one hdr-tech || exit /b 1
) else (
  call :one %~1 || exit /b 1
)

echo.
echo Done. PDFs are in output\
goto :eof

:one
echo [%1] building ...
"%PY%" "books\build\build_html.py" --book "books\%1" || exit /b 1
"%PY%" "books\build\build_pdf.py" --book "books\%1" || exit /b 1
exit /b 0
