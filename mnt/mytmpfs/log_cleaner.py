import json
import datetime

def remove_old_log_entries_newline_delimited(filepath, minutes_threshold=2):
    """
    Removes log entries older than a specified number of minutes from a JSON log file
    where each line is a separate JSON object.

    Args:
        filepath: The path to the JSON log file.
        minutes_threshold: The age threshold in minutes. Entries older than this will be removed.
    """
    try:
        filtered_data = []
        now = datetime.datetime.now(datetime.timezone.utc)
        time_threshold = now - datetime.timedelta(minutes=minutes_threshold)

        with open(filepath, 'r') as f:
            for line in f:
                try:
                    entry = json.loads(line)
                    timestamp_str = entry['timestamp']
                    timestamp = datetime.datetime.fromisoformat(timestamp_str)

                    if timestamp.tzinfo is None:
                        timestamp = timestamp.replace(tzinfo=datetime.timezone.utc)

                    if timestamp >= time_threshold:
                        filtered_data.append(entry)
                except (json.JSONDecodeError, KeyError, ValueError):
                    print(f"Skipping line due to invalid JSON or missing/invalid timestamp: {line.strip()}")

        with open(filepath, 'w') as f:
            for entry in filtered_data:
                f.write(json.dumps(entry) + "\n")

        print(f"Removed log entries older than {minutes_threshold} minutes from {filepath}")

    except FileNotFoundError:
        print(f"Error: File not found at {filepath}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

# Example usage:
log_file_path = "eve.json"  # Replace with your log file path
remove_old_log_entries_newline_delimited(log_file_path)
