@echo off
setlocal
cd /d "%~dp0"
set "PY=D:\DevTools\Anaconda3\python.exe"
set "NODE=node"
where node >nul 2>nul
if errorlevel 1 set "NODE=C:\Program Files\nodejs\node.exe"

echo [1/3] Markdown to HTML ...
"%PY%" "build\build_html.py"
if errorlevel 1 goto err

echo [2/3] HTML to PDF (Chrome engine) ...
"%NODE%" "build\build_pdf.mjs"
if errorlevel 1 goto err

echo [3/3] Writing PDF bookmarks ...
"%PY%" "build\apply_outline.py"
if errorlevel 1 goto err

echo.
echo Done. PDF written to the book output folder.
goto :eof

:err
echo.
echo BUILD FAILED. Please check Python, Node.js and Chrome.
exit /b 1
