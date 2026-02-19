# CSA - Sistema di Indicatori di Performance per i Rilevatori (RPI - Rilevatori Performance Indicatori)

## 📋 Overview
RPI is an automated data pipeline designed to ingest quarterly performance metrics for field interviewers (Rilevatori), process key performance indicators (KPIs), and distribute personalized HTML reports via SMTP.

The system supports two primary survey streams:
* **FOL** (Forze di Lavoro)
* **SPESE** (Consumi delle famiglie)

## 🏗 Architecture
The project follows a modular "Engine" architecture to ensure maintainability:

* **Data Layer**: Handles raw Excel/CSV ingestion via Pandas.
* **Logic Layer**: Processes raw metrics (rounding, scaling, and validation).
* **Presentation Layer**: Decoupled Jinja2 HTML templates for dynamic email generation.
* **Quality Assurance**: Unit tests for transformation logic and email validation.

## 🚀 Getting Started

### 1. Prerequisites
* Python 3.9+
* Access to an SMTP server (e.g., Outlook/Office365 or Gmail)

### 2. Installation
```bash
git clone <https://github.com/Avinash-patnaik/csa-interviewer-performance-automation.git>
cd csa-interviewer-performance-automation
pip install -r requirements.txt