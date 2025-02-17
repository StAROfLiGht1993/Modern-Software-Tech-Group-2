setlocal enabledelayedexpansion

cd /d "%~dp0"

echo Deleting migrations folder...
rmdir /s /q migrations

echo Initializing Alembic migrations...
alembic init migrations

set file=migrations\env.py
set tempfile=temp.txt

:: Set the search term and replacement block
set "search=target_metadata = None"
set "replace1=from app.db.db import Base"
set "replace2=from app.models.auction import Auction"
set "replace3=from app.models.card import Card"
set "replace4=from app.models.profile import Profile"
set "replace5=target_metadata = Base.metadata"

:: Clear tempfile
echo. > %tempfile%

:: Read the env.py file and replace the specific line
(for /f "delims=" %%i in (%file%) do (
    set line=%%i
    if "!line!"=="%search%" (
        echo %replace1%>>%tempfile%
        echo %replace2%>>%tempfile%
        echo %replace3%>>%tempfile%
        echo %replace4%>>%tempfile%
        echo %replace5%>>%tempfile%
    ) else (
        echo !line!>>%tempfile%
    )
)) 

:: Move the tempfile back to env.py
move /y %tempfile% %file%


echo Creating Alembic revision for Auction App...
alembic revision --autogenerate -m "Init Auction App"

alembic upgrade head

uvicorn app.main:app --reload

pause