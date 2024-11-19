import os
import glob
import re
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import pandas as pd

# Directory where RTT files are located
data_dir = './stats'  # Change this if your RTT files are in a different directory

# Initialize a list to store RTT data
rtt_data = []

# Construct the file pattern to search for RTT files
file_pattern = os.path.join(data_dir, 'rtt_P*_W*.txt')

# Get the list of RTT files in the specified directory
files = glob.glob(file_pattern)

# Iterate over each file to extract RTT values
for filepath in files:
    # Extract the filename without directory path
    filename = os.path.basename(filepath)

    # Extract P and W values from the filename using regex
    match = re.match(r'rtt_P(\d+)_W([^\s\.]+)\.txt', filename)
    if match:
        P = int(match.group(1))
        W = match.group(2)
        # Read RTT values from the file
        with open(filepath, 'r') as f:
            lines = f.readlines()
            rtt_values = []
            for line in lines:
                # Look for lines containing 'time='
                if 'time=' in line:
                    # Extract the RTT value using regex
                    match_rtt = re.search(r'time=([\d\.]+) ms', line)
                    if match_rtt:
                        rtt = float(match_rtt.group(1))
                        rtt_values.append(rtt)
            # Store the RTT values along with P and W
            if rtt_values:
                for rtt in rtt_values:
                    rtt_data.append({'P': P, 'W': W, 'RTT': rtt})
            else:
                print(f"No RTT values found in file {filename}.")
    else:
        print(f"Filename {filepath} does not match the expected pattern.")

# Check if any data was collected
if not rtt_data:
    print("No RTT data found. Please ensure RTT files are in the correct format.")
    exit()

# Convert the data into a Pandas DataFrame
df = pd.DataFrame(rtt_data)

# Create a directory to save the plots
output_dir = 'rtt_boxplots'
os.makedirs(output_dir, exist_ok=True)

# Plot settings
sns.set(style="whitegrid")

# Unique window sizes and P values
window_sizes = sorted(df['W'].unique())
P_values = sorted(df['P'].unique())

# For each window size, create a boxplot of RTT distributions for different P values
for W in window_sizes:
    plt.figure(figsize=(10, 6))
    sns.boxplot(x='P', y='RTT', data=df[df['W'] == W])
    plt.title(f'RTT Distribution for Window Size W={W}')
    plt.xlabel('Number of Parallel Streams (P)')
    plt.ylabel('RTT (ms)')
    plt.tight_layout()
    # Save the plot
    plot_filename = f'rtt_boxplot_W{W}.png'
    plt.savefig(os.path.join(output_dir, plot_filename))
    plt.close()
    print(f"Saved RTT boxplot for W={W} as {plot_filename}")

# Alternatively, for each P, create a boxplot of RTT distributions for different window sizes
for P in P_values:
    plt.figure(figsize=(10, 6))
    sns.boxplot(x='W', y='RTT', data=df[df['P'] == P])
    plt.title(f'RTT Distribution for P={P}')
    plt.xlabel('Window Size (W)')
    plt.ylabel('RTT (ms)')
    plt.tight_layout()
    # Save the plot
    plot_filename = f'rtt_boxplot_P{P}.png'
    plt.savefig(os.path.join(output_dir, plot_filename))
    plt.close()
    print(f"Saved RTT boxplot for P={P} as {plot_filename}")

# Optionally, create a combined plot for all data
plt.figure(figsize=(12, 8))
sns.boxplot(x='W', y='RTT', hue='P', data=df)
plt.title('RTT Distribution Across Window Sizes and Parallel Streams')
plt.xlabel('Window Size (W)')
plt.ylabel('RTT (ms)')
plt.legend(title='P')
plt.tight_layout()
plot_filename = 'rtt_boxplot_all.png'
plt.savefig(os.path.join(output_dir, plot_filename))
plt.close()
print(f"Saved combined RTT boxplot as {plot_filename}")

print("All RTT boxplots have been generated and saved.")
