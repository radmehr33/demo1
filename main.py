import streamlit as st
import folium
from streamlit_folium import folium_static
from PIL import Image
import time
import io
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import html

# Set page config
st.set_page_config(page_title="Insurance Platform Demo", layout="wide")

# Custom CSS
st.markdown("""
<style>
    body {
        color: white;
        background-color: #1E1E1E;
    }
    .stApp {
        margin-left: 0;
    }
    .main .block-container {
        max-width: 100%;
        padding: 1rem;
    }
    [data-testid="stSidebar"] {
        background-color: #2D2D2D;
        padding: 2rem 1rem;
    }
    .sidebar-content {
        color: white;
    }
    .sidebar-title {
        font-size: 1.5rem;
        font-weight: bold;
        margin-bottom: 1rem;
    }
    .sidebar-section-title {
        font-size: 1.1rem;
        font-weight: bold;
        margin-bottom: 0.5rem;
    }
    .sidebar-item {
        background-color: #3D3D3D;
        padding: 0.5rem;
        margin-bottom: 0.5rem;
        border-radius: 4px;
    }
    .stTextInput > div > div > input {
        color: white;
        background-color: #3D3D3D;
    }
    .metric-container {
        display: flex;
        flex-wrap: wrap;
        justify-content: space-between;
        margin-top: 1rem;
    }
    .metric-box {
        background-color: #2D2D2D;
        border-radius: 8px;
        padding: 1rem;
        margin-bottom: 1rem;
        width: calc(25% - 1rem);
        box-sizing: border-box;
    }
    .metric-title {
        font-size: 1.2rem;
        font-weight: bold;
    }
    .metric-value {
        font-size: 2rem;
        font-weight: bold;
        margin: 0.5rem 0;
    }
    .metric-subtitle {
        font-size: 0.9rem;
        color: #CCCCCC;
    }
    .search-box {
        margin: 1rem 0;
    }
    .report-container {
        background-color: #2D2D2D;
        border-radius: 8px;
        padding: 1rem;
        margin-top: 1rem;
    }
    .report-title {
        font-size: 1.5rem;
        font-weight: bold;
        margin-bottom: 1rem;
    }
    .report-content {
        margin-bottom: 1rem;
    }
    .report-images {
        display: flex;
        justify-content: space-between;
        margin-top: 1rem;
    }
    .report-image {
        width: 48%;
    }
    .report-image img {
        width: 100%;
        border-radius: 4px;
    }
    @media (max-width: 768px) {
        .metric-box {
            width: calc(50% - 0.5rem);
        }
        .report-images {
            flex-direction: column;
        }
        .report-image {
            width: 100%;
            margin-bottom: 1rem;
        }
    }
    @media (max-width: 480px) {
        .metric-box {
            width: 100%;
        }
    }
</style>
""", unsafe_allow_html=True)


# Sidebar
def render_sidebar():
    st.sidebar.markdown('<div class="sidebar-title">Starview Model 1.0.0</div>', unsafe_allow_html=True)
    st.sidebar.text_input("Search in history", placeholder="Search...", key="history_search")

    sections = {
        "Yesterday": ["Via Lagrange, 3", "Via Roma, 56", "via luigi, 174", "corso unione sovietica, 473"],
        "Last 7 days": ["Via Roma 45", "Via Garibaldi 12", "Via Dante Alighieri 89", "Via Mazzini 33",
                        "Via Verdi 76", "Via San Marco 50", "Via Manzoni 18", "Via Vittorio Emanuele II 22",
                        "Via del Corso 29"],
        "Last month": ["Via Roma 45", "Via Garibaldi 12", "Via Dante Alighieri 89", "Via Mazzini 33",
                       "Via Verdi 76", "Via San Marco 50"]
    }

    for section, items in sections.items():
        st.sidebar.markdown(f'<div class="sidebar-section-title">{section}</div>', unsafe_allow_html=True)
        for item in items:
            st.sidebar.markdown(f'<div class="sidebar-item">{item}</div>', unsafe_allow_html=True)


# Main content
def render_map():
    # Initialize map centered at Milan
    m = folium.Map(location=[45.4642, 9.1900], zoom_start=13,
                   tiles='https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
                   attr='Esri')

    # Generate 45 random locations for pending claims in Milan
    import random
    random.seed(42)
    pending_claims = [
        [45.4642 + random.uniform(-0.02, 0.02), 9.1900 + random.uniform(-0.02, 0.02)]
        for _ in range(45)
    ]

    # Add markers for each pending claim
    for i, location in enumerate(pending_claims):
        folium.Marker(
            location=location,
            popup=folium.Popup(f'<b>Pending Claim #{i + 1}</b><br><a href="#claim-{i + 1}">Generate Report</a>',
                               max_width=300),
            icon=folium.Icon(color='red', icon='info-sign')
        ).add_to(m)

    # Render the map in Streamlit
    folium_static(m, width=1300, height=400)


def render_metrics():
    st.markdown("""
    <div class="metric-container">
        <div class="metric-box">
            <div class="metric-title">Insured property</div>
            <div class="metric-value">775</div>
        </div>
        <div class="metric-box">
            <div class="metric-title">Pending claims</div>
            <div class="metric-value">45</div>
        </div>
        <div class="metric-box">
            <div class="metric-title">Last event</div>
            <div class="metric-value">Rainfall</div>
            <div class="metric-subtitle">8/10/2024</div>
        </div>
        <div class="metric-box">
            <div class="metric-title">Upcoming</div>
            <div class="metric-value">Hail</div>
            <div class="metric-subtitle">18/10/2024</div>
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_search_box():
    st.markdown('<div class="search-box">', unsafe_allow_html=True)
    user_input = st.text_input("Search the property address/postal code/claim code", key="main_search_box")
    st.markdown('</div>', unsafe_allow_html=True)
    return user_input


def typewriter_effect(text):
    container = st.empty()
    displayed_text = ""
    for char in text:
        displayed_text += char
        container.markdown(displayed_text)
        time.sleep(0.02)
    return container


def show_report(search_query):
    st.markdown(f'<div class="report-container" id="claim-{search_query}">', unsafe_allow_html=True)
    st.markdown(f'<div class="report-title">Report for: {search_query}</div>', unsafe_allow_html=True)

    report_text = [
        "• Mid-level damage: between €2500 to €3000.",
        "• High-level damage: between €12000 to €14000.",
        "Property has been insured on 10/8/2018 until €50000 disasters.",
        "The system automatically scheduled for 18/10/2024 for in-person scheduling and notification with reports has been sent to the inspector."
    ]

    for line in report_text:
        typewriter_effect(html.escape(line))
        time.sleep(0.5)

    try:
        before_image = Image.open("via_garibaldi_12_before.png")
        after_image = Image.open("via_garibaldi_12_after.png")

        st.markdown('<div class="report-images">', unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            st.image(before_image, caption="Before Event", use_column_width=True)
        with col2:
            st.image(after_image, caption="After Event", use_column_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    except FileNotFoundError:
        st.error(
            f"No images found for {search_query}. Please ensure the images are available in the correct directory.")

    if st.button(f'Generate PDF Report for {search_query}'):
        pdf_buffer = generate_pdf_report(search_query, report_text)
        st.download_button(
            label="Download PDF Report",
            data=pdf_buffer,
            file_name=f"insurance_report_{search_query}.pdf",
            mime="application/pdf"
        )

    st.markdown('</div>', unsafe_allow_html=True)


def generate_pdf_report(search_query, report_text):
    pdf_buffer = io.BytesIO()
    c = canvas.Canvas(pdf_buffer, pagesize=letter)
    c.setFont('Helvetica-Bold', 16)
    c.drawString(30, 750, f'Report for: {search_query}')
    c.setFont('Helvetica', 12)
    y = 720

    for line in report_text:
        c.drawString(30, y, line)
        y -= 20

    try:
        c.drawImage("via_garibaldi_12_before.png", 30, y - 200, width=250, height=180)
        c.drawImage("via_garibaldi_12_after.png", 300, y - 200, width=250, height=180)
        c.drawString(30, y - 220, "Before Event")
        c.drawString(300, y - 220, "After Event")
    except:
        c.drawString(30, y - 20, "Images not available")

    c.save()
    pdf_buffer.seek(0)
    return pdf_buffer


def main():
    render_sidebar()
    render_map()
    render_metrics()
    user_input = render_search_box()

    if user_input:
        show_report(user_input)


if __name__ == "__main__":
    main()