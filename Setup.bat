@echo off
cls

:: +---------------------------------------------------------------------------------------------+
:: | This is a short startup script for non-technical people.                                    |
:: | It (should) start the current working version of the tool.                                  |
:: | This script will (probably) be depricated and removed from later version of the repository. |
:: +---------------------------------------------------------------------------------------------+

:: +--------------------------+
:: | Become an Administrator. |
:: +--------------------------+

setlocal DisableDelayedExpansion
set "batchPath=%~0"
for %%k in (%0) do set batchName=%%~nk
set "vbsGetPrivileges=OEgetPriv_%batchName%.vbs"
setlocal EnableDelayedExpansion

:checkPrivileges
NET FILE 1>NUL 2>NUL
IF ERRORLEVEL 1 ( goto GetAdminPrivileges ) else ( goto HaveAdminPrivileges )
:GetAdminPrivileges
ver > nul
if '%1'=='ELEV' (echo ELEV & shift /1 & goto gotPrivileges)
ECHO **************************************
ECHO Invoking UAC for Privilege Escalation
ECHO **************************************
ECHO Set UAC = CreateObject^("Shell.Application"^) > "%vbsGetPrivileges%"
ECHO args = "ELEV " >> "%vbsGetPrivileges%"
ECHO For Each strArg in WScript.Arguments >> "%vbsGetPrivileges%"
ECHO args = args ^& strArg ^& " "  >> "%vbsGetPrivileges%"
ECHO Next >> "%vbsGetPrivileges%"
ECHO UAC.ShellExecute "!batchPath!", args, "", "runas", 1 >> "%vbsGetPrivileges%"
"%SystemRoot%\System32\WScript.exe" "%vbsGetPrivileges%" %*
rem TODO: Need to get back to original folder some how.
exit /B
:HaveAdminPrivileges
ECHO ******************
ECHO Have UAC Privilege
ECHO ******************

:: When an admin the default dir is not the script dir.
:: Correcting that.
cd %~dp0

:: +------------------------+
:: | Go to working location |
:: +------------------------+
cd scriptTemp

:InstallPrereqs
ECHO.
ECHO.
ECHO +----------------------------------------+
ECHO * Install and setup Prerequsit Packages. *
ECHO +----------------------------------------+
ECHO * Python 2.7
ECHO * Python 3.6 x64
ECHO * LEAP motion SDK

:CheckIfPython2
IF EXIST C:\Python27 GOTO EnsurePython2Setup
:InstallPython2
ECHO.
ECHO **
ECHO * Installing Python 2.7
ECHO **
python-2.7.15.msi /passive /norestart TARGETDIR=C:\Python27\ ACTION=INSTALL
:EnsurePython2Setup
ECHO.
ECHO **
ECHO * Seting up Python 2.7
ECHO **
C:\Python27\python.exe -m ensurepip -U --default-pip
C:\Python27\python.exe -m pip install --upgrade pip
:DonePython2

:CheckIfPython3
IF EXIST "C:\Program Files\Python36\" GOTO EnsurePython3Setup
:InstallPython3
ECHO.
ECHO **
ECHO * Installing Python 3.6 x64
ECHO **
:: c:\Python27\python.exe -c "import urllib;urllib.urlretrieve('https://www.python.org/ftp/python/3.7.0/python-3.7.0.exe', 'python-3.7.0.exe')"
python-3.6.0-amd64.exe InstallAllUsers=1 TargetDir="C:\Program Files\Python36" /passive
:EnsurePython3Setup
ECHO.
ECHO **
ECHO * Seting up Python 3.6 x64
ECHO **
"C:\Program Files\Python36\python.exe" -m ensurepip -U --default-pip
"C:\Program Files\Python36\python.exe" -m pip install --upgrade pip
:DonePython3


:CheckIfLEAP
IF EXIST "C:\Program Files\Leap Motion" GOTO EnsureLEAPSetup
:InstallLEAP
ECHO.
ECHO **
ECHO * Installing LEAP Motion Drivers
ECHO **
Leap_Motion_Setup_4.0.0.exe /passive
:EnsureLEAPSetup
ECHO.
ECHO **
ECHO * Seting up LEAP Motion
ECHO **
:: TODO?

ECHO.
ECHO.
ECHO +----------------------------+
ECHO * Installing Python Librarys *
ECHO +----------------------------+
ECHO.
ECHO **
ECHO * Python2 Libs
ECHO **
C:\Python27\python.exe -m pip install --upgrade -r ../requirements2.txt
ECHO.
ECHO **
ECHO * Python3 Libs
ECHO **
"C:\Program Files\Python36\python.exe" -m pip install --upgrade -r ../requirements3.txt

pause




