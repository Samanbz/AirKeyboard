import re
from collections import Counter
import matplotlib.pyplot as plt
from datetime import datetime
import os


def analyze_log_frequency(file_path):
    """
    Reads a log file and analyzes the frequency of 'No landmarks detected' warnings
    in 5-second intervals.

    Args:
        file_path (str): The path to the log file.

    Returns:
        A tuple (Counter, start_time) with normalized timestamps and their counts,
        or (None, None) if the file cannot be read.
    """
    log_pattern = re.compile(
        r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}),\d+ - WARNING - No landmarks detected.*")
    timestamps = []

    if not os.path.exists(file_path):
        print(f"Error: The file '{file_path}' was not found.")
        return None, None

    try:
        with open(file_path, 'r') as f:
            for line in f:
                match = log_pattern.match(line)
                if match:
                    # Convert timestamp string to a datetime object
                    timestamp_str = match.group(1)
                    dt_object = datetime.strptime(
                        timestamp_str, "%Y-%m-%d %H:%M:%S")

                    # Round to the nearest 5-second interval
                    seconds = dt_object.second
                    rounded_seconds = (seconds // 5) * 5
                    rounded_dt = dt_object.replace(second=rounded_seconds)

                    timestamps.append(rounded_dt)
    except Exception as e:
        print(f"Error reading or processing file: {e}")
        return None, None

    if not timestamps:
        return Counter(), None

    # Get the start time (earliest timestamp)
    start_time = min(timestamps)

    # Convert timestamps to seconds from start
    normalized_timestamps = [(dt - start_time).total_seconds()
                             for dt in timestamps]

    return Counter(normalized_timestamps), start_time


def plot_log_frequency(frequency_counters, file_names, start_times):
    """
    Plots the frequency of log warnings over normalized time for multiple log files.

    Args:
        frequency_counters (list): List of Counter objects with normalized timestamps.
        file_names (list): List of file names corresponding to each counter.
        start_times (list): List of start times for reference in the legend.
    """
    if not frequency_counters or all(not counter for counter in frequency_counters):
        print("No data available to plot.")
        return

    plt.figure(figsize=(12, 6))
    colors = plt.cm.tab10.colors

    for i, (counter, file_name, start_time) in enumerate(zip(frequency_counters, file_names, start_times)):
        if counter:
            # Sort the items by timestamp
            sorted_items = sorted(counter.items())

            if sorted_items:
                # Unpack the sorted timestamps and their counts
                norm_seconds, counts = zip(*sorted_items)

                # Convert seconds to minutes for better readability
                norm_minutes = [sec/60 for sec in norm_seconds]

                # Create a label with the original start time
                label = f"{os.path.basename(file_name)}"
                if start_time:
                    label += f" (starts at {start_time.strftime('%H:%M:%S')})"

                plt.plot(norm_minutes, counts, marker='o',
                         color=colors[i % len(colors)], label=label)

    # Formatting the plot
    plt.title('Frequency of "No landmarks detected" Warnings (5-second intervals)')
    plt.xlabel('Minutes from start of each log')
    plt.ylabel('Number of Warnings')
    plt.grid(True)
    plt.legend()
    plt.tight_layout()

    # Show the plot
    plt.show()


def main():
    """
    Main function to run the log analysis and plotting for multiple log files.
    """
    # List of log files to analyze
    # Add more log files as needed
    log_files = ['1.log', '2.log', '3.log', '4.log']

    # Allow command-line arguments to override the default log files
    import sys
    if len(sys.argv) > 1:
        log_files = sys.argv[1:]

    frequencies = []
    valid_files = []
    start_times = []

    for log_file in log_files:
        frequency, start_time = analyze_log_frequency(log_file)

        if frequency:
            print(
                f"\nFrequency of 'No landmarks detected' warnings in {log_file}:")
            for seconds, count in sorted(frequency.items()):
                time_str = f"{int(seconds//60)}m {int(seconds % 60)}s"
                print(f"{time_str} from start: {count} warning(s)")
            frequencies.append(frequency)
            valid_files.append(log_file)
            start_times.append(start_time)
        else:
            print(
                f"No 'No landmarks detected' warnings found or file {log_file} could not be read.")

    if frequencies:
        plot_log_frequency(frequencies, valid_files, start_times)
    else:
        print("No valid data to plot.")


if __name__ == "__main__":
    main()
