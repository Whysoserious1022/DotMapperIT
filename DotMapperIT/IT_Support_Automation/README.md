
# Automated IT Support Ticket Processing System

## Overview

This project implements an automated workflow for processing IT support tickets.
The system validates incoming tickets, removes duplicate requests, routes issues
to the appropriate support teams, calculates Service Level Agreement (SLA)
deadlines, and generates operational reports.

The goal of this automation is to improve IT support efficiency, reduce manual
workload, and ensure faster issue resolution.

---

## Problem Statement

Universities and organizations receive many IT support requests related to:

- WiFi connectivity issues
- Login problems
- Software installation issues
- Hardware problems

When handled manually, these requests often cause:

- Delayed responses
- Duplicate tickets
- Incorrect routing
- Increased workload for IT staff

This project automates the ticket processing pipeline to solve these problems.

---

## Key Features

### Ticket Validation
- Email format validation
- Priority validation (Low / Medium / High)

### Data Normalization
Standardizes text fields to maintain consistent formatting.

### Duplicate Detection
Rule used:
Same Email + Same Issue Type within 24 hours

### Automated Issue Routing

| Issue Type | Assigned Team |
|-----------|--------------|
| wifi | Network Team |
| login | IT Support |
| software | Applications Team |
| hardware | Infrastructure Team |
| other | General Support |

### SLA Deadline Calculation

| Priority | SLA Deadline |
|---------|-------------|
| High | 4 hours |
| Medium | 24 hours |
| Low | 72 hours |

### Report Generation

The system generates:
- Processed tickets dataset
- Rejected tickets dataset
- Summary report

---

## Workflow Architecture

Ticket Input → Validation → Normalization → Duplicate Detection → Ticket ID Generation → Issue Routing → SLA Calculation → Processed Ticket Storage → Summary Report Generation

---

## Project Structure

IT_Support_Automation

README.md  
n8n_workflow_design.md  
ticket_automation.py  

sample_tickets.csv  
processed_tickets.csv  
rejected_tickets.csv  
summary_report.csv  

---

## File Descriptions

### ticket_automation.py
Main automation script responsible for validation, routing logic,
SLA calculation, and report generation.

### sample_tickets.csv
Input dataset containing raw IT support tickets.

### processed_tickets.csv
Contains successfully processed tickets.

### rejected_tickets.csv
Contains tickets rejected due to invalid data or duplicates.

### summary_report.csv
Provides overall statistics of processed and rejected tickets.

### n8n_workflow_design.md
Documentation explaining the workflow automation design.

---

## Example Input

name,email,issue_type,priority,description,timestamp
John,john@email.com,wifi,High,Network not working,2026-03-10
Sarah,sarah@email.com,login,Medium,Unable to login,2026-03-10
Mike,mike@email,software,Low,Installation issue,2026-03-10

---

## Example Processed Ticket

ticket_id,name,email,issue_type,priority,team,sla_deadline
TKT001,John,john@email.com,wifi,High,Network,2026-03-10 15:20

---

## Example Rejected Ticket

email,issue,reason
mike@email,software,Invalid Email

---

## Technologies Used

- Python
- CSV data processing
- Regular Expressions (Regex)
- Workflow automation concepts
- n8n workflow design

---

## Benefits

- Faster ticket processing
- Reduced manual workload
- Accurate issue routing
- Prevention of duplicate requests
- Better operational reporting

---

## Future Improvements

- Email notifications for ticket updates
- Slack integration
- Analytics dashboard for IT managers
- AI-based issue classification
- Integration with ServiceNow or Jira

---

## Author

Dayananda S G

Automation Practical Assessment Project
