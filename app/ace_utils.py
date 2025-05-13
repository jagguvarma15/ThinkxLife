def process_ace_response(responses):
    """
    Convert ['Yes', 'No', 'Skip'] to [1.0, 0.0, 0.25]
    """
    mapped = []
    for r in responses:
        if r == "Yes":
            mapped.append(1.0)
        elif r == "No":
            mapped.append(0.0)
        elif r == "Skip":
            mapped.append(0.25)
    return mapped

def compute_ace_score(responses):
    return round(sum(responses), 2)
