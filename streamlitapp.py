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
image_path = r'C:\Users\NAGARAJAN K\Desktop\desktop552025\download.png'  # Use raw string

# Background image path
background_image_path = r"C:\Users\NAGARAJAN K\Desktop\redbus project\background.jpg" # Use raw string for background image

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
    # Inject custom CSS for styling
    st.markdown(
        f"""
        <style>
        body {{
            background-image: url('data:image/jpeg;base64,{encoded_background_image}');
            background-size: cover;
            background-attachment: fixed;
            margin: 0;
            padding: 0;
        }}

        .title {{
            color: #e63946;
            font-size: 3rem;
            font-weight: 700;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin-bottom: 0.5rem;
        }}
        .header {{
            color: #333;
            font-size: 1.75rem;
            font-weight: 600;
            margin-bottom: 1rem;
        }}

        .table-container {{
            overflow-x: auto;
            margin: 1.5rem 0;
        }}

        .styled-table {{
            border-collapse: collapse;
            width: 100%;
            min-width: 800px;
            background-color: #fff;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }}
        .styled-table thead tr {{
            background-color: #006d77;
            color: #fff;
            text-align: center;
        }}
        .styled-table th, .styled-table td {{
            padding: 12px 20px;
            border-bottom: 1px solid #e0e0e0;
            text-align:center;
        }}
        .styled-table tbody tr {{
            transition: background-color 0.2s ease-in-out;
        }}
        .styled-table tbody tr:nth-of-type(even) {{
            background-color: #f7f7f7;
        }}
        .styled-table tbody tr:hover {{
            background-color: #e0f7fa;
        }}
        .styled-table tbody tr:last-of-type {{
            border-bottom: 2px solid #006d77;
        }}
        .styled-table a {{
            color: #0077b6;
            text-decoration: none;
            font-weight: 500;
        }}
        .styled-table a:hover {{
            text-decoration: underline;
        }}
        input[type="text"] {{
            padding-left: 30px !important;
            background: url("https://cdn-icons-png.flaticon.com/512/622/622669.png") no-repeat 5px center !important;
            background-size: 20px 20px !important;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

    # Title and header
    st.markdown('<h1 class="title">RedBus Info</h1>', unsafe_allow_html=True)
    st.markdown('<h2 class="header">Bus Routes Information</h2>', unsafe_allow_html=True)

    # Load data
    data = load_data()

    # Sidebar filters
    st.sidebar.header('Filter Options')

    # Route filter
    selected_route = st.sidebar.selectbox('Select Route', data['RouteName'].unique()) if 'RouteName' in data.columns else None
    # Bus Type filter
    bus_types = ['All'] + data['Bus Type'].dropna().unique().tolist() if 'Bus Type' in data.columns else []
    selected_bus_type = st.sidebar.selectbox('Select Bus Type', bus_types) if bus_types else None
    # Price Range filter
    selected_price_range = st.sidebar.slider('Select Price Range', float(data['Price'].min()), float(data['Price'].max()), (float(data['Price'].min()), float(data['Price'].max()))) if 'Price' in data.columns else (0, 0)
    # Star Rating filter
    selected_rating = st.sidebar.slider('Select Minimum Star Rating', float(data['Rating'].min()), float(data['Rating'].max()), float(data['Rating'].min())) if 'Rating' in data.columns else 0
    # Seat Availability filter
    selected_seats = st.sidebar.slider('Select Minimum Seats Available', int(data['Seats Available'].min()), int(data['Seats Available'].max()), int(data['Seats Available'].min())) if 'Seats Available' in data.columns else 0

    # Apply filters
    filtered_data = data.copy()

    if selected_route:
        filtered_data = filtered_data[filtered_data['RouteName'] == selected_route]

    if selected_bus_type and selected_bus_type != 'All':
        filtered_data = filtered_data[filtered_data['Bus Type'] == selected_bus_type]

    filtered_data = filtered_data[
        (filtered_data['Price'] >= selected_price_range[0]) &
        (filtered_data['Price'] <= selected_price_range[1]) &
        (filtered_data['Rating'] >= selected_rating) &
        (filtered_data['Seats Available'] >= selected_seats)
    ]
    search_term = st.text_input("Search Bus Name or Route")

    if search_term:
        filtered_data = filtered_data[
            filtered_data['Bus Name'].str.contains(search_term, case=False, na=False) |
            filtered_data['RouteName'].str.contains(search_term, case=False, na=False)
        ]

    # Make route links clickable
    if 'RouteLink' in filtered_data.columns:
            filtered_data['RouteLink'] = filtered_data.apply(
            lambda row: f'<a href="{row["RouteLink"]}" target="_blank">{row["RouteLink"]}</a>', axis=1
        )

    # Show filtered data or message
    if filtered_data.empty:
        st.warning("No buses available for the selected filters.")
    else:
        st.markdown(f"<div class='table-container'>{filtered_data.to_html(escape=False, index=False, classes='styled-table')}</div>", unsafe_allow_html=True)

        # Summary info
        st.success(f"Total Buses: {len(filtered_data)}")
        if 'Rating' in filtered_data.columns:
            avg_rating = filtered_data['Rating'].mean()
            full_stars = int(avg_rating)
            half_star = avg_rating - full_stars >= 0.5

            stars = '⭐' * full_stars
            if half_star:
                stars += '✨'  # or use '⭐' or '⭑' to indicate a half-star visually

            st.info(f"Average Rating: {avg_rating:.2f}  {stars}")
        if 'Price' in filtered_data.columns:
            st.info(f"Minimum Price: ₹{filtered_data['Price'].min():.2f}")
        if 'Price' in filtered_data.columns:
            st.info(f"Maximum Price: ₹{filtered_data['Price'].max():.2f}")
        if 'Duration' in filtered_data.columns and 'Bus Name' in filtered_data.columns:
            # If Duration is in HH:MM format, convert it to minutes
            def duration_to_minutes(dur_str):
                if isinstance(dur_str, str):
                    # Example: '05h 25m'
                    hours = 0
                    minutes = 0
                    if 'h' in dur_str:
                        parts = dur_str.split('h')
                        hours = int(parts[0].strip())
                        if len(parts) > 1 and 'm' in parts[1]:
                            minutes = int(parts[1].replace('m', '').strip())
                    elif 'm' in dur_str:
                        minutes = int(dur_str.replace('m', '').strip())
                    return hours * 60 + minutes
                else:
                    # If it's already numeric or missing, return 0 or convert safely
                    try:
                        return float(dur_str)
                    except:
                        return 0


            filtered_data['Duration_Minutes'] = filtered_data['Duration'].apply(duration_to_minutes)
            min_duration_idx = filtered_data['Duration_Minutes'].idxmin()
            least_duration_bus_name = filtered_data.loc[min_duration_idx, 'Bus Name']
            least_duration_value = filtered_data.loc[min_duration_idx, 'Duration']

            st.info(f"Fastest Bus: {least_duration_bus_name} (Duration: {least_duration_value})")


if __name__ == '__main__':
    main()
