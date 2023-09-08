# Simple Route Logger

This Python application utilizes Flask, SQLAlchemy, and the Google Maps API to track and manage geographic positions. The web app allows users to retrieve their current latitude and longitude coordinates and save them along with additional location details, reverse geocode the location to retrieve address details, calculate driving distances between positions, and export data as both CSV and PDF files. The code also includes functionality for editing and deleting recorded positions.

## Features

- Web Interface: Provides a user-friendly web interface for inputting and managing geographic positions.
- Reverse Geocoding: Converts latitude and longitude coordinates into detailed address information, including street, house number, town, and postcode.
- Distance Calculation: Calculates driving distances between recorded positions, allowing users to track travel distances.
- Data Export: Offers the capability to export position data as CSV and PDF files for easy sharing and analysis.
- Google Maps Integration: Utilizes the Google Maps API for geolocation services, enhancing accuracy and functionality.
- Editing Positions: Allows users to edit recorded positions, with automatic geocoding to update coordinates based on modified addresses.
- Deletion of Positions: Provides the ability to delete individual positions or clear all positions from the database.
- Time Stamping: Records the date and time of each position entry.
- Time Zone Support: Change the "Europe/Berlin" timezone for accurate timestamping.
- Total Distance Calculation: Computes the total distance traveled based on recorded driving distances.
- Environment Variable Handling: Loads API keys and sensitive information from environment variables for security.
- Cross-Platform: Designed to run on various platforms with the flexibility to adapt to different deployment scenarios.
- Database Integration: Uses SQLAlchemy to manage a SQLite database for storing position data.
- Local Deployment: Supports local deployment for easy setup and testing.

## Dependencies

- Flask: A micro web framework for building web applications.
- Flask-SQLAlchemy: Extension for Flask that simplifies database integration using SQLAlchemy.
- ReportLab: A Python library for creating PDF documents.
- Google Maps Python Client: A client library for accessing the Google Maps API services.
- python-dotenv: A package for loading environment variables from a .env file.
- pytz: A Python package for working with time zones.

## Installation

First, clone this repository to your local machine:

```bash
git clone https://github.com/Timon-Schneider/simple-route-logger.git
```

Then, navigate into the project directory and install the dependencies:

```bash
cd simple-route-logger
pip install -r requirements.txt
```

## Docker Usage

To build and run the application using Docker, execute the following commands:

```bash
cd simple-route-logger
docker compose up -d
```

Once the server is running, you can access the application at [http://localhost:8888](http://localhost:8888) in your web browser.

## Google Maps API key

Rename the file named "dotenv" within the app directory to ".env," and then insert your Google Maps API key into this ".env" file.

## Project Status

This project is currently under development. More features will be added in the future.

---

# Simple Route Logger

Diese Python-Anwendung nutzt Flask, SQLAlchemy und die Google Maps API, um geografische Positionen zu speichern und zu verwalten. Die Webanwendung ermöglicht es den Benutzern, ihre aktuellen Breiten- und Längengradkoordinaten abzurufen und sie zusammen mit zusätzlichen Standortdetails zu speichern, den Standort rückwärts zu geokodieren, um Adressdetails abzurufen, Fahrstrecken zwischen Positionen zu berechnen und Daten sowohl als CSV- als auch als PDF-Dateien zu exportieren. Der Code enthält auch Funktionen zum Bearbeiten und Löschen von aufgezeichneten Positionen.

## Funktionen

- Web-Schnittstelle: Bietet eine benutzerfreundliche Webschnittstelle für die Eingabe und Verwaltung von geografischen Positionen.
- Umgekehrte Geokodierung: Konvertiert Breiten- und Längenkoordinaten in detaillierte Adressinformationen, einschließlich Straße, Hausnummer, Ort und Postleitzahl.
- Entfernungsberechnung: Berechnet die Entfernungen zwischen aufgezeichneten Positionen und ermöglicht es dem Benutzer, Entfernungen zu verfolgen.
- Datenexport: Bietet die Möglichkeit, Positionsdaten als CSV- und PDF-Dateien zu exportieren, damit sie leicht weitergegeben und analysiert werden können.
- Google Maps-Integration: Nutzt die Google Maps API für Geolokalisierungsdienste und verbessert so die Genauigkeit und Funktionalität.
- Bearbeiten von Positionen: Ermöglicht Benutzern die Bearbeitung aufgezeichneter Positionen mit automatischer Geokodierung zur Aktualisierung der Koordinaten auf der Grundlage geänderter Adressen.
- Löschung von Positionen: Bietet die Möglichkeit, einzelne Positionen zu löschen oder alle Positionen aus der Datenbank zu entfernen.
- Zeitstempel: Zeichnet das Datum und die Uhrzeit jedes Positionseintrags auf.
- Unterstützung von Zeitzonen: Ändern Sie die Zeitzone "Europa/Berlin" für eine genaue Zeitstempelung.
- Berechnung der Gesamtdistanz: Berechnet die zurückgelegte Gesamtstrecke auf der Grundlage der aufgezeichneten Fahrstrecken.
- Umgang mit Umgebungsvariablen: Lädt API-Schlüssel und sensible Informationen aus Sicherheitsgründen aus Umgebungsvariablen.
- Plattformübergreifend: Entwickelt für den Einsatz auf verschiedenen Plattformen mit der Flexibilität, sich an unterschiedliche Einsatzszenarien anzupassen.
- Datenbank-Integration: Verwendet SQLAlchemy zur Verwaltung einer SQLite-Datenbank für die Speicherung von Positionsdaten.
- Lokale Bereitstellung: Unterstützt die lokale Bereitstellung zur einfachen Einrichtung

## Abhängigkeiten

- Flask: Ein Micro-Web-Framework zum Erstellen von Webanwendungen.
- Flask-SQLAlchemy: Erweiterung für Flask, die die Datenbankintegration mit SQLAlchemy vereinfacht.
- ReportLab: Eine Python-Bibliothek zur Erstellung von PDF-Dokumenten.
- Google Maps Python Client: Eine Client-Bibliothek für den Zugriff auf die Google Maps API-Dienste.
- python-dotenv: Ein Paket zum Laden von Umgebungsvariablen aus einer .env-Datei.
- pytz: Ein Python-Paket für die Arbeit mit Zeitzonen.

## Installation

Klonen Sie zunächst dieses Repository auf Ihre lokale Maschine:

```bash
git clone https://github.com/Timon-Schneider/simple-route-logger.git
```

Navigieren Sie dann in das Projektverzeichnis und installieren Sie die Abhängigkeiten:

```bash
cd simple-route-logger
pip install -r requirements.txt
```

## Docker-Nutzung

Um die Anwendung mit Docker zu erstellen und auszuführen, führen Sie die folgenden Befehle aus:

```bash
cd simple-route-logger
docker compose up -d
```

Sobald der Server läuft, können Sie die Anwendung in Ihrem Webbrowser unter [http://localhost:8888](http://localhost:8888) aufrufen.

## Google Maps API-Schlüssel

Benennen Sie die Datei "dotenv" im App-Verzeichnis in ".env" um und fügen Sie dann Ihren Google Maps-API-Schlüssel in diese ".env"-Datei ein.

## Projektstatus

Dieses Projekt befindet sich derzeit in der Entwicklung. In Zukunft werden weitere Funktionen hinzugefügt.
