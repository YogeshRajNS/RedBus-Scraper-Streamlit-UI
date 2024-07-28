# RedBus Web Scraping Project
This project involves scraping bus details from the RedBus website for ten states, covering both government and private bus services. The scraped data is stored in a MySQL database, and a Streamlit-based user interface allows for data visualization and interaction.

Features:
Web scraping of bus information from RedBus using Selenium.
Data stored includes route name, route link, bus name, bus type, departing time, duration, reaching time, star rating, price, and seats available.
Data storage in a MySQL database.
Streamlit user interface with filters to select and view bus details.
Displays average rating and price for each route.
Provides links for users to redirect to the RedBus site for booking.
Technologies Used:
Python
Selenium
MySQL
Streamlit
Setup and Installation:
Clone the repository.
Install the required dependencies using pip install -r requirements.txt.
Set up the MySQL database and update the connection details in the configuration file.
Run the Streamlit application using streamlit run app.py.
Usage:
Scrape data by running the Selenium scraper script.
Launch the Streamlit UI to interact with and visualize the scraped data.
Use filters to find specific bus routes, view average ratings and prices, and access booking links.
