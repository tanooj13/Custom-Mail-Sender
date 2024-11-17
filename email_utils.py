import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import requests
from datetime import datetime, timedelta
import threading
import time
from queue import Queue
import streamlit as st
import pandas as pd
from email_status_db import log_email_status

# Groq API Configuration
# API key and URL for the Groq service
GROQ_API_KEY = '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'
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"

# Queue for managing email tasks
email_queue = Queue()

# Function to generate the email body using the Groq API
def generate_email_body(prompt_template, data_row):
    try:
        # Fill the template with row data and send the prompt to Groq API
        filled_prompt = "Just give the body of the mail for the following prompt in 8 lines\n with best regards containing the name of the sender" + prompt_template.format(**data_row)
        response = requests.post(
            GROQ_API_URL,
            json={
                "model": "mixtral-8x7b-32768",
                "messages": [{"role": "user", "content": filled_prompt}],
                "max_tokens": 150,
                "temperature": 0.7
            },
            headers={"Authorization": f"Bearer {GROQ_API_KEY}"}
        )

        # Check API response and return generated content
        if response.status_code == 200:
            generated_body = response.json()["choices"][0]["message"]["content"].strip()
            return generated_body
        else:
            # Log error message if API call fails
            st.error(f"Error from Groq API: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        # Handle exceptions during API call
        st.error(f"An error occurred: {e}")
        return None

# Function to schedule emails for later sending
def schedule_emails(data, sender_email, sender_password, email_subject, email_body_template, schedule_datetime, throttle_rate):
    try:
        # Parse the scheduled datetime
        schedule_dt = datetime.strptime(schedule_datetime, "%Y-%m-%d %H:%M:%S")
        for _, row in data.iterrows():
            # Extract email details and add to the queue
            recipient_email = row["Email"]
            subject = email_subject.format(**row.to_dict())
            body_template = email_body_template.format(**row.to_dict())

            # Enqueue the email task with the schedule time
            email_queue.put((schedule_dt, sender_email, sender_password, recipient_email, subject, body_template))

        # Add throttle rate to the queue for processing
        email_queue.put(("THROTTLE_RATE", throttle_rate))
        return True
    except Exception as e:
        # Log errors during scheduling
        st.error(f"An error occurred while scheduling emails: {e}")
        return False

# Function to process and send emails from the queue
def process_queue():
    throttle_rate = 10  # Default throttle rate
    while True:
        try:
            if not email_queue.empty():
                # Get the next email task
                item = email_queue.get()
                if item[0] == "THROTTLE_RATE":
                    # Update throttle rate if applicable
                    throttle_rate = item[1]
                    continue

                # Extract task details
                schedule_time, sender_email, sender_password, recipient_email, subject, body_template = item
                now = datetime.now()

                if schedule_time <= now:
                    # Generate email body using the template
                    body = generate_email_body(body_template, {"Email": recipient_email})
                    if body:
                        # Send the email if the body is successfully generated
                        send_email(sender_email, sender_password, recipient_email, subject, body)
                    time.sleep(60 / throttle_rate)  # Throttle the sending rate
                else:
                    # Requeue the task if it's not time yet
                    email_queue.put(item)
                    time.sleep(1)  # Wait before rechecking the queue
            else:
                # If the queue is empty, wait before checking again
                time.sleep(1)
        except Exception as e:
            # Log errors during queue processing
            st.error(f"Error in processing queue: {e}")

# Function to send an email
def send_email(sender_email, sender_password, recipient_email, subject, body):
    try:
        # Configure the SMTP server
        smtp_server = "smtp.gmail.com"
        smtp_port = 587

        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()  # Start TLS encryption
            server.login(sender_email, sender_password)  # Log in to the email server

            # Create the email message
            message = MIMEMultipart()
            message["From"] = sender_email
            message["To"] = recipient_email
            message["Subject"] = subject
            message.attach(MIMEText(body, "plain"))

            # Send the email
            server.send_message(message)

        # Log the email status as "Sent"
        log_email_status(recipient_email, subject, "Sent")
    except Exception as e:
        # Log errors and update email status as "Failed"
        st.error(f"Error sending email to {recipient_email}: {e}")
        log_email_status(recipient_email, subject, "Failed")

# Function to start the email scheduler in a separate thread
def start_scheduler():
    threading.Thread(target=process_queue, daemon=True).start()
