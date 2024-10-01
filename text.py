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







######################################################################################################
raw_data = uploaded_file1.read().decode('utf-8')

rows = []
previous_line = ""
count = 0

for line in raw_data.splitlines():
    if line.startswith(("~"," ")):
        previous_line += line  
    else:
        if previous_line:
            rows.append(previous_line)  
        previous_line = line  
        count += 1
        #print(count)


if previous_line:
    rows.append(previous_line)


output_file_path = "1zmerged_client.txt"
with open(output_file_path, "w") as output_file:
    for row in rows:
        output_file.write(row + "\n")

print(f"Merged file created at: {output_file_path}")





#################################################################################################
with open("1zmerged_client.txt", "r") as file:
    raw_data = file.read()

rows_starting_with_tilde = []
count =0
for line in raw_data.splitlines():
    if not line.startswith(("EM","CDK","GLOBE","CGN","LTVOL","BMR","CMS","BMR","CSFL","CQB","CBS","PRO","LTMM")):
        count +=1
        #print(count)
        rows_starting_with_tilde.append(line)



########################################################################################################
with open("1zmerged_client.txt", "r") as file:
    raw_data = file.read()
lines = raw_data.strip().split("\n")
data = [line.split("~") for line in lines]
dr = pd.DataFrame(data)
dr.columns =['Client Code', 'Ucc Code', 'Name', 'Address', 'Pin Code', 'PAN No',
           'Phone No', 'Mobile No', 'Email No', 'Turnover', 'Status',
           'Status Date', 'Registered', 'Branch', 'Sub-Branch', 'Group Code',
           'RMTL Code', 'First Trade', 'Intro by', 'Intro by2', 'Ac Open Date',
           'DP Code', 'DP Name', 'DP Client id', 'Bank AC No', 'Bank Name',
           'Bank Address', 'IFSC Code', 'MICR Code', 'Risk Catg', 'Poa Flag',
           'Poa Acitvation', 'Poa DeAcitvation', 'Father Name', 'Entity',
           'Date of Birth', 'GST State Name', 'Contract Type', 'Software Type',
           'Interest', 'Internet Trading', 'Terminal ID', 'Fo Terminal ID',
           'Active Exchange', 'File No', 'KYC Flag', 'Brokerage Slab ID',
           'Last Sett of Date', 'FATCA', 'CKYC Regn.No', 'UID  No', 'GST Regn.No',
           'Annual Income', 'Dealer Code', 'Remarks', 'Familyid', 'Settoff Period',
           'Last Trade Done Date', 'UPI ID', 'Net Worth', 'Poa Flag(Fund)',
           'Poa Acitvation Fund', 'Poa DeAcitvation Fund', 'Lead Refno',
           'mapin id', 'payout flag', 'Region', 'DemChrg(B) %', 'DemChrg(S) %',
           'DemChrg(Rs.)', 'DemChrg(Rs.).1', 'KRADoc.Recv.Date', 'Occupation',
           'Annual Income Date', 'Gender', 'Bank Account Type',
           'Daily Margin Code', 'Security Account Code', 'Non Traceable',
           'AAdhar Link Flag', 'Nominee Flag', 'DDPI Activated',
           'DDPI Activated Date', 'Status Change Reason', 'KYC Mode', 'KYC Form',
           'RBI Payment Mode', 'RBI Approval No', 'PIS Bank A/c No',
           'NRI Saving Bank A/c No', 'Custodial Code (IFT)']
print(dr)
dr.to_csv("test.csv")










#####################################################################################################


if uploaded_file1 is not None and uploaded_file2 is not None:
    df1 = pd.DataFrame(dr)
    st.dataframe(df1)
    df2 = pd.read_csv(uploaded_file2)
    st.dataframe(df2)
    if df1["Client Code"].equals(df2["Client Code"]):
        st.success("Files are identical")
    else:
        df1 = pd.DataFrame(dr)
        st.warning("Files are different")
        diff = df1[["Client Code"]].merge(df2[["Client Code"]], indicator=True, how='outer')
        diff = diff[diff['_merge'] != 'both']
        print("hgfgdsfggfkgsdgfkgkdhsgf",diff)
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
