import streamlit as st
import random
import os
import uuid
from PIL import Image
import compare as cp

# Set the title of the app
st.title("Image Uploader")

# Create a temporary directory to store images
temp_dir = "temp_images"
os.makedirs(temp_dir, exist_ok=True)

# Upload images
uploaded_files = st.file_uploader("Upload two images", type=["jpg", "jpeg", "png"], accept_multiple_files=True)

# Check if exactly two images are uploaded
if uploaded_files:
    if len(uploaded_files) != 2:
        st.error("Please upload exactly 2 images.")
    else:
        # Save images with a random name
        saved_images = []
        for file in uploaded_files:
            random_name = f"{uuid.uuid4()}.{file.name.split('.')[-1]}"
            file_path = os.path.join(temp_dir, random_name)
            with open(file_path, "wb") as f:
                f.write(file.getbuffer())
                f.close()
            saved_images.append(file_path)

        result, finalimg1, finalimg2 = cp.main_app(saved_images[0], saved_images[1])
        if result == "success":
            st.image(saved_images[0], use_container_width=True)
            st.image(finalimg1, use_container_width=True)
            st.image(finalimg2, use_container_width=True)
        else:
            st.info(result)
        # Display one randomly selected image
        #selected_image_path = random.choice(saved_images)
        #image = Image.open(selected_image_path)
        #st.image(image, caption=os.path.basename(selected_image_path), use_container_width=True)

        # Delete the saved images after displaying
        for img_path in saved_images:
            os.remove(img_path)
        #os.rmdir(temp_dir)  # Remove the temporary directory if empty
else:
    st.info("Please upload two images to see a random one displayed.")