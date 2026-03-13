# Automation Practical Assessment Projects

This repository contains two automation projects developed as part of an **Automation Practical Assessment**.
Both projects demonstrate workflow automation concepts using **Python and n8n-based workflow design**.

---

# Project 1: IT Support Ticket Automation

## Overview
This project automates the processing of IT support tickets submitted by students or staff in a university environment.
The automation pipeline validates tickets, removes duplicates, routes issues to the correct support teams,
calculates SLA deadlines, and generates operational reports.

The goal is to **reduce manual workload and improve IT support response efficiency**.

## Key Features
- Email validation
- Priority validation
- Duplicate ticket detection
- Automated issue routing
- SLA deadline calculation
- Processed and rejected ticket outputs
- Summary report generation

## Workflow
Ticket Input
      |
      v
Validation
      |
      v
Duplicate Detection
      |
      v
Ticket ID Generation
      |
      v
Issue Routing
      |
      v
SLA Calculation
      |
      v
Processed Ticket Storage
      |
      v
Summary Report

## Technologies Used
- Python
- CSV data processing
- Workflow automation concepts
- n8n workflow design

---

# Project 2: Automated Explainer Video Generator

## Overview
This project automatically generates short explainer videos (30–60 seconds) from structured text input.
The system converts text into narration using a **text-to-speech engine**, generates slides for each section
of the text, and compiles them into a final MP4 video.

This automation allows universities to quickly generate announcement videos without manual editing.

## Key Features
- Automatic text-to-speech narration
- Slide generation from text
- Scene-based video generation
- Automated video compilation
- Configurable parameters for layout and timing

## Workflow
Input Text File
      |
      v
Workflow Trigger
      |
      v
Text Parsing
      |
      v
Scene Generation
      |
      v
Text-To-Speech Conversion
      |
      v
Slide Image Rendering
      |
      v
Scene Video Creation
      |
      v
Final Video Compilation
      |
      v
Output: explainer_video.mp4

## Technologies Used
- Python
- MoviePy
- Pillow
- gTTS / pyttsx3
- FFmpeg
- n8n workflow design

---

# Repository Structure

Automation_Assessment
│
├── IT_Support_Automation
│   ├── ticket_automation.py
│   ├── processed_tickets.csv
│   ├── rejected_tickets.csv
│   ├── summary_report.csv
│   └── n8n_workflow_design.md
│
├── Video_Generation_Automation
│   ├── video_generator.py
│   ├── input.txt
│   ├── explainer_video.mp4
│   └── n8n_workflow_design.md
│
└── reports
    ├── assessment1_report.pdf
    └── assessment2_report.pdf

---

# Skills Demonstrated
- Workflow automation
- Data processing
- System architecture design
- Text-to-speech integration
- Video generation automation
- Error handling and pipeline design

---

# Author
Dayananda S G

Automation Practical Assessment Projects
