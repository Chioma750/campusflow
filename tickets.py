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
    if current_tickets == "":
        return "T001"