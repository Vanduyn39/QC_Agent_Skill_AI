# 🚀 QC Super Agent - Antigravity Automation

**QC Super Agent** is an AI assistant system running on the Antigravity platform, designed to automate the entire workflow of a Quality Control (QC) specialist: from reading business requirements to generating Test Cases, rapidly logging bugs, and automatically compiling daily/weekly reports with visual charts.

## 📌 Key Features
- **Automated Test Case Generation:** Automatically reads Requirement files (`.docx`, `.pdf`, `.xlsx`) **placed in the `inputs` folder**, generates standard format Test Cases, and pushes them directly to Google Sheets.
- **Lightning-fast Bug Logging:** Extracts bug information from natural language prompts, categorizes Severity/Priority according to project guidelines, and logs them into both local Excel files and Google Sheets.
- **Professional Reporting:**
    - **Daily Report:** Summarizes the number of bugs logged in a day and analyzes error modules.
    - **Weekly Report:** Provides statistics on bug trends over the week, accompanied by visual charts (`.png`).
- **Multi-Project Management:** Automatically categorizes and manages data based on the `assets/{project_name}` directory structure.

---

## 🛠 Google Sheets API Setup Guide

To allow the Agent to write data to the Cloud, you need to provide it with a "key" via the Google Cloud Console.

### 1. Create a Project and Get the Credentials File
1. Go to the [Google Cloud Console](https://console.cloud.google.com/).
2. Create a new Project (e.g., `QC-Automation-Agent`).
3. Navigate to **APIs & Services > Library**: Find and **Enable** the following two APIs:
    - **Google Sheets API**
    - **Google Drive API**
4. Navigate to **Credentials > Create Credentials > Service Account**:
    - Name the Service Account and click **Create**.
    - Once created, click on the email of that account, go to the **Keys** tab **> Add Key > Create New Key**.
    - Select **JSON** format. The file will be downloaded to your computer.
5. Rename the downloaded file to `credentials.json` and place it in the root directory of this repository.

### 2. Create the Sheet and Share Access (Crucial Step)
To avoid Google's storage limits (Quota Exceeded errors) for the Service Account, please follow this method:
1. Open the `credentials.json` file, find and copy the line containing `"client_email": "..."`.
2. Go to your personal Google Drive and create a new Google Sheet file. Name it exactly after your project (e.g., `Comana`).
3. Click the **Share** button in the top right corner.
4. Paste the Service Account email (from step 1), set the role to **Editor**, and click **Send**.
5. Repeat this process for any other projects you add.

---

## 📂 Folder Structure
```text
QC_Agent_Skill/
├── credentials.json          # Google API Key file (DO NOT EXPOSE)
├── SKILL.md                  # The "brain" instructions for the Agent
├── assets/                   # Data storage for each project (Comana, Project_X...)
│   └── {project_name}/
│       ├── inputs/           # ⚠️ DROP YOUR REQUIREMENT FILES HERE FOR THE AI TO READ
│       └── outputs/          # Contains generated reports, charts, and excel backups
├── references/               # Specific guidelines and rules for each project
│   └── {project_name}/
│       ├── bug_guidelines.md
│       └── testcase_template.md
└── scripts/                  # Python source code for logic processing
    ├── sheet_logger.py       # Pushes data to Google Sheets
    ├── log_manager.py        # Manages Bug/Test Case logging logic
    └── generate_reports.py   # Draws charts and generates reports
    └── read_requirements.py   # Read requirements
