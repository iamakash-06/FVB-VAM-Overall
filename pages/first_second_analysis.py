import streamlit as st

st.markdown("# Analytics for Gaze Points in the 1st Second")

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
print(combined_df)
print(combined_df.describe())
sorted_df = combined_df.sort_values('Video ID')
print(sorted_df)
filtered_df = combined_df[combined_df['Time (s)'] < 1]
print(filtered_df)
center_counts = filtered_df.groupby(['Center X', 'Center Y']).size().reset_index(name='Count')
highest_frequency = center_counts.sort_values('Count', ascending=False).iloc[0]
highest_frequency_center_x = highest_frequency['Center X']
highest_frequency_center_y = highest_frequency['Center Y']

st.write("The highest frequency Center X within 1 second is:", highest_frequency_center_x)
st.write("The highest frequency Center Y within 1 second is:", highest_frequency_center_y)

import matplotlib.pyplot as plt

top_frequencies = filtered_df.groupby(['Center X', 'Center Y']).size().reset_index(name='Frequency').nlargest(15, 'Frequency')

plt.figure(figsize=(10, 6))
plt.bar(range(len(top_frequencies)), top_frequencies['Frequency'])
plt.xlabel('Center X and Center Y')
plt.ylabel('Frequency')
plt.title('Top 15 Center X and Center Y Pair Frequencies')
plt.xticks(range(len(top_frequencies)), [f"{x}, {y}" for x, y in zip(top_frequencies['Center X'], top_frequencies['Center Y'])], rotation=90)
st.pyplot(plt.gcf())

frequency_df = filtered_df.groupby(['Center X', 'Center Y']).size().reset_index(name='Frequency')

frequency_df = frequency_df.sort_values('Frequency', ascending=False)

threshold = 10
frequency_df = frequency_df[frequency_df['Frequency'] >= threshold]

colors = frequency_df['Frequency']

plt.figure(figsize=(10, 6))
plt.scatter(frequency_df['Center X'], frequency_df['Center Y'], s=frequency_df['Frequency']*10, c=colors, cmap='cool', alpha=0.8)
plt.xlabel('Center X')
plt.ylabel('Center Y')
plt.title('Frequency Focus Visualization')
plt.colorbar(label='Frequency')
st.pyplot(plt.gcf())
