# Group Members Full Names and Student IDs:

- Student: Yaseen Sassi     StudentID: 24023127

- Student: Thierno Batiga     StudentID: 24024769

- Student: Leonard Masters     StudentID: 24031618

- Student: Ishak Askar    StudentID: 24023614

---

# Instructions on how to get the app up and running in order:

Step 1: Make a file under the folder "utils/" called config.py.

Step 2: Go into config_template.py under "utils/" folder, copy the code and paste it into config.py.

Step 3: Edit the login details for your MySQL Workbench in the code you pasted into config.py to your own account login details, now your database should be connected when you get to running the app.

Step 4: In your terminal run "pip install -r requirements.txt", this makes sure your environment is fully set-up with required libraries.

Step 5: Select into the following files and run them once IN THIS ORDER to pre-populate your database with required data: 1. "create_locations.py", 2. "create_admin.py" and 3. "create_apartments.py". One file populates locations in the database, next creates an admin account you can login with and the last populates the apartments table in the database.

Step 6: Select into the file "app.py" and click run or run it from the terminal.

Step 7: The app is now running. You can now log in as an admin and perform tasks such as creating lower level staff acccounts such as FrontDesk, FinanceManager etc. Once you have a FrontDesk staff account, you can then create tenant accounts and log in as a tenant, whcih will take you to the tenant portal.

---

Note: If you get an error with some pages uninstall bcrypt and re-install the version bcrypt 3.2.2

You can do that with the following commands:

- "pip uninstall bcrypt"

Then use

- pip install bcrypt==3.2.2