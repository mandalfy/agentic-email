import streamlit as st
from main import process_and_send_email

# Streamlit UI
st.title("AI Email Agent")

# Input fields
recipient_name = st.text_input("Recipient's Name")
recipient_email = st.text_input("Recipient's Email Address")
email_subject = st.text_input("Email Subject")
uploaded_file = st.file_uploader("Upload a PDF (Optional)", type=["pdf"])

# Send email button
if st.button("Send Email"):
    if not (recipient_name and recipient_email and email_subject):
        st.error("Please provide the recipient's name, email address, and subject.")
    else:
        with st.spinner("Processing and sending email..."):
            try:
                process_and_send_email(recipient_name, recipient_email, email_subject, uploaded_file)
                st.success("Email sent successfully!")
            except Exception as e:
                st.error(f"Failed to send email: {str(e)}")