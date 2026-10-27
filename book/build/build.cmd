@echo off
setlocal
cd /d "%~dp0"
set "PY=D:\DevTools\Anaconda3\python.exe"
set "NODE=node"
where node >nul 2>nul
if errorlevel 1 set "NODE=C:\Program Files\nodejs\node.exe"

echo [1/3] Markdown to HTML ...
"%PY%" "build_html.py"
if errorlevel 1 goto err
echo [2/3] HTML to PDF ...
"%NODE%" "build_pdf.mjs"
if errorlevel 1 goto err
echo [3/3] Writing PDF bookmarks ...
"%PY%" "apply_outline.py"
if errorlevel 1 goto err
echo.
echo Done. PDF -> E:\Study\HDR技术\output
goto :eof

:err
echo.
echo BUILD FAILED. Check Python / Node / Chrome.
exit /b 1
