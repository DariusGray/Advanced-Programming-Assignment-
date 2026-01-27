# FTP-Based Clinical Data Management System

## Overview
This project is a Python-based clinical data validation and archival system developed for Port Avalon General Hospital (PAGH). The system securely retrieves CSV files from a legacy FTP server, validates them against strict data integrity rules, and routes them to appropriate storage locations. A graphical user interface (GUI) is provided to support visual workflow preferences for medical analysts.

The solution is containerized using Docker and follows modern software engineering practices including Test-Driven Development (TDD), automation, design patterns, and CI/CD.

---

## Key Features
- Secure FTP connection management with visual connection status
- Graphical user interface built using Tkinter
- Sequential CSV validation with detailed error reporting
- Automatic file routing:
  - Valid files → Archive directory (timestamped)
  - Invalid files → Errors directory (logged with GUIDs)
- Duplicate file prevention using processed-file tracking
- External UUID API integration with fallback mechanism
- Fully containerized deployment using Docker and Docker Compose
- CI/CD pipeline using GitHub Actions

---

## Validation Rules
Each CSV file is validated against the following rules:

- Filename format: `CLINICALDATA_YYYYMMDDHHMMSS.csv`
- Correct header structure (9 required fields)
- Positive integer dosage values
- Valid date format (`YYYY-MM-DD`)
- StartDate must precede EndDate
- Outcome must be one of:
  - `Improved`
  - `No Change`
  - `Worsened`
- Mandatory fields must not be empty
- Duplicate records within a file are detected
- Corrupted or malformed CSV files are rejected

---
## Project Structure
```
.
├── main.py # Application entry point
├── gui.py # Tkinter GUI implementation
├── ftp_client.py # FTP Facade (OOP design pattern)
├── validator.py # CSV validation logic
├── logger.py # Error logging with UUID API
├── config.py # Configuration and directory setup
├── tests/ # Unit and integration tests
├── scripts/ # Automated Scripts for FTP Connection Check and Validation
├── Dockerfile # Docker image definition
├── docker-compose.yml # Container configuration
└── README.md # Project documentation
```


---

## Running the Application with Docker

### Prerequisites
- Docker
- Docker Compose
- X server (e.g. Xming on Windows)

### Steps
```bash
docker compose pull
docker compose up
```
Docker Compose applies all configuration defined in docker-compose.yml, including environment variables and volume mappings. The Tkinter GUI is rendered on the host display using the DISPLAY environment variable.

### Graphical User Interface

The interface is divided into:
- Connection Panel – manage FTP connections
- Server Browser – search and select CSV files
- Workspace Panel – validate and process files
- Activity Feed – real-time system feedback
The design follows Nielsen’s usability heuristics, ensuring clarity, consistency, and meaningful error feedback.

### Testing Strategy

The project follows the Test Pyramid approach:
- Unit tests for validation rules
- Integration tests for UUID API and logging
- End-to-end testing via GUI interaction
TDD was applied using the Red–Green–Refactor cycle during development.

### Automation and CI/CD
- Automated scripts generate valid and invalid CSV files for testing
- FTP connectivity checks are automated
- GitHub Actions pipeline performs:
  - Automated testing
  - Container build
  - Image publishing to GitHub Container Registry (GHCR)

### Technologies Used
- Python 3
- Tkinter
- ftplib
- Docker & Docker Compose
- Git & GitHub
- GitHub Actions
- UUIDTools API

### Author
#### Kaung Nyi Hein
ATHE Level 4 Extended Diploma in Computing

Unit 11 – Advanced Programming
