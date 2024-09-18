Script in this repo is meant to help TAs using Brightspace to download student
HW submissions perfom scripting over students' assignments, and manage things
like discarding the non-latest submission, calcuating late days for the
assignment, etc.

The code in this repo is meant to be changed as per your needs. A sample usage
looks like the following for me.

1. Clone this repo.
1. Download all the submissions from Brightspace to this repo folder.
1. Brightspace gives them in a zip format. I have save the zip (call it
   `hws.zip`) to a folder called `proj1-submissions`. Then unzip the file using
   `unzip hws.zip`.
1. Update the variables in the `collect_assignments.py` as necessary.
1. Run `python collect_assignments.py`.
1. This generates two files, one that displays the late days used by the student
   in this project submission. Note that we're rounding the day to the ceiling
   integer. You can change the code to do whatever fits your course policies.
   The second file generates the script that I can run as `bash <script-name>`.
   In my case I am using this script to unzip the student's submission and put
   it in a folder by student's username.
1. Note that if a student has multiple submissions, only the latest one will be
   used.
