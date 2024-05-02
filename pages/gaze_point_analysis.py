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

frequency_df = combined_df.groupby(['Center X', 'Center Y']).size().reset_index(name='Frequency')

threshold = 10
frequency_df = frequency_df[frequency_df['Frequency'] >= threshold]

colors = frequency_df['Frequency']

plt.figure(figsize=(10, 6))
plt.scatter(frequency_df['Center X'], frequency_df['Center Y'], s=frequency_df['Frequency']*10, c=colors, cmap='cool', alpha=0.8)
plt.xlabel('Center X')
plt.ylabel('Center Y')
plt.title('Frequency Focus Visualization (Whole DataFrame)')
plt.colorbar(label='Frequency')
st.pyplot(plt.gcf())

top_coordinates = combined_df.groupby(['Center X', 'Center Y']).size().reset_index(name='Count').nlargest(15, 'Count')

plt.figure(figsize=(10, 6))
plt.bar(range(len(top_coordinates)), top_coordinates['Count'])
plt.xlabel('Center X and Center Y')
plt.ylabel('Count')
plt.title('Top 15 Center X and Center Y Coordinates')
plt.xticks(range(len(top_coordinates)), [f"{x}, {y}" for x, y in zip(top_coordinates['Center X'], top_coordinates['Center Y'])], rotation=90)
st.pyplot(plt.gcf())
