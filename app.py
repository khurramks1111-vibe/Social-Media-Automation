import streamlit as st
from gtts import gTTS
from PIL import Image, ImageDraw, ImageFont
import requests
import os

# Page Configuration
st.set_page_config(page_title="AI Content Automation Tool", page_icon="🤖", layout="centered")

st.title("🤖 Automated Social Media Content Creator")
st.write("Generate a social media graphic post and voiceover automatically on any topic!")

# Step 1: User Input
topic = st.text_input("Enter a topic for research (e.g., 'Python programming', 'Mars', 'Coffee'):", "")

if st.button("Generate Content"):
    if topic:
        with st.spinner("Searching and generating content..."):
            try:
                # Step 2: Automated Research via Wikipedia API (More Reliable Endpoint)
                wiki_url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{topic.title().replace(' ', '_')}"
                response = requests.get(wiki_url)
                
                if response.status_code == 200:
                    data = response.json()
                    raw_text = data.get("extract", "")
                    if raw_text:
                        content_text = " ".join(raw_text.split()[:40]) + "..."
                    else:
                        content_text = f"Discover amazing facts about {topic}! This specialized overview brings you the core concepts, history, and development of {topic} in a concise summary perfect for sharing."
                else:
                    # Dynamic backup text if Wikipedia page doesn't exist
                    content_text = f"Exploring the world of {topic}! In this digital age, {topic} has gained immense significance. Understanding its fundamentals helps content creators and enthusiasts stay ahead with key facts, trends, and valuable insights."

                st.subheader("📝 Generated Content Summary")
                st.write(content_text)

                # Step 3: Generate Voiceover (Audio)
                tts = gTTS(text=content_text, lang='en', slow=False)
                audio_path = "voiceover.mp3"
                tts.save(audio_path)
                
                st.subheader("🔊 Generated Voiceover")
                st.audio(audio_path, format="audio/mp3")

                # Step 4: Generate Graphic Post using Pillow
                image_path = "post_graphic.png"
                bg_path = "bg.jpg" # Make sure to put an image named bg.jpg in your folder
                
                if os.path.exists(bg_path):
                    img = Image.open(bg_path)
                    img = img.resize((800, 800)) # Standard Instagram Square Size
                else:
                    # Fallback: Create a solid dark blue background if bg.jpg is missing
                    img = Image.new('RGB', (800, 800), color=(20, 30, 45))
                
                draw = ImageDraw.Draw(img)
                
                # Overlay Title and Text
                draw.text((50, 100), f"DID YOU KNOW? \n({topic.upper()})", fill=(255, 215, 0)) # Gold Color
                
                # Wrapping text manually for image bounds
                lines = []
                words = content_text.split()
                current_line = ""
                for word in words:
                    if len(current_line + " " + word) < 35:
                        current_line += " " + word
                    else:
                        lines.append(current_line.strip())
                        current_line = word
                if current_line:
                    lines.append(current_line.strip())
                
                y_text = 250
                for line in lines:
                    draw.text((50, y_text), line, fill=(255, 255, 255)) # White Text
                    y_text += 50
                
                img.save(image_path)
                
                st.subheader("🖼️ Generated Graphic Card")
                st.image(image_path, use_container_width=True)

                # Step 5: Download Buttons
                st.subheader("📥 Download Assets")
                col1, col2 = st.columns(2)
                
                with open(audio_path, "rb") as audio_file:
                    col1.download_button(label="🎵 Download Audio", data=audio_file, file_name=f"{topic}_voiceover.mp3", mime="audio/mp3")
                    
                with open(image_path, "rb") as img_file:
                    col2.download_button(label="🖼️ Download Image", data=img_file, file_name=f"{topic}_post.png", mime="image/png")

            except Exception as e:
                st.error(f"Something went wrong: {e}")
    else:
        st.warning("Please enter a topic first!")