# IT Support Ticket Automation Design

This document details the configuration and reasoning behind the automated IT Support ticket pipeline. The provided Python implementation acts interchangeably with the intended logic to be replicated in n8n.

## 1. n8n Workflow Steps

If implemented directly in n8n, here are the logical steps and nodes required to fulfill all assessment constraints.

### Trigger Phase
* **Webhook Node** or **Read File/CSV Node**: Triggers the automation when a new individual ticket is submitted via an API call from an internal portal/form, or runs chronologically/manually when a CSV file is uploaded.

### Transformation & Validation Phase
* **Set Node (Data Normalization)**: 
  * Converts text inside `email`, `priority`, and `issue type` variables to lowercase.
  * Trims leading/trailing whitespaces from `name` and `description` applying string operation expressions.
* **Crypto Node**: Generate a UUID/hash for the `Ticket ID`.
* **Database/Memory / Function Node (Deduplication)**:
  * Check against a database (e.g., PostgreSQL or Google Sheets node querying recent rows) to find if an identical `email` + `issue type` combination exists where `Timestamp` is less than 24 hours old.
* **If / Switch Nodes (Validation)**:
  * Validate Email format using Regex (`^[^@]+@[^@]+\.[^@]+$`).
  * Check if `priority` matches predetermined values (low, medium, high).
  * Check if `issue type` is known.

### Routing Phase
* **Switch Node (Routing)**:
  * Evaluates the validated `Issue Type`.
  * Routes to branches: `wifi` -> Network, `login` -> IT Support, `software` -> Applications, `hardware` -> Infrastructure, default (`other`) -> General.

### SLA Calculation Phase
* **Date & Time Node**: 
  * Based on the routed priority, mathematically increment and adjust the `Timestamp` attribute to calculate the SLA Deadline.
  * Adds intervals: High (+4 hours), Medium (+24 hours), Low (+72 hours).

### Error Handling Phase
* **Error Trigger Node**: Failsafe mechanism that captures unhandled n8n application exceptions (e.g. Server storage failure) and relays an operation alert to DevOps.
* **Filter / If Nodes**: When validation rules fail (e.g., invalid email, duplicate ticket, unknown issue type), the node splits the flow to bypass the SLA and routing. It captures the reason for the failure in a `Reject_Reason` field.

### Output Generation Phase
* **Read/Write Spreadsheet Node / Database Nodes**: Iterates and commits the valid processed tickets with their Routed Team and SLA Deadline onto a processed datastore. It stores invalidated tickets in a rejected datastore.
* **Code / Aggregate Node**: Generates the final count summary (Total received, processed vs. rejected, tickets per team breakdown).
* **Spreadsheet File Node**: Generates the CSV files output for `Processed` and `Rejected` tickets along with compiling the Summary report.

---

## 2. Python Implementation Logic

To meet the scope of submitting code alongside workflow descriptions, `ticket_automation.py` models the precise requirements of the system.

### Key Decisions Made:
1. **Deduplication Strategy**: We use an in-memory dictionary storing `(email, issue_type)` as keys and their latest submission timestamp as the value. Within the loop, if an identical key is spotted within `< 24 hours`, it gets explicitly flagged as rejected. In a production state mapping to n8n, this cache would act as a Redis instance or small database cache.
2. **Graceful Error Handling / Continuation**: Instead of halting script execution when a validation phase fails, the script continues evaluating the payload, accumulates all potential rejection reasons, and correctly shuttles the ticket object to the discarded/error queue.
3. **Data Normalization Prioritization**: Text inputs are stripped of leading/trailing spaces, and critical logic fields (`email`, `priority`, `issue type`) are explicitly converted to lowercase immediately. This eliminates syntax bugs guaranteeing downstream processes (Router matching and Validation sets) function properly, unaffected by bad user input casing.
4. **Resilient Timestamps**: We heavily rely on accurate dates for the Deduplication and SLA features. By wrapping parsed datetime conversions in `try...except` blocks, we simulate an 'Error Handling' procedure ensuring if an erroneous string is received, the system gracefully generates a rejection flag but prevents fatal crashes.
