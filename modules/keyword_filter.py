# modules/keyword_filter.py
def apply_keyword_filter(logs_dict, keyword_string):
    if not keyword_string:
        return logs_dict

    keywords = [kw.strip().lower() for kw in keyword_string.split(",")]
    filtered_logs = {}

    for key, content in logs_dict.items():
        lines = content.splitlines()
        filtered = [line for line in lines if any(kw in line.lower() for kw in keywords)]
        filtered_logs[key] = "\n".join(filtered) if filtered else "No matching lines found."

    return filtered_logs