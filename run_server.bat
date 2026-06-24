@echo off
title YAN Cosmetics Local Server
echo ===================================================
echo   YAN Cosmetics - Запуск локального сервера
echo ===================================================
echo.
echo [1/2] Запуск браузера: http://localhost:8000/index.html
start "" "http://localhost:8000/index.html"
echo.
echo [2/2] Запуск сервера Python на порту 8000...
echo (Не закрывайте это окно, пока работаете с сайтом)
echo.
python -m http.server 8000
pause
