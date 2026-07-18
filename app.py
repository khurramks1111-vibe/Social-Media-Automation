import streamlit as st
from gtts import gTTS
from PIL import Image, ImageDraw, ImageFont
import requests
import os
import random

# Page Configuration
st.set_page_config(page_title="Pro AI Content Tool", page_icon="🤖", layout="centered")

st.title("🤖 Pro Social Media Content Creator")
st.write("Generate a professional social media graphic and voiceover automatically!")

# Step 1: User Input
topic = st.text_input("Enter a topic:", "")

if st.button("Generate Pro Content"):
    if topic:
        with st.spinner("Creating professional content..."):
            try:
                # Step 2: Automated Research via Wikipedia API (With Headers)
                wiki_url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{topic.title().replace(' ', '_')}"
                headers = {'User-Agent': 'Mozilla/5.0'} # Keep the browser header
                response = requests.get(wiki_url, headers=headers)
                
                # Default text length limit: 110 words
                if response.status_code == 200:
                    data = response.json()
                    raw_text = data.get("extract", "")
                    if raw_text:
                        content_text = " ".join(raw_text.split()[:110]) + "..."
                    else:
                        content_text = f"Discover key insights about {topic}! This summary provides essential knowledge, historical context, and modern applications of {topic} for creators and professionals."
                else:
                    content_text = f"Explore {topic}! This overview highlights its global significance, core principles, unique features, and future outlook, providing valuable perspectives for enthusiasts and developers."

                st.subheader("📝 Generated Summary")
                st.write(content_text)

                # Step 3: Generate Voiceover (Audio)
                tts = gTTS(text=content_text, lang='en', slow=False)
                audio_path = "voiceover.mp3"
                tts.save(audio_path)
                
                st.subheader("🔊 Voiceover")
                st.audio(audio_path, format="audio/mp3")

                # Step 4: Generate Pro Graphic Post using Pillow
                image_path = "post_graphic.png"
                W, H = (800, 800) # Instagram Square Size

                # A. Create a clean, modern base: Dark Navy with a slight gradient or pattern
                base_color = (20, 25, 45) # Dark Navy
                alt_color = (30, 35, 55) # Slightly Lighter Navy
                img = Image.new('RGB', (W, H), color=base_color)
                draw = ImageDraw.Draw(img)

                # B. Add subtle network/AI pattern element using small circles
                pattern_color = (40, 45, 75)
                for _ in range(30):
                    x = random.randint(0, W)
                    y = random.randint(0, H)
                    size = random.randint(2, 6)
                    draw.ellipse([x, y, x+size, y+size], fill=pattern_color)

                # C. Overlay Header: 'AI CONTENT' and Footer 'TOOL' with lines
                line_color = (100, 100, 130)
                # Header text
                header_text = f"AI CONTENT | {topic.upper()}"
                draw.text((50, 40), header_text, fill=(255, 255, 255), font_size=20)
                # Header horizontal line
                draw.line([(50, 75), (W-50, 75)], fill=line_color, width=1)
                # Footer horizontal line
                draw.line([(50, H-75), (W-50, H-75)], fill=line_color, width=1)
                # Footer text
                footer_text = "AUTOMATED TOOL"
                draw.text((W-180, H-60), footer_text, fill=(200, 200, 220), font_size=16)

                # D. Main Title Area: DID YOU KNOW?
                title_color = (255, 215, 0) # Gold
                title_font_size = 40
                draw.text((50, 100), f"DID YOU KNOW?", fill=title_color, font_size=title_font_size)

                # E. Text Box Overlay for better readability
                overlay_color = (25, 30, 55) # Almost match base, slightly more opaque
                text_box_pos = (50, 180, W-50, 700) # Left, Top, Right, Bottom
                draw.rectangle(text_box_pos, fill=overlay_color)

                # F. Main Text Wrapping and Rendering
                # Use a larger wrap width (70 characters) and tighter line height (35 pixels)
                # to fix the image_0.png gap problem.
                words = content_text.split()
                lines = []
                current_line = ""
                for word in words:
                    if len(current_line + " " + word) < 70:
                        current_line += " " + word
                    else:
                        lines.append(current_line.strip())
                        current_line = word
                if current_line:
                    lines.append(current_line.strip())
                
                main_text_color = (230, 230, 250) # Light lavender-white
                main_font_size = 22
                y_text = 200 # Starting y position inside the text box
                line_height = 35 # Tighter line height
                
                # Calculate how many lines can fit; if text is too long, we stop
                max_lines = (text_box_pos[3] - text_box_pos[1] - 20) // line_height
                lines = lines[:max_lines]

                for line in lines:
                    draw.text((65, y_text), line, fill=main_text_color, font_size=main_font_size)
                    y_text += line_height
                
                img.save(image_path)
                
                st.subheader("🖼️ Pro Graphic Card")
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