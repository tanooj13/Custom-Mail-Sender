# Custom Email Scheduler Application

This project is a **Custom Email Scheduler** application that allows users to schedule and send personalized emails using a CSV file of recipient details. The system supports email body generation using the **Groq API**, logs email statuses in a SQLite database, and provides real-time logs for email delivery.

---

## Table of Contents
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [File Structure](#file-structure)
- [Configuration](#configuration)
- [Technologies Used](#technologies-used)
- [License](#license)

---

## Features

- **Upload CSV File**: Easily upload recipient details with columns like `Name`, `Email`, `Company`, etc.
- **Dynamic Email Body**: Generate personalized email bodies using the Groq API.
- **Email Scheduling**: Specify date, time, and throttle rate for email delivery.
- **Real-Time Logging**: Track email delivery status and view logs in real time.
- **SQLite Database**: Logs email statuses, including whether emails are sent or opened.
- **Multi-threading**: Ensures smooth scheduling and queue processing.

---

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/<username>/email-scheduler.git
   cd email-scheduler
   ```

2. Create a virtual environment and activate it:
   ```bash
   python -m venv venv
   source venv/bin/activate   # On Windows: venv\Scripts\activate
   ```

3. Install required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up the database:
   ```bash
   python email_status_db.py
   ```

---

## Usage

1. Run the Streamlit application:
   ```bash
   streamlit run app.py
   ```

2. Navigate to the provided local URL in your browser.

3. Follow the steps in the UI:
   - Upload a CSV file.
   - Configure email details and templates.
   - Set scheduling parameters.
   - View email delivery logs.

---

## File Structure

```plaintext
email-scheduler/
├── app.py                 # Main Streamlit application
├── email_utils.py         # Contains email scheduling, generation, and queue processing logic
├── email_status_db.py     # Handles SQLite database operations for email logs
├── requirements.txt       # Python dependencies
├── README.md              # Documentation
└── email_status.db        # SQLite database (auto-created on initialization)
```

---

## Configuration

### Groq API
- The Groq API key and URL are configured in `email_utils.py`:
  ```python
  GROQ_API_KEY = 'your_groq_api_key_here'
  GROQ_API_URL = 'https://api.groq.com/openai/v1/chat/completions'
  ```
- Replace `your_groq_api_key_here` with your actual Groq API key.

### SMTP Settings
- The SMTP server for Gmail is used by default in `email_utils.py`:
  ```python
  smtp_server = "smtp.gmail.com"
  smtp_port = 587
  ```
- Update these values if using a different email provider.

---

## Technologies Used

- **Streamlit**: Frontend framework for building interactive web apps.
- **Python Libraries**:
  - `smtplib`: For sending emails.
  - `sqlite3`: For database operations.
  - `requests`: For interacting with the Groq API.
  - `pandas`: For processing CSV data.
  - `threading`: For background email scheduling.
- **SQLite**: Lightweight database for logging email delivery statuses.


---

## License

This project is licensed under the MIT License. You are free to use, modify, and distribute this software in compliance with the license.

---

For contributions or issues, feel free to create a pull request or open an issue on the repository! 🎉
