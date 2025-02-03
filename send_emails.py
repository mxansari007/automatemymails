import os
import smtplib
import pandas as pd
import requests  # ✅ Only needed for CSV download
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

# Fetch environment variables
CLOUDINARY_CSV_URL = os.getenv("MAIL_CSV")  # ✅ Cloudinary CSV URL
SENDER_EMAIL = os.getenv("SENDER_EMAIL")
SENDER_PASSWORD = os.getenv("SENDER_PASSWORD")

# ✅ Step 1: Download CSV file from Cloudinary
csv_file = "temp.csv"  # Temporary file to store downloaded CSV
try:
    response = requests.get(CLOUDINARY_CSV_URL)
    response.raise_for_status()
    with open(csv_file, "wb") as file:
        file.write(response.content)
    print("✅ CSV file downloaded successfully from Cloudinary!")
except requests.exceptions.RequestException as e:
    print(f"❌ Error downloading CSV file: {e}")
    exit(1)  # Exit the script if the file cannot be downloaded

# ✅ Step 2: Read CSV file
df = pd.read_csv(csv_file)
print("✅ CSV file loaded successfully!")

# ✅ Step 3: Use local resume file instead of downloading
resume_file = "Mohammad_Maaz_Resume_NIT_KKR.pdf"  # Resume is now stored in the repo

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
    
    <p>I hope you're doing well. My name is <b>Mohammad Maaz Ansari</b>, and I am currently pursuing my MCA from <b>NIT Kurukshetra</b> with a CGPA of 8.43. I recently came across opportunities at <b>{recruiter_company}</b> and would love to explore potential roles that align with my skills and experience.</p>
    
    <p>With a strong foundation in <b>full-stack web development</b> and <b>cloud computing</b>, I have hands-on experience in <b>React.js, Express.js, Next.js, MySQL, MongoDB, Docker, and AWS</b>. My passion lies in building scalable and efficient applications, and I have demonstrated this through my projects and internship experiences.</p>
    
    <p>Here are some of my key projects:</p>
    
    <ul>
        <li><b><a href="https://nitkkrhostels.live">NIT Hostel Management System</a></b>: A comprehensive web-based application simplifying hostel administration with automated room assignments, student data uploads, and digital notice distribution.</li>
        <li><b><a href="https://smartreport.vercel.app/">Smart Report</a></b>: A platform that generates structured and visually appealing medical reports, integrating OTP-based authentication and PDF generation.</li>
        <li><b>Hiring System UI Redesign (Internship at Codehop Interfusion)</b>: Revamped the frontend of a hiring platform, improving engagement by 4% and reducing processing time by 10%.</li>
        <li><b>TinkerQuest Hackathon Project (Top 20 out of 500+ teams)</b>: Built a patient report generation system using React.js and PDF generation tools.</li>
    </ul>
    
    <p>Beyond technical skills, I have actively contributed to my department, delivering lectures on <b>Git & GitHub</b> and <b>Web Development</b> under the Digital India Workshop.</p>
    
    <p>Here are my details:</p>
    <ul>
        <li><b>Email:</b> mxansari007@gmail.com</li>
        <li><b>Phone:</b> +91-9457077164</li>
        <li><b>GitHub:</b> <a href="https://github.com/mxansari007">GitHub Profile</a></li>
        <li><b>LinkedIn:</b> <a href="https://www.linkedin.com/in/maaz-ansari-a6b6b0137/">LinkedIn Profile</a></li>
    </ul>
    
    <p>I would love to connect and discuss how my skills align with <b>{recruiter_company}</b>'s requirements. Looking forward to your response!</p>
    
    <p>Best regards, <br><b>Mohammad Maaz Ansari</b></p>
    </body>
    </html>
    """

    msg = MIMEMultipart()
    msg["From"] = SENDER_EMAIL
    msg["To"] = to_email
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "html"))

    # Attach resume (Local File)
    try:
        with open(resume_file, "rb") as resume:
            attach_part = MIMEApplication(resume.read(), _subtype="pdf")
            attach_part.add_header("Content-Disposition", "attachment", filename="Mohammad_Maaz_NIT_KKR_2025.pdf")
            msg.attach(attach_part)
    except Exception as e:
        print(f"❌ Failed to attach resume: {e}")

    # Send the email
    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.sendmail(SENDER_EMAIL, to_email, msg.as_string())
        server.quit()
        print(f"✅ Email sent to {to_email}")
    except Exception as e:
        print(f"❌ Failed to send email to {to_email}: {e}")

# Iterate through CSV and send emails
for _, row in df.iterrows():
    recruiter_email = row.get("Email")
    recruiter_name = row.get("Name")
    recruiter_company = row.get("Company")

    if pd.notna(recruiter_email):
        send_email(recruiter_email, recruiter_name, recruiter_company)
