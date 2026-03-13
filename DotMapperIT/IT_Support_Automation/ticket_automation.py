import csv
import re
import uuid
from datetime import datetime, timedelta
from collections import defaultdict

# --- Configuration & Mappings ---
ROUTING_RULES = {
    'wifi': 'Network',
    'login': 'IT Support',
    'software': 'Applications',
    'hardware': 'Infrastructure',
    'other': 'General'
}

SLA_RULES_HOURS = {
    'high': 4,
    'medium': 24,
    'low': 72
}

VALID_PRIORITIES = set(SLA_RULES_HOURS.keys())
EMAIL_REGEX = re.compile(r"^[^@]+@[^@]+\.[^@]+$")

# Mock data for demonstration (simulates incoming tickets or CSV upload)
MOCK_INPUT = [
    {"Name": "Alice", "Email": "alice@university.edu", "Issue Type": "wifi", "Priority": "High", "Description": "Cannot connect to eduroam", "Timestamp": "2023-10-01T08:00:00"},
    {"Name": "Bob", "Email": "bob@university.edu", "Issue Type": "Login", "Priority": "Medium", "Description": "Forgot password", "Timestamp": "2023-10-01T09:00:00"},
    {"Name": "Charlie", "Email": "invalid-email", "Issue Type": "software", "Priority": "Low", "Description": "Need SPSS", "Timestamp": "2023-10-01T10:00:00"},
    {"Name": "Alice", "Email": "alice@university.edu", "Issue Type": "wifi", "Priority": "High", "Description": "Still cannot connect to eduroam", "Timestamp": "2023-10-01T08:30:00"}, # Duplicate
    {"Name": "Dave", "Email": "dave@university.edu", "Issue Type": "unknown_issue", "Priority": "High", "Description": "Help", "Timestamp": "2023-10-01T11:00:00"},
]

def process_tickets(input_data):
    """
    Core automation logic to validate, transform, route, and apply SLA to tickets.
    """
    processed_tickets = []
    rejected_tickets = []
    
    # For deduplication: store the latest timestamp of a particular email + issue type
    # Using a dictionary: (email, issue_type) -> datetime
    ticket_history = {}
    
    for row in input_data:
        reject_reasons = []
        
        # 1. Normalize text fields
        name = str(row.get('Name', '')).strip()
        email = str(row.get('Email', '')).strip().lower()
        issue_type = str(row.get('Issue Type', '')).strip().lower()
        priority = str(row.get('Priority', '')).strip().lower()
        description = str(row.get('Description', '')).strip()
        timestamp_str = str(row.get('Timestamp', '')).strip()
        
        # Parse timestamp safely
        try:
            # Assuming ISO format for simplicity
            ticket_time = datetime.fromisoformat(timestamp_str)
        except ValueError:
            reject_reasons.append("Invalid Timestamp format")
            ticket_time = datetime.now() # Fallback for further processing
            
        # 2. Mandatory Transformations & Validations
        if not EMAIL_REGEX.match(email):
            reject_reasons.append("Invalid Email")
            
        if priority not in VALID_PRIORITIES:
            reject_reasons.append("Invalid Priority")
            
        route_team = ROUTING_RULES.get(issue_type)
        if not route_team:
            reject_reasons.append("Unknown Issue Type")
            
        # Deduplication Check (Same email + issue within 24 hours)
        dedup_key = (email, issue_type)
        if dedup_key in ticket_history:
            last_time = ticket_history[dedup_key]
            if (ticket_time - last_time).total_seconds() <= 24 * 3600:
                reject_reasons.append("Duplicate Ticket (Within 24h)")
                
        # Generate Unique ID
        ticket_id = str(uuid.uuid4())[:8] # Short UUID for readability
        
        # 3. Routing Rules (Handled above via ROUTING_RULES)
        
        # 4. SLA Rules
        sla_deadline = None
        if priority in SLA_RULES_HOURS:
            sla_deadline = ticket_time + timedelta(hours=SLA_RULES_HOURS[priority])
            
        # 5. Error Handling Routing
        if reject_reasons:
            row['Reject_Reason'] = " | ".join(reject_reasons)
            rejected_tickets.append(row)
        else:
            # Update history cache for future deduplication checks
            ticket_history[dedup_key] = ticket_time
            
            processed_tickets.append({
                'Ticket_ID': ticket_id,
                'Name': name,
                'Email': email,
                'Issue_Type': issue_type,
                'Priority': priority,
                'Description': description,
                'Timestamp': timestamp_str,
                'Routed_Team': route_team,
                'SLA_Deadline': sla_deadline.isoformat() if sla_deadline else ""
            })
            
    return processed_tickets, rejected_tickets

def generate_reports(processed, rejected):
    """
    Generates required outputs (CSV and summaries)
    """
    # Summary calculations
    total_received = len(processed) + len(rejected)
    processed_count = len(processed)
    rejected_count = len(rejected)
    
    tickets_per_team = defaultdict(int)
    for t in processed:
        tickets_per_team[t['Routed_Team']] += 1
        
    summary = {
        "Total Received": total_received,
        "Processed": processed_count,
        "Rejected": rejected_count,
        "Tickets per Team": dict(tickets_per_team)
    }
    
    # Write Output to CSV
    try:
        if processed:
            with open('processed_tickets.csv', 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=processed[0].keys())
                writer.writeheader()
                writer.writerows(processed)
                
        if rejected:
            with open('rejected_tickets.csv', 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=rejected[0].keys())
                writer.writeheader()
                writer.writerows(rejected)
                
        # Write Summary Report
        with open('summary_report.csv', 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(["Metric", "Value"])
            writer.writerow(["Total Tickets Received", summary["Total Received"]])
            writer.writerow(["Processed", summary["Processed"]])
            writer.writerow(["Rejected", summary["Rejected"]])
            writer.writerow([])
            writer.writerow(["Team", "Ticket Count"])
            for team, count in summary["Tickets per Team"].items():
                writer.writerow([team, count])
                
        print("Successfully generated output data: processed_tickets.csv, rejected_tickets.csv, and summary_report.csv")
    except Exception as e:
        print(f"Storage failure occurred while saving attachments: {str(e)}")
        
    return summary

if __name__ == "__main__":
    print("Executing IT Support Ticket Automation pipeline...")
    processed, rejected = process_tickets(MOCK_INPUT)
    summary = generate_reports(processed, rejected)
    
    print("\n--- Pipeline Summary ---")
    import json
    print(json.dumps(summary, indent=2))
