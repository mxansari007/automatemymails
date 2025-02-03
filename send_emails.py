import os
import smtplib
import pandas as pd
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

# Load recruiter details from CSV
csv_file = os.getenv("MAIL_CSV")
df = pd.read_csv(csv_file)

# Fetch credentials securely from GitHub Secrets
SENDER_EMAIL = os.getenv("SENDER_EMAIL")
SENDER_PASSWORD = os.getenv("SENDER_PASSWORD")

# Email SMTP setup
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

# Path to your resume file
RESUME_PATH = "Mohammad_Maaz_Resume_NIT_KKR.pdf"

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
        with open(RESUME_PATH, "rb") as resume_file:
            attach_part = MIMEApplication(resume_file.read(), _subtype="pdf")
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
