# Urochomienie i obsługiwanie projektu stacji meteorologicznej w Raspberry PI

## 1. Połączenie się do Raspberry PI
użytkownik: pi

hasło: test123
### 1.1 Połączenie się po ssh
Sprawdzenie jaki adres ip ma Raspberry PI (przykładowo adres_sieci=192.168.1.0, maska=24):
```bash
$ sudo nmap adres_sieci/maska
```
Po sprawdzeniu dostępnych adresów IP trzeba znaleźć IP dla Raspberry PI i uruchomić poniższą komendę.
```bash
$ ssh pi@adres_ip_raspberry_pi
```
Poprosi o hasło - należy wpisać "test123".

Po zalogowaniu się powinno przenieść do Raspberry PI :
- w konsoli jest: pi@raspberrypi:~ $
- bezwzględna ścieżka to /home/pi

## 2. Uruchomianie aplikacji webowej

### 2.1 Uruchomienie wirtualnego środowiska
W głównym folderze (/home/pi):
```bash
pi@raspberrypi:~ $ source env/bin/activate
```
Powinno wyświetlić się środowisko witrualne: (env) pi@raspberrypi:~ $ 

### 2.2 Uruchomienie aplikacji webowej
W głównym folderze (/home/pi)w środowisku wirtualnym:
```bash
(env) pi@raspberrypi:~ $ cd weather_station/
(env) pi@raspberrypi:~/weather_station $ python manage.py runserver 0.0.0.0:1234
```
Podany port (1234) jest portem przykładowym, można użyć dowolnie innego. 

Po uruchomieniu serwera, należy otworzyć w przeglądarce: http://adres_ip_raspberry_pi:port/
- np: "http://192.168.1.140:1234/".

Żby zakończyć działanie serwera należy wcisnąć CTRL C w konsoli, następnie można wyjść ze środowiska wirtualnego wpisując "deactivate".

## 3. Uruchomienie skryptu zapisującego pojedynczy pomiar do bazy danych
Standardowo skrypt ten jest uruchamiany automatycznie co godzinę, więc nie ma potrzeby uruchamiania go ręcznie. Jednak, jeśli na potrzeby demonstracji chce się zrobić jeden pomiar (odczytać dane z czujników), zwalidować je (sprawdzić czy nie ma pomiarów znacznie odstających od normy) oraz wczytać do bazy danych PotgreSQL należy postępować według poniższych instrukcji:

### 3.1 Uruchomianie wirtualnego środowiska
Jeśli jest się w wirtualnym środowisku od aplikacji webowej należy z niego wyjść komendą "deactivate".

W głównym folderze (cd /home/pi):
```bash
pi@raspberrypi:~ $ cd data/
pi@raspberrypi:~/data $ source env/bin/activate
```
Powinno wyświetlić się środowisko witrualne: (env) pi@raspberrypi:~/data $

### 3.2 Uruchomienie skryptu zapisującego pojedynczy pomiar: sensors_measurements.py
W folderze "data" (/home/pi/data/), w środowisku wirtualnym:
```bash
(env) pi@raspberrypi:~/data $ cd data_project/
(env) pi@raspberrypi:~/data/data_project $ python sensors_measurements.py 
```
## 4. Uruchomienie skryptu pokazującego aktualne wskazania czujników (w nieskończonej pętli)
Jeśli nie jesteś w środowisku wirtualnym uruchamianym z folderu "data" (/home/pi/data/), należy wykonać punkt 3.1.

W folderze "data" (cd /home/pi/data):
```bash
(env) pi@raspberrypi:~/data $ python scrapper.py 
```
## 5. Połączenie się z bazą danych PostgreSQL i pokazanie danych z tabeli
W głównym folderze (cd /home/pi) bez środowiska wirtualnego (komenda "deactivate"):
### 5.1 Zalogowanie się po PostgreSQL jako użytkownik "postgres"
```bash
pi@raspberrypi:~ $ sudo -u postgres psql
```
### 5.2 Połączenie się z bazą danych "mydb"
```bash
postgres=# \c mydb
```
### 5.3. Wylistowanie dostępnych tabel
```bash
mydb=# \dt
```
### 5.3. Wyświetlenie wszystkich rekordów z tabeli dat_weatherdata (tabela z danymi z czujników)
```bash
mydb=# SELECT * FROM data_weatherdata;
```
