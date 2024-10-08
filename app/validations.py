def validate_hero_power_strength(strength):
    if strength not in ['Strong', 'Weak', 'Average']:
        raise ValueError(f"Invalid strength value: {strength}")

def validate_power_description(description):
    if not description or len(description) < 20:
        raise ValueError("Description must be present and at least 20 characters long")
