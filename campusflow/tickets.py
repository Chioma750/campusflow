def validate_title(raw_title):
    cleaned_title = raw_title.strip()
    if cleaned_title == "":
        raise ValueError("Ticket title cannot be blank.")
    return cleaned_title

def validate_category(raw_category):
    cleaned_category = raw_category.strip().title()
    category = ["Network", "Hardware", "Software", "Other"]
    if cleaned_category not in category:
        raise ValueError("Invalid category. Must be Network, Hardware, Software, or Other.")
    return cleaned_category

def validate_urgency(raw_urgency):
    cleaned_urgency = raw_urgency.strip().lower()
    validate = ["low", "medium", "high"]
    if cleaned_urgency not in validate:
        raise ValueError("Invalid urgency. Must be low, medium, or high.")
    return cleaned_urgency

def validate_users(raw_users):
    cleaned_users = raw_users.strip()
    try:
        num_users = int(cleaned_users)
    except ValueError:
            raise ValueError("Affected users must be a valid whole number.")
    if num_users <= 0:
        raise ValueError("Affected users must be a positive integer greater than zero.")
    return num_users

def calculate_priority(urgency, affected_users):
    if urgency == "high" and affected_users >= 10:
        return "critical"
    elif urgency == "high" or (urgency == "medium" and affected_users >= 5):
        return "high"
    elif urgency == "medium" or (urgency == "low" and affected_users >= 10):
        return "medium"
    else:
        return "low"
    
def generate_id(current_tickets):
    if not current_tickets:
        return "T001"
    else:
        id_list = list(current_tickets.keys())
        last_id = id_list[-1]
        last_id[1:]
        next_num = int(last_id[1:]) + 1
        str(next_num).zfill(3)
        return "T" + str(next_num).zfill(3) 

def create_ticket(raw_title, raw_category, raw_urgency, raw_users, current_tickets):
    valid_title = validate_title(raw_title)
    valid_category = validate_category(raw_category)
    valid_urgency = validate_urgency(raw_urgency)
    valid_users = validate_users(raw_users)

    computed_priority = calculate_priority(valid_urgency, valid_users)
    new_id = generate_id(current_tickets)

    new_tickets = {
        "id": new_id,
        "title": valid_title,
        "category": valid_category,
        "urgency": valid_urgency,
        "affected_users": valid_users,
        "priority": computed_priority,
        "status": open,
        "assigned_to": None
    }

    current_tickets[new_id] = new_tickets
