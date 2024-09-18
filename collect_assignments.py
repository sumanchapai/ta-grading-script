from datetime import datetime
from pathlib import Path

import re
import math

### Need to change the followings based on the project
PROJECT_SUBMISSIONS = Path("/Users/suman/Desktop/purdue-ta/grading-fall-cs408/proj1-submissions")
PROJECT_DEADLINE = datetime(2024, 9, 10, 23, 59)
# Filename that saves the number of late days used by a student in this project
LATE_DAYS_FILENAME = "late-days-used-project1.txt" 
# Here we define the script to unzip the pdfs and put them in a new folder, etc.
SAVE_SUBMISSIONS_TO = "clean-submissions-project-1"
SCRIPT_PRE = f"mkdir {SAVE_SUBMISSIONS_TO}"
SCRIPT_POST = f"cd {SAVE_SUBMISSIONS_TO}"
# Once that script is generated run it as `bash SCRIPT_NAME`
SCRIPT_NAME = "project-1-collect.sh"
# Customize the script as needed
def SCRIPT_FOR_EACH(project_path, username):
    lines = [
        # Create a folder for the student
        f'mkdir "./{SAVE_SUBMISSIONS_TO}/{username}"',
        # Move the zip to the desired location
        f'cp "{project_path}/"*.zip "./{SAVE_SUBMISSIONS_TO}/{username}"',
        # cd to the location and unzip
        f'cd "./{SAVE_SUBMISSIONS_TO}/{username}"',
        f'unzip *.zip',
        f'rm *.zip',
        f'cd ../../',
        ""
    ]
    return lines


### NO NEED TO CHANGE
### Should work the same for all projects without changing anything
STUDENT_FOLDER_REGEX =  re.compile(
    r"^\d+-\d+\s-\s([\w\d]+)\s\w+\s\w+\s-\s(.*)$"
) # Example: 202020-29393 - chapsu01 Suman Chapai - Sep 20, 2024 1035 PM 
DATE_TIME_FORMAT = "%b %d, %Y %I%M %p" # Example: Sep 20, 2024 1035 PM

def get_purdue_id_submission_time(name):
    match =  STUDENT_FOLDER_REGEX.match(name)
    purdue_username, date_str = match.groups()
    time = datetime.strptime(date_str, DATE_TIME_FORMAT)
    return purdue_username, time

def calculate_late_days(deadline, submitted_time):
    late_seconds = (submitted_time - deadline).total_seconds()
    late_days = math.ceil(late_seconds / (60 * 60 * 24))
    if late_days < 0:
        late_days = 0
    return late_days

def get_late_days_and_submissions_dict():

    late_days = {} # username -> late_days_used_for_this_assignment
    students_latest_submission = {} # username -> (folder path, submission time)

    for file in PROJECT_SUBMISSIONS.iterdir():
        filename = str(file.name)
        if not STUDENT_FOLDER_REGEX.match(filename):
            continue
        username, submission_time = get_purdue_id_submission_time(filename)
        if (username not in students_latest_submission
            # Or if this is a newer submission
            or (submission_time - students_latest_submission[username][1]).total_seconds() > 0):
            late_days[username] = calculate_late_days(PROJECT_DEADLINE, submission_time)
            students_latest_submission[username] = (file, submission_time)

    return late_days, students_latest_submission

def generate_late_days_file():
    late_days, students_latest_submission = get_late_days_and_submissions_dict()
    with open(LATE_DAYS_FILENAME, 'w') as fd:
        for student in students_latest_submission:
            late_by = late_days[student]
            submitted_at = students_latest_submission[student][1].strftime("%b-%d %H:%M")
            fd.write(f"{student:<20} \t {late_by}\t {submitted_at}\n")

def generate_script_for():
    _, students_latest_submission = get_late_days_and_submissions_dict()
    with open(SCRIPT_NAME, "w") as fd:
        fd.write(SCRIPT_PRE) 
        fd.write("\n")
        for username in students_latest_submission:
            project_path = students_latest_submission[username][0]
            script_lines = SCRIPT_FOR_EACH(project_path, username)
            # Write script to script file
            for line in script_lines:
                fd.write(line)
                fd.write("\n")
        fd.write(SCRIPT_POST)
        fd.write("\n")


if __name__ == "__main__":
    generate_late_days_file()
    generate_script_for()
