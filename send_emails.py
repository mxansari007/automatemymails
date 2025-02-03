import os
import smtplib
import pandas as pd
import requests  # ✅ To fetch CSV and Resume from Cloudinary
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

# Fetch environment variables
CLOUDINARY_CSV_URL = os.getenv("MAIL_CSV")  # ✅ Cloudinary CSV URL
CLOUDINARY_RESUME_URL = os.getenv("Resume_Path")  # ✅ Cloudinary Resume URL
SENDER_EMAIL = os.getenv("SENDER_EMAIL")
SENDER_PASSWORD = os.getenv("SENDER_PASSWORD")

# ✅ Step 1: Download CSV file from Cloudinary
csv_file = "temp.csv"  # Temporary file to store downloaded CSV
try:
    response = requests.get(CLOUDINARY_CSV_URL)
    response.raise_for_status()
    with open(csv_file, "wb") as file:
        file.write(response.content)
    print("CSV file downloaded successfully from Cloudinary!")
except requests.exceptions.RequestException as e:
    print(f"Error downloading CSV file: {e}")
    exit(1)  # Exit the script if the file cannot be downloaded

# ✅ Step 2: Read CSV file
df = pd.read_csv(csv_file)
print("CSV file loaded successfully!")

# ✅ Step 3: Download Resume from Cloudinary
resume_file = "Mohammad_Maaz_NIT_KKR_2025.pdf"
try:
    response = requests.get(CLOUDINARY_RESUME_URL)
    response.raise_for_status()
    with open(resume_file, "wb") as file:
        file.write(response.content)
    print("Resume downloaded successfully from Cloudinary!")
except requests.exceptions.RequestException as e:
    print(f"Error downloading Resume: {e}")
    exit(1)  # Exit the script if the file cannot be downloaded

# Email SMTP setup
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

def send_email(to_email, recruiter_name, recruiter_company):
    """Sends a cold email to the recruiter with the resume attached."""
    subject = f"Application for Software Developer Role - Mohammad Maaz Ansari"

    body = f"""
    <html>
    <body>
    <p>Dear <b>{recruiter_name}</b>,</p>

    <p>I hope you're doing well. My name is <b>Mohammad Maaz Ansari</b>, and I am currently pursuing my MCA from NIT Kurukshetra.<br/> 
    I came across opportunities at <b>{recruiter_company}</b> and would love to explore potential roles that align with my skills.</p>

    <p>I have experience in frontend, backend development, and Cloud Computing, with expertise in <b>React.js, Express.js, MySQL, Docker, AWS</b>. 
    My projects include:</p>

    <ul>
        <li><b><a href="https://nitkkrhostels.live">NIT Hostel Management System</a></b>: Simplifies hostel management.</li>
        <li><b><a href="https://smartreport.vercel.app/">Smart Report</a></b>: Generates medical reports in a visually appealing format.</li>
    </ul>

    <p>Here are my details:</p>
    <ul>
        <li><b>Email:</b> mxansari007@gmail.com</li>
        <li><b>Phone:</b> +91-9457077164</li>
        <li><b>GitHub:</b> <a href="https://github.com/mxansari007">GitHub Profile</a></li>
        <li><b>LinkedIn:</b> <a href="https://www.linkedin.com/in/maaz-ansari-a6b6b0137/">LinkedIn Profile</a></li>
    </ul>

    <p>Looking forward to your response.</p>

    <p>Best regards, <br><b>Mohammad Maaz Ansari</b></p>
    </body>
    </html>
    """

    msg = MIMEMultipart()
    msg["From"] = SENDER_EMAIL
    msg["To"] = to_email
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "html"))

    # Attach resume
    try:
        with open(resume_file, "rb") as resume:
            attach_part = MIMEApplication(resume.read(), _subtype="pdf")
            attach_part.add_header("Content-Disposition", "attachment", filename="Mohammad_Maaz_NIT_KKR_2025.pdf")
            msg.attach(attach_part)
    except Exception as e:
        print(f"Failed to attach resume: {e}")

    # Send the email
    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.sendmail(SENDER_EMAIL, to_email, msg.as_string())
        server.quit()
        print(f"Email sent to {to_email}")
    except Exception as e:
        print(f"Failed to send email to {to_email}: {e}")

# Iterate through CSV and send emails
for _, row in df.iterrows():
    recruiter_email = row.get("Email")
    recruiter_name = row.get("Name")
    recruiter_company = row.get("Company")

    if pd.notna(recruiter_email):
        send_email(recruiter_email, recruiter_name, recruiter_company)
