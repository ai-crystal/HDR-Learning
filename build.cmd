@echo off
rem One-click build: Markdown -> PDF (output folder)
cd /d "%~dp0"
call "book\build\build.cmd"
