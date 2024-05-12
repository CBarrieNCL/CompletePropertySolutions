import streamlit as st

def main():
    st.markdown("""<h1 style="color: #FE7A36; font: "sans serif";>Welcome to Complete Property Solutions</h1>""", unsafe_allow_html=True)
    st.write("Your one-stop solution for all your property needs.")

    st.markdown("---")

    st.markdown("""<h1 style="color: #FE7A36; font: "sans serif";>Services</h1>""", unsafe_allow_html=True)
    st.write("""
    - Property Management
    - Real Estate Sales and Purchases
    - Property Renovations and Repairs
    - Rental Services
    - Property Consultation
    - Legal Assistance
    - Investment Opportunities
    """)

    st.markdown("---")

    st.markdown("""<h1 style="color: #FE7A36; font: "sans serif";>About Us</h1>""", unsafe_allow_html=True)
    st.write("""
    Complete Property Solutions is a leading property management and real estate company dedicated to providing comprehensive services for property owners, investors, and tenants. With years of experience in the industry, we pride ourselves on our professionalism, expertise, and commitment to client satisfaction.

    Our team consists of highly skilled professionals who are passionate about real estate and dedicated to delivering exceptional results. Whether you're a property owner looking for management services, an investor seeking lucrative opportunities, or a tenant searching for the perfect rental, we have the solutions to meet your needs.

    At Complete Property Solutions, we believe in transparency, integrity, and personalized service. We strive to build long-term relationships with our clients based on trust, reliability, and mutual respect.

    Contact us today to learn more about how we can help you achieve your property goals!
    """)

    st.markdown("---")

    st.markdown("""<h1 style="color: #FE7A36; font: "sans serif";>Contact Us</h1>""", unsafe_allow_html=True)
    st.write("""
    **Address:** 123 Main Street, Cityville, State, ZIP  
    **Phone:** (123) 456-7890  
    **Email:** info@completepropsolutions.com
    """)

if __name__ == "__main__":
    main()
