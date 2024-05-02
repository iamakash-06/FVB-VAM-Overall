import streamlit as st

st.markdown("# Analytics for Gaze Points")

import os
import pandas as pd

data_dir = "Data_csv"
dataframes = []

for filename in os.listdir(data_dir):
    if filename.endswith(".csv"):
        file_path = os.path.join(data_dir, filename)
        df = pd.read_csv(file_path)
        dataframes.append(df)

combined_df = pd.concat(dataframes, ignore_index=True)

# Print

sorted_df = combined_df.sort_values('Video ID')

filtered_df = combined_df[combined_df['Time (s)'] < 1]

center_counts = filtered_df.groupby(['Center X', 'Center Y']).size().reset_index(name='Count')
highest_frequency = center_counts.sort_values('Count', ascending=False).iloc[0]
highest_frequency_center_x = highest_frequency['Center X']
highest_frequency_center_y = highest_frequency['Center Y']

import matplotlib.pyplot as plt

import pandas as pd
import pandas as pd

# Assuming the dataframe containing the data is named 'combined_df'

# Convert the 'Time (s)' column to datetime format
combined_df['Time (s)'] = pd.to_datetime(combined_df['Time (s)'], unit='s')

# Calculate the time difference between consecutive rows
combined_df['Time Diff'] = combined_df['Time (s)'].diff()

# Identify the saccades (where time difference is greater than a threshold)
threshold = pd.Timedelta(seconds=1)  # Adjust the threshold as needed
combined_df['Saccade'] = combined_df['Time Diff'] > threshold

# Assign a unique identifier to each saccade sequence
combined_df['Saccade ID'] = combined_df['Saccade'].cumsum()

# Group by 'Saccade ID', 'Center X', and 'Center Y' and calculate the total time spent in each saccade sequence
saccade_times = combined_df.groupby(['Saccade ID', 'Center X', 'Center Y'])['Time Diff'].sum().reset_index()

# Sort the saccade sequences by total time spent in descending order
top_saccades = saccade_times.sort_values('Time Diff', ascending=False).head(10)

# Print the top 10 coordinates with respect to continuous time spent
st.write(top_saccades[['Center X', 'Center Y', 'Time Diff']])

#Plot a graph for the above
import matplotlib.pyplot as plt

plt.figure(figsize=(10, 6))
plt.bar(range(len(top_saccades)), top_saccades['Time Diff'].dt.total_seconds())
plt.xlabel('Center X and Center Y')
plt.ylabel('Total Time (seconds)')
plt.title('Top 10 Saccade Sequences by Total Time Spent')
plt.xticks(range(len(top_saccades)), [f"{x}, {y}" for x, y in zip(top_saccades['Center X'], top_saccades['Center Y'])], rotation=90)
st.pyplot(plt.gcf())

#Plot frequency focus graph for the above saccade data and give color to them based on the frequency
colors = top_saccades['Time Diff'].dt.total_seconds()

plt.figure(figsize=(10, 6))
plt.scatter(top_saccades['Center X'], top_saccades['Center Y'], s=top_saccades['Time Diff'].dt.total_seconds()*10, c=colors, cmap='cool', alpha=0.8)
plt.xlabel('Center X')
plt.ylabel('Center Y')
plt.title('Frequency Focus Visualization (Top Saccade Sequences)')
plt.colorbar(label='Total Time (seconds)')
st.pyplot(plt.gcf())


