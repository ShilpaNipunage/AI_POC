# 🏫 Multi-Agent School Beacon Workflow (n8n + LLM)

This project automates the parsing of school beacons (emails and the attachments) using LLMs, and sends updates/reminders to parents and students via Gmail and Google Tasks.

## 🛠️ Tech Stack

- [x] n8n (workflow orchestrator)
- [x] Gemini Chat Model 
- [x] Gmail API
- [x] Google Tasks API

## 🔄 Workflow Overview

1. **Trigger:** Weekly school newsletter PDF received
2. **Decompresser:** Unzips the attachment if its a zip file
3. **PDFReader:** Reads contents from pdf
4. **Parser:** LLM extract action items, assignments and updates from mail contents and parsed pdf contents
5. **Actions:**
   - Emails parents with summary and the action items
   - Adds tasks to Google Tasks for assignments and assessments
  
## 🚀 How to Use

1. Clone this repo
2. Import `school_beacon_workflow.json` into your local n8n instance
3. Configure API keys for OpenAI/Gemini, Gmail, and Google Tasks
4. Run manually

## 📸 Screenshots

### n8n Workflow:
![workflow](https://github.com/user-attachments/assets/c3b8b5e1-c16e-4016-bfec-2a214b065719)


### Sample School Email:
![Mail from School](https://github.com/user-attachments/assets/a7070f44-bcb4-461c-b728-9bd6e5581148)


### Sample generated Summary:
![BeaconSummary](https://github.com/user-attachments/assets/257934f0-f883-4bb2-9377-06e785d83323)

