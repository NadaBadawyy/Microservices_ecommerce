@echo off
echo ==========================================
echo      E-COMMERCE DATABASE REPAIR TOOL
echo ==========================================
echo.
echo 1. Dropping existing tables (clearing bad schema)...
python drop_tables.py

echo.
echo 2. Removing old migration files...
if exist migrations (
    rd /s /q migrations
    echo    - Migrations folder deleted.
) else (
    echo    - No migrations folder found.
)

echo.
echo 3. Initializing new migrations (matching current code)...
set FLASK_APP=manage.py
flask db init
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Flask db init failed.
    pause
    exit /b
)

echo.
echo 4. Generating migration script...
flask db migrate -m "Reset schema to match models"
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Flask db migrate failed.
    pause
    exit /b
)

echo.
echo 5. Applying new schema to database...
flask db upgrade
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Flask db upgrade failed.
    pause
    exit /b
)

echo.
echo 6. Seeding database with initial data...
python setup_database.py
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Seeding failed.
    pause
    exit /b
)

echo.
echo ==========================================
echo      DATABASE REPAIR COMPLETE!
echo ==========================================
echo.
echo You may now restart your services.
pause
