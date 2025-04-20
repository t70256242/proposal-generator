import time
import os
from datetime import datetime
import streamlit as st
from firebase_config import auth, db
import pycountry
import fitz
from PIL import Image
from cross_plat import EditTextFile
from merge_pdf import Merger
import os
from dotenv import load_dotenv


def get_pdf_preview(file_path):
    doc = fitz.open(file_path)
    page = doc[0]
    pixmap = page.get_pixmap()
    image = Image.frombytes("RGB", [pixmap.width, pixmap.height], pixmap.samples)
    return image


def render_all_pdf_pages(pdf_path):
    images = []
    try:
        doc = fitz.open(pdf_path)
        for page in doc:
            pix = page.get_pixmap(dpi=150)  # Higher DPI = better quality
            img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
            images.append(img)
        return images
    except Exception as e:
        st.error(f"Error rendering PDF: {e}")
        return []


def get_merged_pdf_preview(file_path, page_num=3):
    try:
        doc = fitz.open(file_path)
        page = doc[page_num]
        pix = page.get_pixmap(dpi=150)
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        return img
    except Exception as e:
        st.error(f"Failed to load PDF: {e}")
        return None


page_1_pdf = None

if "page" not in st.session_state:
    st.session_state.page = 1


def next_page():
    st.session_state.page += 1
    # st.rerun()
    st.experimental_rerun()


def prev_page():
    st.session_state.page -= 1
    # st.rerun()
    st.experimental_rerun()


if st.session_state.page == 1:
    st.title("Proposal PDF Generator")
    with st.form("Get Started"):
        name = st.text_input("Name")
        email = st.text_input("Email")
        phone = st.text_input("Phone")
        countries = sorted([country.name for country in pycountry.countries])
        country = st.selectbox("Select Country", countries)
        date = st.date_input("Date")
        submitted = st.form_submit_button("Next")
        if submitted:
            formatted_date = date.strftime("%d %B %Y")
            pdf_editor = EditTextFile("Page1_template.pdf")
            output_pdf = "pdf_list/Page1.pdf"
            modifications = {
                "Name:": f": {name}",
                "Email:": f": {email}",
                "Phone": f": {phone}",
                "Country": f": {country}",
                "14 April 2025": f"{formatted_date}"
            }
            pdf_editor.modify_pdf_fields(output_pdf, modifications, 8)
            next_page()


elif st.session_state.page == 2:
    st.title("Select Index Page Style")
    pdf_file = ["pdf_list/Page2.pdf", "pdf_list/Page2.pdf", "pdf_list/Page2.pdf"]
    pdf_previews = {file: get_pdf_preview(file) for file in pdf_file}
    selected_pdf = st.selectbox("Choose your Template", list(pdf_previews.keys()))

    if selected_pdf:
        st.image(pdf_previews[selected_pdf])
        st.write(f"You selected {selected_pdf}")

    if st.button("Next"):

        next_page()
    if st.button("Previous"):
        prev_page()

    # if st.button("Next", on_click=next_page):  # Use on_click parameter
    #     pass  # The callback already handles the navigation
    #
    # if st.button("Previous", on_click=prev_page):
    #     pass

elif st.session_state.page == 3:

    directory = "pdf_list"
    file_list = [os.path.join(directory, f) for f in os.listdir(directory) if f.endswith(".pdf")]
    rino_p = Merger(file_list)
    pdf_file = "merged(1-6)_preview.pdf"
    rino_p.merge_pdf_files(pdf_file)
    st.title("📄 Full Proposal Preview")

    all_pages = render_all_pdf_pages(pdf_file)

    if all_pages:
        for i, img in enumerate(all_pages):
            st.image(img, caption=f"Page {i + 1}", use_column_width=True)
    else:
        st.warning("No pages found or unable to render PDF.")

    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("Previous"):
            prev_page()
    with col2:
        if st.button("Next"):
            next_page()

# if st.button("Next", on_click=next_page):  # Use on_click parameter
#     pass  # The callback already handles the navigation
#
# if st.button("Previous", on_click=prev_page):
#     pass