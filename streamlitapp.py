import streamlit as st
import pandas as pd
from sqlalchemy import create_engine, text
import base64
import os

# Database connection
db_url = 'mysql+pymysql://root:1234@localhost/redbusinfo'
engine = create_engine(db_url)

# Function to load and encode the image
def load_image(image_path):
    with open(image_path, "rb") as image_file:
        encoded_image = base64.b64encode(image_file.read()).decode()
    return encoded_image

# Path to your image
image_path = r"C:\Users\NAGARAJAN K\Desktop\download.png"  # Use raw string

# Background image path
background_image_path = r"C:\Users\NAGARAJAN K\Desktop\360_F_91454716_m2p0NDccj6Mu8w6IAj3v8KniuvSYlGpO.jpg"  # Use raw string for background image

# Encode images
encoded_image = load_image(image_path)
encoded_background_image = load_image(background_image_path)

# HTML and CSS for the images
image_html = f"""
<div style="position: absolute; top: 0; right: 0;">
    <img src="data:image/png;base64,{encoded_image}" width="70">
</div>
"""

# Display the image in Streamlit
st.markdown(image_html, unsafe_allow_html=True)

# Query the data
def load_data():
    query = text("SELECT * FROM oneRouteBusesInfo")
    with engine.connect() as connection:
        data = pd.read_sql_query(query, con=connection)
    return data

# Streamlit app
def main():
    st.markdown(
        f"""
        <style>
        body {{
            background-image: url('data:image/jpeg;base64,{encoded_background_image}');
            background-size: cover;
        }}
        .title {{
            color: red;
            font-size: 3em;
            font-weight: bold;
            font-family: 'Courier New', Courier, monospace;
        }}
        .header {{
            color: black;
            font-size: 1.5em;
            font-weight: bold;
        }}
        th, td {{
            text-align: center;
            padding: 30px;
            border: 10px solid #001;
        }}
       
    
        </style>
        """,
        unsafe_allow_html=True
    )

    st.markdown('<h1 class="title">RedBus Info</h1>', unsafe_allow_html=True)
    st.markdown('<h2 class="header">Bus Routes Information</h2>', unsafe_allow_html=True)

    # Load data
    data = load_data()

    # Filter sidebar
    st.sidebar.header('Filter Options')
    
    # Route filter
    if 'RouteName' in data.columns:
        route_names = data['RouteName'].unique()
        selected_route = st.sidebar.selectbox('Select Route', route_names)
    else:
        st.sidebar.write("No 'RouteName' column found in data.")

    # Bus type filter
    if 'Bus Type' in data.columns:
        bus_types = data['Bus Type'].unique().tolist()
        bus_types.insert(0, 'All')  # Add 'All' option
        selected_bus_type = st.sidebar.selectbox('Select Bus Type', bus_types)
    else:
        st.sidebar.write("No 'BusType' column found in data.")

    # Price range filter
    if 'Price' in data.columns:
        min_price = data['Price'].min()
        max_price = data['Price'].max()
        selected_price_range = st.sidebar.slider('Select Price Range', min_price, max_price, (min_price, max_price))
    else:
        st.sidebar.write("No 'Price' column found in data.")

    # Star rating filter
    if 'Rating' in data.columns:
        min_rating = data['Rating'].min()
        max_rating = data['Rating'].max()
        selected_rating = st.sidebar.slider('Select Minimum Star Rating', min_rating, max_rating, min_rating)
    else:
        st.sidebar.write("No 'Rating' column found in data.")

    # Availability filter
    if 'Seats Available' in data.columns:
        min_seats = data['Seats Available'].min()
        max_seats = data['Seats Available'].max()
        selected_seats = st.sidebar.slider('Select Minimum Seats Available', min_seats, max_seats, min_seats)
    else:
        st.sidebar.write("No 'Seats Available' column found in data.")

    # Apply filters
    filtered_data = data

    if 'RouteName' in data.columns:
        filtered_data = filtered_data[filtered_data['RouteName'] == selected_route]

    if 'Bus Type' in data.columns and selected_bus_type != 'All':
        filtered_data = filtered_data[filtered_data['Bus Type'] == selected_bus_type]

    if 'Price' in data.columns:
        filtered_data = filtered_data[(filtered_data['Price'] >= selected_price_range[0]) & (filtered_data['Price'] <= selected_price_range[1])]

    if 'Rating' in data.columns:
        filtered_data = filtered_data[filtered_data['Rating'] >= selected_rating]

    if 'Seats Available' in data.columns:
        filtered_data = filtered_data[filtered_data['Seats Available'] >= selected_seats]

    # Add clickable links using the RouteLink column
    if 'RouteLink' in filtered_data.columns:
        filtered_data['RouteLink'] = filtered_data.apply(
            lambda row: f'<a href="{row["RouteLink"]}" target="_blank">{row["RouteName"]}</a>', axis=1
        )

    if filtered_data.empty:
        st.write("No buses available for the selected filters.")
    else:
        st.write(f"Showing data for Route: {selected_route} and Bus Type: {selected_bus_type}")
        
        # Display DataFrame with clickable links
        st.write(filtered_data.to_html(escape=False, index=False), unsafe_allow_html=True)

        # Optional: Show other data visualizations or information
        st.write(f"Total Buses: {len(filtered_data)}")
        if 'Rating' in filtered_data.columns:
            avg_rating = filtered_data['Rating'].mean()
            st.write(f"Average Rating: {avg_rating:.2f}")
        if 'Price' in filtered_data.columns:
            avg_price = filtered_data['Price'].mean()
            st.write(f"Average Price: {avg_price:.2f}")

if __name__ == '__main__':
    main()