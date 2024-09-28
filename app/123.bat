@echo off
setlocal enabledelayedexpansion

set "searchDir=C:\Users\rwr\Desktop\Full web - Copy\app"
set "searchString=app.auth"

echo Searching for files containing "%searchString%" in %searchDir%...
echo.

for /r "%searchDir%" %%F in (*) do (
    findstr /m /c:"%searchString%" "%%F" >nul
    if !errorlevel! equ 0 (
        echo %%F
    )
)

echo.
echo Search complete.