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