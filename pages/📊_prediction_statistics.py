import streamlit as st
import matplotlib.pyplot as plt

st.logo('cropped-radem.png')

    # Create a pie chart
def plot_pie_chart(class_counts, figsize=(4, 2)):
    fig, ax = plt.subplots(figsize=figsize)
    ax.pie(class_counts, labels=class_counts.index, autopct='%1.1f%%', startangle=90, colors=['#ff9999','#66b3ff'])
    ax.axis('equal')  # Equal aspect ratio ensures the pie is drawn as a circle.
    return fig
st.write('### Prediction Percentages')

if 'pourcentage' in st.session_state:
 fig = plot_pie_chart(st.session_state['pourcentage'])
 st.pyplot(fig)


# Filter for fraudulent cases and group by region and district
fraudulent_data = st.session_state['resultspred'][st.session_state['resultspred']['decoded_class'] == 'Fraud']
fraud_counts = fraudulent_data.groupby(['region', 'districts']).size().reset_index(name='count')

st.divider()

# Function to plot the number of fraud cases by region and district
def plot_fraud_by_region_and_district(fraud_counts):
    # Create a bar plot
    fig, ax = plt.subplots(figsize=(10, 6))  # Set figure size
    ax.bar(fraud_counts['region'].astype(str) + ', ' + fraud_counts['districts'].astype(str), fraud_counts['count'], color='green')

    # Set the plot title and labels
    ax.set_title('Number of Fraud Cases by Region and District')
    ax.set_ylabel('Count')
    ax.set_xlabel('Region, District')

    # Rotate the x-axis labels for better readability
    plt.xticks(rotation=45, ha='right')
    
    return fig

st.write('### Number of Fraud Cases by Region and District')
# Example usage
fig = plot_fraud_by_region_and_district(fraud_counts)
st.pyplot(fig)

#  fraud_counts_pivot = fraud_counts.pivot(index='districts', columns='region', values='count').fillna(0)
#  st.bar_chart(fraud_counts_pivot)