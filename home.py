import streamlit as st
import pandas as pd

# Load credentials and property listings from CSV
credentials = pd.read_csv("credentials.csv")
property_listings = pd.read_csv("property_listings.csv")

def login():
    st.title("Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if check_credentials(username, password):
            role = get_role(username)
            st.success("Logged in as {} with role {}".format(username, role))
            st.query_params(logged_in=True)
        else:
            st.error("Invalid username or password")

def check_credentials(username, password):
    # Check if username and password match any row in the credentials dataframe
    return any((credentials["username"] == username) & (credentials["password"] == password))

def get_role(username):
    # Retrieve the role of the user from the credentials dataframe
    return credentials.loc[credentials['username'] == username, 'role'].iloc[0]

def show_property_listings():
    st.title("Property Listings")
    st.write(property_listings)

def main():
    if "logged_in" not in st.session_state:
        login()
    elif "logged_in" in st.session_state:
        st.title("Welcome!")
        st.write("You have successfully logged in!")
        show_property_listings()

if __name__ == "__main__":
    main()
