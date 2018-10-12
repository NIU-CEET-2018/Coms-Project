@echo off
cls

:: +---------------------------------------------------------------------------------------------+
:: | This is a short startup script for non-technical people.                                    |
:: | It (should) start the current working version of the tool.                                  |
:: | This script will (probably) be depricated and removed from later version of the repository. |
:: +---------------------------------------------------------------------------------------------+

:: When an admin the default dir is not the script dir.
:: Correcting that.
cd %~dp0

"C:\Python27\python.exe" Leap_asl_Andrew_Windows\Leap_Reader.py

