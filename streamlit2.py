import streamlit as st
import pandas as pd
import plotly.express as px

# Title
st.set_page_config(page_title='EV Sales Dashboard', layout='wide')
st.title("India Electric Vehicle Sales Dashboard (2014–2024)")

# Load Data
data = pd.read_csv("Electric Vehicle Sales by State in India.csv")  # Replace with your actual CSV file

# -----------------------
# Data Inspection
# -----------------------
st.sidebar.header("Data Overview")
if st.sidebar.checkbox("Show raw data"):
    st.subheader("Raw Dataset")
    st.dataframe(data)

st.sidebar.write("Shape:", data.shape)
st.sidebar.write("Columns:", list(data.columns))

# -----------------------
# Data Cleaning
# -----------------------
# Convert 'Date' to datetime if needed
if 'Date' in data.columns and data['Date'].dtype == 'object':
    data['Date'] = pd.to_datetime(data['Date'], dayfirst=True, errors='coerce')

# Drop rows with nulls in critical columns
data.dropna(subset=['EV_Sales_Quantity', 'Year', 'Month_Name', 'State'], inplace=True)

# Convert types
cat_cols = ['Month_Name', 'State', 'Vehicle_Class', 'Vehicle_Category', 'Vehicle_Type']
for col in cat_cols:
    data[col] = data[col].astype('category')
data['EV_Sales_Quantity'] = data['EV_Sales_Quantity'].astype(int)

# -----------------------
# Sidebar Filters
# -----------------------
st.sidebar.header("Filters")

years = sorted(data['Year'].unique())
selected_year = st.sidebar.slider("Select Year", min_value=min(years), max_value=max(years), value=(min(years), max(years)))

states = sorted(data['State'].unique())
selected_states = st.sidebar.multiselect("Select States", options=states, default=states)

# Filter data
filtered_data = data[(data['Year'] >= selected_year[0]) & (data['Year'] <= selected_year[1])]
filtered_data = filtered_data[filtered_data['State'].isin(selected_states)]

# -----------------------
# KPI Section
# -----------------------
st.subheader("Key Performance Indicators")
total_sales = filtered_data['EV_Sales_Quantity'].sum()
total_states = filtered_data['State'].nunique()
total_types = filtered_data['Vehicle_Type'].nunique()

col1, col2, col3 = st.columns(3)
col1.metric("Total EV Sales", f"{total_sales:,}")
col2.metric("States Covered", total_states)
col3.metric("Vehicle Types", total_types)

# -----------------------
# Visualization Section
# -----------------------
st.subheader("Visual Exploratory Data Analysis")

# Column 1
col1, col2 = st.columns(2)

with col1:
    # 1. EV Sales by Vehicle Category
    cat_group = filtered_data.groupby('Vehicle_Category')['EV_Sales_Quantity'].sum().reset_index()
    fig1 = px.pie(cat_group, names='Vehicle_Category', values='EV_Sales_Quantity',
                  title='EV Sales by Vehicle Category', hole=0.4)
    fig1.update_traces(textinfo='percent+label', pull=[0.02]*len(cat_group), hoverinfo='label+percent+value', marker=dict(line=dict(color='#000000', width=1)))
    st.plotly_chart(fig1, use_container_width=True)

    # 2. Sales by Vehicle Type
    type_group = filtered_data.groupby('Vehicle_Type')['EV_Sales_Quantity'].sum().reset_index()
    fig2 = px.bar(type_group, x='Vehicle_Type', y='EV_Sales_Quantity', title='EV Sales by Vehicle Type', color='Vehicle_Type',
                  hover_data={'EV_Sales_Quantity': ':.2s'})
    st.plotly_chart(fig2, use_container_width=True)

    # 3. Sales by State
    state_group = filtered_data.groupby('State')['EV_Sales_Quantity'].sum().sort_values(ascending=False).reset_index()
    fig3 = px.bar(state_group, x='State', y='EV_Sales_Quantity', title='EV Sales by State', color='EV_Sales_Quantity',
                  hover_data={'EV_Sales_Quantity': ':.2s'})
    fig3.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(fig3, use_container_width=True)

    # 4. Vehicle Class Distribution
    class_group = filtered_data.groupby('Vehicle_Class')['EV_Sales_Quantity'].sum().reset_index()
    fig5 = px.bar(class_group, x='Vehicle_Class', y='EV_Sales_Quantity', title='Sales by Vehicle Class', color='Vehicle_Class',
                  hover_data={'EV_Sales_Quantity': ':.2s'})
    st.plotly_chart(fig5, use_container_width=True)

    # 5. Yearly Comparison (if multiple years selected)
    if selected_year[1] > selected_year[0]:
        yearwise = filtered_data.groupby(['Year', 'Vehicle_Category'])['EV_Sales_Quantity'].sum().reset_index()
        fig6 = px.bar(yearwise, x='Year', y='EV_Sales_Quantity', color='Vehicle_Category', barmode='group',
                     title='Yearly Sales by Category', hover_data={'EV_Sales_Quantity': ':.2s'})
        st.plotly_chart(fig6, use_container_width=True)

with col2:
    # 6. Total Sales per Month
    monthly_sales = filtered_data.groupby('Month_Name')['EV_Sales_Quantity'].sum().reset_index()
    fig7 = px.bar(monthly_sales, x='Month_Name', y='EV_Sales_Quantity',
                  title='Total Sales per Month', color='EV_Sales_Quantity',
                  hover_data={'EV_Sales_Quantity': ':.2s'})
    st.plotly_chart(fig7, use_container_width=True)

    # 7. Total Sales by Vehicle Class (Filtered)
    filtered_class_sales = filtered_data.groupby('Vehicle_Class')['EV_Sales_Quantity'].sum().reset_index()
    fig8 = px.pie(filtered_class_sales, names='Vehicle_Class', values='EV_Sales_Quantity',
                  title='Total Sales by Vehicle Class (Filtered)', hole=0.4)
    fig8.update_traces(textinfo='percent+label', hoverinfo='label+percent+value',
                       marker=dict(line=dict(color='#000000', width=1)))
    st.plotly_chart(fig8, use_container_width=True)

    # 8. Vehicle Type Comparison
    vehicle_type_comparison = filtered_data.groupby('Vehicle_Type')['EV_Sales_Quantity'].sum().reset_index()
    fig9 = px.bar(vehicle_type_comparison, x='Vehicle_Type', y='EV_Sales_Quantity',
                  title='Vehicle Type Comparison', color='Vehicle_Type',
                  hover_data={'EV_Sales_Quantity': ':.2s'})
    st.plotly_chart(fig9, use_container_width=True)

    # 9. Sales by Vehicle Type and Year
    type_year_group = filtered_data.groupby(['Year', 'Vehicle_Type'])['EV_Sales_Quantity'].sum().reset_index()
    fig10 = px.bar(type_year_group, x='Year', y='EV_Sales_Quantity', color='Vehicle_Type', barmode='group',
                   title='Sales by Vehicle Type Over Years', hover_data={'EV_Sales_Quantity': ':.2s'})
    st.plotly_chart(fig10, use_container_width=True)

    # 10. Total Sales per State by Vehicle Category
    state_category_sales = filtered_data.groupby(['State', 'Vehicle_Category'])['EV_Sales_Quantity'].sum().reset_index()
    fig11 = px.bar(state_category_sales, x='State', y='EV_Sales_Quantity', color='Vehicle_Category',
                   title='Sales per State by Vehicle Category', hover_data={'EV_Sales_Quantity': ':.2s'})
    fig11.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(fig11, use_container_width=True)

# -----------------------
# Advanced Analysis with Animation
# -----------------------
st.subheader("Animated EV Sales Over Time")
animated_data = data.groupby(['Year', 'Vehicle_Type'])['EV_Sales_Quantity'].sum().reset_index()
fig_anim = px.bar(animated_data,
                  x='Vehicle_Type',
                  y='EV_Sales_Quantity',
                  color='Vehicle_Type',
                  animation_frame='Year',
                  title='Animated Vehicle Type Sales Over Years',
                  hover_data={'EV_Sales_Quantity': ':.2s'})
st.plotly_chart(fig_anim, use_container_width=True)

# Footer
st.markdown("---")
st.markdown("*Dashboard by Muhammed Fazal*")