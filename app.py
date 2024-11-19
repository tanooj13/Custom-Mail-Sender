import streamlit as st
import pandas as pd
from email_utils import schedule_emails, start_scheduler
from email_status_db import get_log_details

# Start the email scheduler
start_scheduler()

# Set the app title
st.title("Custom Email Sender")

#  Upload CSV File
st.header("Upload Recipient Data")
# Allow the user to upload a CSV file containing recipient details
uploaded_file = st.file_uploader("Upload a CSV file containing recipient details (e.g., Name, Email, Company):", type=["csv"])

if uploaded_file:
    # Read and display the uploaded CSV file
    data = pd.read_csv(uploaded_file)
    st.write("Uploaded Data:")
    st.dataframe(data)

# Email Configuration
st.header("Email Configuration")
# Input fields for sender email and password
sender_email = st.text_input("Sender Email", help="Enter the email address from which emails will be sent.")
sender_password = st.text_input("Sender Password", type="password", help="Enter the password for the sender email.")

# Input fields for email subject and body template with placeholders
email_subject = st.text_input("Email Subject", "Hello {Name}!", help="Use placeholders like {Name}, {Company}, etc.")
email_body_template = st.text_area(
    "Email Body Template",
    "Dear {Name},\n\nWe are excited to connect with you from {Company}.\n\nBest regards,\n[Your Name]",
    help="Use placeholders like {Name}, {Company}, etc."
)

# Email Scheduling Options
st.header("Schedule your mails")
# Input fields for scheduling date, time, and throttle rate (emails per minute)
schedule_date = st.date_input("Schedule Date", help="Select the date to send the emails.")
schedule_time = st.time_input("Schedule Time (24-hour format)", help="Select the exact time for sending emails.")
throttle_rate = st.slider("Throttle Rate (Emails per minute)", min_value=1, max_value=60, value=10, help="Emails sent per minute.")

# Button to schedule emails
if st.button("Schedule Emails"):
    # Validate inputs before scheduling emails
    if uploaded_file is None:
        # Error message if no file is uploaded
        st.error("Please upload a CSV file.")
    elif not sender_email or not sender_password:
        # Error message if sender email or password is missing
        st.error("Please enter the sender email and password.")
    elif not email_subject or not email_body_template:
        # Error message if email subject or body template is missing
        st.error("Please provide both subject and body templates.")
    else:
        # If all inputs are valid, schedule the emails
        st.info("Scheduling emails, please wait...")
        schedule_datetime = f"{schedule_date} {schedule_time}"
        # Call the `schedule_emails` function to handle the scheduling
        success = schedule_emails(
            data,
            sender_email,
            sender_password,
            email_subject,
            email_body_template,
            schedule_datetime,
            throttle_rate
        )
        if success:
            # Success message after scheduling emails
            st.success(f"Emails scheduled successfully for {schedule_datetime}!")

# Display Logs Section
st.header("Email Delivery Logs")
# Button to view email delivery logs
if st.button("View Logs"):
    # Fetch and display email delivery logs
    logs = get_log_details()
    st.write("Email Delivery Log:")
    st.dataframe(pd.DataFrame(logs))

