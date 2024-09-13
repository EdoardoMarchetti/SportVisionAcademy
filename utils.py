# Helper function to validate email
import re
import streamlit as st


def is_valid_email(email):
    """Validates an email address using regex."""
    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(email_regex, email)

# Helper function to validate phone number
def is_valid_phone(phone):
    """Validates a phone number with country code using regex."""
    phone_regex = r'^\+\d{1,3}\d{7,14}$'  # Example: +39xxxxxxxxxx
    return re.match(phone_regex, phone)

# Check if all fields are valid
def are_personal_details_valid():
    """Checks if personal details (email and phone) are valid."""
    if not is_valid_email(st.session_state['Email']):
        st.warning("Inserisci un'email valida.")
        return False
    if not is_valid_phone(st.session_state['Telefono']):
        st.warning("Inserisci un numero di telefono valido (includi prefisso es. +39).")
        return False
    return True