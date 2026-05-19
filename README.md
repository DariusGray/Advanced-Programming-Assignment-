<<<<<<< HEAD
# [cite_start]FTP-Based Clinical Data Management System [cite: 400]
### [cite_start]🏥 Port Avalon General Hospital (PAGH) · Data Integrity & Archival Solution [cite: 486]

[cite_start]An enterprise-grade, Python-based application engineered to validate clinical data for Port Avalon General Hospital (PAGH)[cite: 486, 487]. [cite_start]The system connects seamlessly to an FTP server, downloads available CSV datasets, rigorously validates them against a predefined rule engine, and displays transparent results through a custom graphical user interface (GUI)[cite: 487]. 

[cite_start]The codebase was architected by combining imperative, object-oriented, and functional programming paradigms to solve complex real-world data workflows[cite: 488].

---

## 🚀 Key Features & Capabilities

* [cite_start]**Intuitive Desktop GUI:** Features a Tkinter-based universal console designed strictly around Human-Computer Interaction (HCI) principles and Nielsen’s heuristic guidelines[cite: 583, 585].
* [cite_start]**Intelligent File Routing:** Automatically validates CSV files and routes them into dedicated, user-defined storage directories (e.g., Archive, Errors)[cite: 487, 707].
* [cite_start]**Resilient API Logging:** Invalid entries are quarantined and logged using unique identifiers (GUIDs) fetched from an external UUID API (UUIDTools)[cite: 615, 658]. [cite_start]If the API is ever unreachable, the system automatically falls back to a deterministic, timestamp-based local identifier[cite: 659].
* [cite_start]**Advanced Design Patterns:** Implements the Facade design pattern via the `FTPClient` class to securely encapsulate sensitive connection details and abstract low-level FTP processes from the rest of the application[cite: 602, 604].
* [cite_start]**Robust Automation:** Includes standalone automation scripts that seamlessly verify FTP access credentials and programmatically generate both valid and invalid mock CSV files for continuous validation testing[cite: 624, 631, 634].

---

## 🛠️ Modern Software Engineering Practices

This project prioritizes maintainability, continuous testing, and modern deployment standards:

* [cite_start]**Test-Driven Development (TDD):** The core validation logic was strictly developed using the "Red-Green-Refactor" cycle[cite: 552]. [cite_start]The testing architecture mirrors the Test Pyramid, heavily utilizing Pytest for unit tests, alongside deeper integration and end-to-end tests[cite: 572, 574, 575, 735].
* [cite_start]**CI/CD Pipeline:** Fully integrated with GitHub Actions to automate Continuous Integration and Continuous Delivery[cite: 726]. [cite_start]Every push or pull request automatically triggers dependency installation and unit testing[cite: 727, 735]. [cite_start]Upon passing, a Docker image is built and continuously deployed to the GitHub Container Registry (GHCR)[cite: 731, 740].
* [cite_start]**Agile Workflow:** Development was meticulously tracked using Agile incremental development strategies and a Trello Kanban board[cite: 756, 761].

---

## 📐 Clinical Validation Ruleset

[cite_start]To ensure strict data integrity, every ingested payload must clear the following deterministic rules[cite: 487]:

| Feature | Validation Rule |
| :--- | :--- |
| **File Identity** | [cite_start]Filenames must begin with the `CLINICALDATA_` prefix[cite: 765]. |
| **Schema** | [cite_start]Each record row must contain exactly 9 columns[cite: 567]. |
| **Completeness** | [cite_start]Mandatory fields (PatientID, TrialCode, DrugCode, Outcome, SideEffects, Analyst) cannot be empty[cite: 562]. |
| **Metrics** | [cite_start]The medication dosage amount must be a strictly positive integer[cite: 642]. |
| **Temporal Logic** | [cite_start]The chronological `StartDate` must strictly occur before the `EndDate`[cite: 642]. |
| **Date Standard** | [cite_start]All temporal fields must follow the standard `YYYY-MM-DD` format[cite: 642]. |
| **Categorical** | [cite_start]The outcome field is restricted to specific allowed values: `Improved`, `No Change`, or `Worsened`[cite: 642]. |
| **Idempotency** | [cite_start]The system natively detects and rejects duplicate records within a single file[cite: 642]. |

---

## 🐳 Containerized Deployment

[cite_start]The entire system is packaged as a highly portable Docker container[cite: 700]. [cite_start]To ensure critical files persist beyond the container's lifecycle, Docker Compose is utilized to map the `Archive`, `Errors`, `temp`, and internal log files to local host volumes[cite: 707, 708]. 

[cite_start]Because this is a visual application, the Dockerized GUI renders securely onto your host machine using the `DISPLAY` environment variable alongside an X11 runtime environment (like Xming)[cite: 711, 718].

### Running the Application

1. **Pull the latest built image from GHCR:**
   ```bash
   docker compose pull
   ```
   (Ensure you are running this in the directory containing the `docker-compose.yml` file).

2. **Spin up the containerized system:**
    `docker compose up`
    (Note: Ensure your local X Server is running and properly configured to accept connections from the Docker runtime before launching.)
