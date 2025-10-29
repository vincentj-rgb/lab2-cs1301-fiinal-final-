# This creates the page for displaying data visualizations.
# It should read data from both 'data.csv' and 'data.json' to create graphs.

import streamlit as st
import pandas as pd
import json # The 'json' module is needed to work with JSON files.
import os   # The 'os' module helps with file system operations.

# PAGE CONFIGURATION
st.set_page_config(
    page_title="Visualizations",
    page_icon="📈",
)

# PAGE TITLE AND INFORMATION
st.title("Data Visualizations 📈")
st.write("This page displays graphs based on the collected data.")


# DATA LOADING
# A crucial step is to load the data from the files.
# It's important to add error handling to prevent the app from crashing if a file is empty or missing.

# TO DO:
# 1. Load the data from 'data.csv' into a pandas DataFrame.
#    - Use a 'try-except' block or 'os.path.exists' to handle cases where the file doesn't exist.
try:
    all_my_hours_df = pd.read_csv("data.csv")
except Exception as e:
    st.stop()
    #I have it read the data from the csv file
    #if it doesnt work, itll stop from the except



    
# 2. Load the data from 'data.json' into a Python dictionary.
#    - Use a 'try-except' block here as well.
try:
    with open('data.json') as f:
        json_contents = json.load(f)
    
    title_from_json = json_contents['chart_title']
    data_points_from_json = json_contents['data_points']

    all_json_data_df = pd.DataFrame(data_points_from_json)
except Exception as e:
    st.stop()
    #First, I have it try to open the json file and load it.
    #After loading it onto a variable i move it into a dataframe by using pd
    #If anything fails, itll go into except and stop it fit anythings broken
    #This was useful when i had to debug as well



# GRAPH CREATION
# The lab requires you to create 3 graphs: one static and two dynamic.
# You must use both the CSV and JSON data sources at least once.

st.divider()
st.header("Graphs")

# GRAPH 1: STATIC GRAPH
st.subheader("Graph 1: How hard each class is") # CHANGE THIS TO THE TITLE OF YOUR GRAPH
# TO DO:
# - Create a static graph (e.g., bar chart, line chart) using st.bar_chart() or st.line_chart().
# - Use data from either the CSV or JSON file.
# - Write a description explaining what the graph shows.
st.write("This graph shows the what I think each classes difficulty is.")
st.bar_chart(all_json_data_df, x="label", y="value") 

    #Essentially, this graph just shows the json files where i listed my classes and how difficult i think they are

# GRAPH 2: DYNAMIC GRAPH
st.subheader("Graph 2: How much I study") # CHANGE THIS TO THE TITLE OF YOUR GRAPH
# TODO:
# - Create a dynamic graph that changes based on user input.
# - Use at least one interactive widget (e.g., st.slider, st.selectbox, st.multiselect).
# - Use Streamlit's Session State (st.session_state) to manage the interaction.
# - Add a '#NEW' comment next to at least 3 new Streamlit functions you use in this lab.
# - Write a description explaining the graph and how to interact with it.
st.write("This line chart shows how much I study")

max_val = 20

if 'hour_limit' not in st.session_state:
    st.session_state.hour_limit = max_val
st.session_state.hour_limit = st.slider("Only show hours LESS than:", 1, max_val, st.session_state.hour_limit)
hours_to_show = all_my_hours_df[ all_my_hours_df['Hours'] < st.session_state.hour_limit ]

st.scatter_chart(hours_to_show) #NEW

    #This graph goes to my CSV file where it holds the amount of hours I study. It plots it on a scatter plot and you can filter how much I studied using the slider.


# GRAPH 3: DYNAMIC GRAPH
st.subheader("Graph 3: How hard a day of Classes will be") # CHANGE THIS TO THE TITLE OF YOUR GRAPH
# TO DO:
# - Create another dynamic graph.
# - If you used CSV data for Graph 1 & 2, you MUST use JSON data here (or vice-versa).
# - This graph must also be interactive and use Session State.
# - Remember to add a description and use '#NEW' comments.
st.write("This area chart shows how much I struggle with my classses throughout the day based on combination.")

all_labels = all_json_data_df['label'].tolist()
if 'labels_to_show' not in st.session_state: #NEW
    st.session_state.labels_to_show = all_labels.copy()
selected_labels = st.multiselect( "Select classes to display:",options=all_labels, default=st.session_state.labels_to_show)#New (label_to_show)

st.session_state.labels_to_show = selected_labels
data_for_plotting = all_json_data_df[all_json_data_df['label'].isin(st.session_state.labels_to_show)]
plot_df_3 = data_for_plotting.set_index("label")

st.area_chart(plot_df_3) #New


    #This graph just demonstrats the integral of each class in a hypothetical combination of classes.
    #The amount under the curve demonstrates how hard each combo would be with the x being the # of classes.
