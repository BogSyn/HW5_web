# Домашнє завдання #5

<h1>Опис:</h1>

<b>Основна частина:</b> файл <b>main.py<b> повертає курс EUR та USD ПриватБанку
Виконано обмеження в по дням — остання 10 днів.

<b>Приклад:</b> 

py .\main.py - виводить курс валют: долар США; євро за поточний день

py .\main.py 3 - виводить за три дні

<b>Додаткова частина:</b>
Додана можливість вибору, через передані параметри консольної 
утиліти, додаткових валют у відповіді програми  

<b>Приклад:</b> 

py .\main.py 2 PZL CHF - виводить курс валют: долар США; євро; польський злотий; швейцарський франк за два дні

Файл <b>web_server.py<b> запускає серверну частину чату

Введення в чаті команди <b>exchange<b> показує користувачам поточний курс валют у текстовому форматі

Після виконання команди <b>exchange<b> створюється(або дописується) файл <b>currency_log.txt<b> 

<b>Приклад:</b>

<b>exchange<b> - виводить курс валют: долар США; євро за поточний день

<b>exchange 6 PZL CHF<b> - виводить курс валют: долар США; євро; польський злотий; швейцарський франк за шість днів



