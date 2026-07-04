from flask import Flask, render_template, request, redirect, url_for
# from flask_mail import Mail, Message 
import os

import random
import string

app = Flask(__name__)

# ===============================
# File for storing registrations
# ===============================
FILE_NAME = "registrations.txt"

# ===============================
# EVENT DETAILS (IMPORTANT)
# ===============================
EVENT_DETAILS = {
    "Code Sprint 2026": {
        "date": "25 April 2026",
        "time": "10:00 AM",
        "venue": "Computer Lab 1",
        "description": "Programming competition based on coding and logical problem solving.",
        "coordinator": "Mrs. Nidhi Keshav",
        "phone": "+91 999999999",
        "email": "nidhi@test.gmail.com"
    },

    "Web Design Challenge": {
        "date": "27 April 2026",
        "time": "11:30 AM",
        "venue": "Seminar Hall",
        "description": "Design creative and responsive websites.",
        "coordinator": "Miss Akansha Rathore",
        "phone": "+91 9999999999",
        "email": "akansha@test.gmail.com"
    },

    "Project Exhibition": {
        "date": "30 April 2026",
        "time": "09:30 AM",
        "venue": "Auditorium",
        "description": "Showcase innovative projects before faculty members.",
        "coordinator": "Mrs. Mitali Choudhary",
        "phone": "+91 9999999999",
        "email": "mitali@test.gmail.com"
    },

    "Quiz Master": {
        "date": "2 May 2026",
        "time": "01:00 PM",
        "venue": "Room 204",
        "description": "Test your technical and general knowledge.",
        "coordinator": "Miss Swati Modi",
        "phone": "+91 9999999999",
        "email": "swati@test.gmail.com"
    },

    "Cultural Fiesta": {
        "date": "5 May 2026",
        "time": "04:00 PM",
        "venue": "Main Stage",
        "description": "Dance, singing and cultural activities.",
        "coordinator": "Mrs. Krishna Paan",
        "phone": "+91 9999999999",
        "email": "krishna@test.gmail.com"
    },

    "Sports Meet": {
        "date": "8 May 2026",
        "time": "08:00 AM",
        "venue": "College Ground",
        "description": "Indoor and outdoor sports competitions.",
        "coordinator": "Mr. Arjun Parihar",
        "phone": "+91 9999999999",
        "email": "arjun@test.gmail.com"
    }
}


# -------------------------------
# Create file if not exists
# -------------------------------
if not os.path.exists(FILE_NAME):
    open(FILE_NAME, "w").close()

def generate_ticket_id():

    while True:

        ticket_id = "CC2026-" + "".join(
            random.choices(string.ascii_uppercase + string.digits, k=6)
        )

        if not os.path.exists(FILE_NAME):
            return ticket_id

        with open(FILE_NAME, "r", encoding="utf-8") as file:

            data = file.read()

            if ticket_id not in data:
                return ticket_id
    
    
# -------------------------------
# Save Registration
# -------------------------------
def save_registration(data):
    with open(FILE_NAME, "a", encoding="utf-8") as file:

        file.write(f"Name: {data['name']}\n")
        file.write(f"Enrollment: {data['enrollment']}\n")
        file.write(f"Department: {data['department']}\n")
        file.write(f"Semester: {data['semester']}\n")
        file.write(f"Email: {data['email']}\n")
        file.write(f"Phone: {data['phone']}\n")
        file.write(f"Event: {data['event']}\n")
        file.write(f"Message: {data['message']}\n")
        file.write(f"Ticket ID: {data['ticket_id']}\n")
        file.write(f"UTR: {data['utr']}\n")
        file.write("=====================================\n\n")


# -------------------------------
# Read Registrations
# -------------------------------
def load_registrations():

    registrations = []

    if not os.path.exists(FILE_NAME):
        return registrations

    with open(FILE_NAME, "r", encoding="utf-8") as file:

        student = {}

        for line in file:

            line = line.strip()

            if line.startswith("Name:"):
                student["name"] = line.replace("Name:", "").strip()

            elif line.startswith("Enrollment:"):
                student["enrollment"] = line.replace("Enrollment:", "").strip()

            elif line.startswith("Department:"):
                student["department"] = line.replace("Department:", "").strip()

            elif line.startswith("Semester:"):
                student["semester"] = line.replace("Semester:", "").strip()

            elif line.startswith("Email:"):
                student["email"] = line.replace("Email:", "").strip()

            elif line.startswith("Phone:"):
                student["phone"] = line.replace("Phone:", "").strip()

            elif line.startswith("Event:"):
                student["event"] = line.replace("Event:", "").strip()

            elif line.startswith("Message:"):
                student["message"] = line.replace("Message:", "").strip()
                
            elif line.startswith("Ticket ID:"):
                student["ticket_id"] = line.replace("Ticket ID:", "").strip()
                
            elif line.startswith("UTR:"):
                student["utr"] = line.replace("UTR:", "").strip()

            elif line.startswith("====================================="):

                if student:
                    registrations.append(student)
                    student = {}

    return registrations


# -------------------------------
# Home
# -------------------------------
@app.route("/")
def home():
    registrations = load_registrations()
    total = len(registrations)

    return render_template("index.html", total=total)

# -------------------------------
# Events
# -------------------------------
@app.route("/events")
def events():
    return render_template("events.html")


# -------------------------------
# Register
# -------------------------------
@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        student = {
            "name": request.form["name"],
            "enrollment": request.form["enrollment"],
            "department": request.form["department"],
            "semester": request.form["semester"],
            "email": request.form["email"],
            "phone": request.form["phone"],
            "event": request.form["event"],
            "message": request.form["message"],
            "utr": request.form["utr"],
            "ticket_id": generate_ticket_id()
            
            
        }

        save_registration(student)

        # Event Details
        event = student["event"]
        details = EVENT_DETAILS.get(event, {})

        # ==========================
        # Email to Student
        # ==========================

        return render_template(
        "success.html",
        name=student["name"],
        ticket_id=student["ticket_id"],
        event=event,
        details=details
)

    selected_event = request.args.get("event", "")

    return render_template(
        "register.html",
        selected_event=selected_event
    )
# -------------------------------
# Admin
# -------------------------------

# -------------------------------
# Check Registration Status
# -------------------------------
@app.route("/status", methods=["GET", "POST"])
def status():

    if request.method == "POST":

        phone = request.form["phone"]
        enrollment = request.form["enrollment"]
        ticket_id = request.form["ticket_id"]

        registrations = load_registrations()

        for student in registrations:

            if (
                student.get("phone") == phone
                and student.get("enrollment") == enrollment
                and student.get("ticket_id") == ticket_id
            ):

                details = EVENT_DETAILS.get(student["event"], {})

                return render_template(
                    "result.html",
                    student=student,
                    details=details
                )

        return render_template(
            "status.html",
            error="No Registration Found!"
        )

    return render_template("status.html")


@app.route("/admin")
def admin():

    registrations = load_registrations()

    total = len(registrations)

    code_sprint = 0
    web_design = 0
    quiz_master = 0
    project_exhibition = 0
    cultural_fiesta = 0
    sports_meet = 0

    for student in registrations:

        if student["event"] == "Code Sprint 2026":
            code_sprint += 1

        elif student["event"] == "Web Design Challenge":
            web_design += 1

        elif student["event"] == "Quiz Master":
            quiz_master += 1

        elif student["event"] == "Project Exhibition":
            project_exhibition += 1

        elif student["event"] == "Cultural Fiesta":
            cultural_fiesta += 1

        elif student["event"] == "Sports Meet":
            sports_meet += 1

    return render_template(

        "admin.html",

        registrations=registrations,

        total=total,

        code_sprint=code_sprint,

        web_design=web_design,

        quiz_master=quiz_master,

        project_exhibition=project_exhibition,

        cultural_fiesta=cultural_fiesta,

        sports_meet=sports_meet
    )

# -------------------------------
# Run Server
# -------------------------------
if __name__ == "__main__":

    app.run(
        debug=True
    )