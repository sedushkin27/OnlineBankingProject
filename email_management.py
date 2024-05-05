import smtplib  # Import the smtplib library to send emails
from email.message import EmailMessage  # Import the EmailMessage class to create the email message

# Set the sender and password for the email account
sender = ''  # Enter the email address of the sender here
password = ''  # Enter the password for the email account here

def send_email(recipient, massage):
    # Create an SMTP object for the Gmail server and specify the port number
    server = smtplib.SMTP("smtp.gmail.com", 587)

    # Enable encryption using the starttls() method
    server.starttls()

    try:
        # Log in to the email account using the sender and password
        server.login(sender, password)

        # Send the email to the recipient with the specified massage
        server.sendmail(sender, recipient, massage)

        # Return a success message
        return 'message sent'
    except Exception as _ex:
        # Return an error message if there is a problem sending the email
        return f'{_ex} you may not have entered a login and password in email_management.py '
