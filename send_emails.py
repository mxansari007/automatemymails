import os
import smtplib
import pandas as pd
import requests
import time
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

# ✅ Setup Logging
logging.basicConfig(filename="email_log.txt", level=logging.INFO, format="%(asctime)s - %(message)s")

# ✅ Fetch environment variables
CLOUDINARY_CSV_URL = os.getenv("MAIL_CSV")
SENDER_EMAIL = os.getenv("SENDER_EMAIL")
SENDER_PASSWORD = os.getenv("SENDER_PASSWORD")

# ✅ Step 1: Download CSV file
csv_file = "temp.csv"
try:
    response = requests.get(CLOUDINARY_CSV_URL)
    response.raise_for_status()
    with open(csv_file, "wb") as file:
        file.write(response.content)
    print("✅ CSV file downloaded successfully!")
except requests.exceptions.RequestException as e:
    print(f"❌ Error downloading CSV file: {e}")
    exit(1)

# ✅ Step 2: Read CSV file
df = pd.read_csv(csv_file)
print("✅ CSV file loaded successfully!")

# ✅ Resume file (stored locally)
resume_file = "Mohammad_Maaz_Resume_NIT_KKR.pdf"

# ✅ Email SMTP Setup
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
MAX_RETRIES = 3  # Number of retries per email
DELAY_BETWEEN_EMAILS = 1  # Delay in seconds to prevent rate limits

def send_email(server, to_email, recruiter_name, recruiter_company):
    """Sends a cold email with resume attached, with retries on failure."""
    subject = f"Application for Software Developer Role - Mohammad Maaz Ansari"
    
    body = f"""
    <html>
    <body>
    <p>Dear <b>{recruiter_name}</b>,</p>
    
    <p>I hope you're doing well. My name is <b>Mohammad Maaz Ansari</b>, and I am currently pursuing my MCA from <b>NIT Kurukshetra</b> with a CGPA of 8.43. I recently came across opportunities at <b>{recruiter_company}</b> and would love to explore potential roles that align with my skills and experience.</p>
    
    <p>With a strong foundation in <b>full-stack web development</b> and <b>cloud computing</b>, I have hands-on experience in <b>React.js, Express.js, Next.js, MySQL, MongoDB, Docker, and AWS</b>. My passion lies in building scalable and efficient applications, and I have demonstrated this through my projects and internship experiences.</p>
    
    <p>Here are some of my key projects:</p>
    
    <ul>
        <li><b><a href="https://nitkkrhostels.live">NIT Hostel Management System</a></b>: A comprehensive web-based application simplifying hostel administration.</li>
        <li><b><a href="https://smartreport.vercel.app/">Smart Report</a></b>: A platform generating structured medical reports with OTP authentication.</li>
        <li><b>Hiring System UI Redesign (Internship at Codehop Interfusion)</b>: Improved engagement by 4% and reduced processing time by 10%.</li>
    </ul>
    
    <p>Here are my details:</p>
    <ul>
        <li><b>Email:</b> mxansari007@gmail.com</li>
        <li><b>Phone:</b> +91-9457077164</li>
        <li><b>GitHub:</b> <a href="https://github.com/mxansari007">GitHub Profile</a></li>
        <li><b>LinkedIn:</b> <a href="https://www.linkedin.com/in/maaz-ansari-a6b6b0137/">LinkedIn Profile</a></li>
    </ul>
    
    <p>Looking forward to your response!</p>
    
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
        print(f"❌ Failed to attach resume: {e}")

    # Retry logic
    for attempt in range(MAX_RETRIES):
        try:
            server.sendmail(SENDER_EMAIL, to_email, msg.as_string())
            logging.info(f"✅ Email sent to {to_email}")
            print(f"✅ Email sent to {to_email}")
            return True
        except Exception as e:
            print(f"⚠️ Attempt {attempt+1} failed for {to_email}: {e}")
            logging.warning(f"⚠️ Attempt {attempt+1} failed for {to_email}: {e}")
            time.sleep(2 ** attempt)  # Exponential backoff (2, 4, 8 sec)
    
    print(f"❌ Failed to send email to {to_email} after {MAX_RETRIES} attempts.")
    logging.error(f"❌ Failed to send email to {to_email} after {MAX_RETRIES} attempts.")
    return False

# ✅ Establish SMTP connection once (avoids reconnecting each time)
try:
    server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
    server.starttls()
    server.login(SENDER_EMAIL, SENDER_PASSWORD)
    print("✅ SMTP connection established.")
except Exception as e:
    print(f"❌ SMTP connection failed: {e}")
    exit(1)

# ✅ Send emails with rate limiting
for _, row in df.iterrows():
    recruiter_email = row.get("Email")
    recruiter_name = row.get("Name", "Recruiter")
    recruiter_company = row.get("Company", "your company")

    if pd.notna(recruiter_email):
        success = send_email(server, recruiter_email, recruiter_name, recruiter_company)
        
        if success:
            time.sleep(DELAY_BETWEEN_EMAILS)  # ✅ Prevents rapid consecutive emails

# ✅ Close SMTP session
server.quit()
print("✅ All emails processed and SMTP connection closed.")
