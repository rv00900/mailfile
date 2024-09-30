import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import pandas as pd
import streamlit as st
from io import StringIO

def send_internal_email(subject, body, to_email, attachments=None):
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587
    from_email = "rsingh@quantboxtrading.com"
    password = "9984241799aA@#"
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'html'))  
    if attachments:
        for file_path in attachments:
            try:
                with open(file_path, 'rb') as f:
                    part = MIMEBase('application', 'octet-stream')
                    part.set_payload(f.read())
                encoders.encode_base64(part)
                filename = file_path.split('/')[-1]
                part.add_header(
                    'Content-Disposition',
                    f'attachment; filename={filename}',
                )
                msg.attach(part)
            except Exception as e:
                print(f"Failed to attach file {file_path}: {e}")
    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(from_email, password)
        server.send_message(msg)
        print("Email sent successfully!")
        #st.write("Email sent successfully!")
    except smtplib.SMTPAuthenticationError:
        print("Failed to authenticate. Check your email and password.")
    except Exception as e:
        print(f"Failed to send email: {e}")
        st.write('Failed to send email')
    finally:
        server.quit()
st.title("CSV File Checker")
uploaded_file1 = st.file_uploader("Choose the left_CSV file", type="csv")
uploaded_file2 = st.file_uploader("Choose the right_CSV file", type="csv")
if uploaded_file1 is not None and uploaded_file2 is not None:
    df1 = pd.read_csv(uploaded_file1)
    df2 = pd.read_csv(uploaded_file2)
    if df1.equals(df2):
        st.success("Files are identical")
    else:
        st.warning("Files are different")
        diff = df1.merge(df2, indicator=True, how='outer')
        diff = diff[diff['_merge'] != 'both']
        st.write("Differences:")
        st.dataframe(diff)
        df = diff.head(5)
        df_html = df.to_html(index=False)
        diff.to_csv("data.csv")  
        attachments = ["data.csv"]
        title = st.text_input("Enter_Subject")
        st.write("Subject", title)
        if st.button("Send Email"):
            send_internal_email(
                subject=f'{title}',
                body=df_html,
                to_email="quantbox7@gmail.com",
                attachments=attachments
            )
            st.success("Email sent successfully!")
        else:
            st.warning("Please enter a subject for the email.")
