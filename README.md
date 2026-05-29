# Projekt: Mikroserwisy (Nginx Proxy + Logowanie JWT)

Prjekt zaliczeniowy z 2 przedmiotów:

Wsparcie tworzenia aplikacji internetowych - Serwer Proxy z Nginx dla dwóch aplikacji w tej samej sieci

Techniki integracji aplikacji internetowych - Mikroserwisowy system logowania (REST + Docker) rozdzielony na kontenery

## Architektura i wymagania

Brama wejściowa (port 80), rozdziela ruch na podstawie URL

Osobny kontener obsługujący tylko logowanie i generowanie tokenów JWT

Główna aplikacja w osobnym kontenerze, chroniona tokenem JWT

Kontenery bazują na obrazach alpine

## Konfiguracja
Przed startem należy utworzyć w głownym folderze plik .env z danymi jak: 

SECRET_KEY=super_tajny_klucz_jwt

ADMIN_USER=admin

ADMIN_PASS=haslo123


## Budowanie
docker compose up -d --build

Główny moduł http://localhost/main

Moduł autoryzacji http://localhost/auth/login
