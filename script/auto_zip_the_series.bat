@echo off
setlocal enabledelayedexpansion

echo ===============================
echo PURE CMD CHAPTER ZIPPER
echo ===============================

set /p SERIES=Masukkan path folder series: 
set /p START=Mulai chapter: 
set /p END=Sampai chapter: 
set /p STEP=Per ZIP berapa chapter: 

for %%F in ("%SERIES%") do (
    set SERIES_ABS=%%~fF
    set PREFIX=%%~nxF
)

pushd "%SERIES_ABS%" || (
    echo ❌ Folder series tidak ditemukan
    pause
    exit /b
)

set CUR=%START%

:LOOP
if %CUR% GTR %END% goto DONE

set NEXT=%CUR%
set /a NEXT+=%STEP%-1
if %NEXT% GTR %END% set NEXT=%END%

set ZIP=%PREFIX%_%CUR%-%NEXT%.zip

echo.
echo Membuat %ZIP%

set FILES=

for /L %%i in (%CUR%,1,%NEXT%) do (
    if exist "chapter %%i" set FILES=!FILES! "chapter %%i"
    if exist "chapter_%%i" set FILES=!FILES! "chapter_%%i"
    if exist "chapter-%%i" set FILES=!FILES! "chapter-%%i"
)

if not defined FILES (
    echo ⚠️ Tidak ada folder chapter di range ini
    goto SKIP
)

tar -a -c -f "%ZIP%" %FILES%

:SKIP
set /a CUR+=%STEP%
goto LOOP

:DONE
popd
echo.
echo SELESAI
pause
