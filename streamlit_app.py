import streamlit as st
import random
from PIL import Image

# Set the title of the app
st.title("Image Uploader")

# Upload images
uploaded_files = st.file_uploader("Upload two images", type=["jpg", "jpeg", "png"], accept_multiple_files=True)

# Check if exactly two images are uploaded
if uploaded_files:
    if len(uploaded_files) != 2:
        st.error("Please upload exactly 2 images.")
    else:
        # Display one randomly selected image
        selected_image = random.choice(uploaded_files)
        image = Image.open(selected_image)
        st.image(image, caption=selected_image.name, use_column_width=True)
else:
    st.info("Please upload two images to see a random one displayed.")