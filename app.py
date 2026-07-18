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
topic = st.text_input("Enter a topic for research (e.g., 'Gender equality', 'Artificial intelligence', 'Coffee'):", "")

if st.button("Generate Content"):
    if topic:
        with st.spinner(f"Searching and generating unique content for '{topic}'..."):
            try:
                # Advanced Wikipedia Search Logic (Bypasses Google 403 Errors perfectly)
                content_text = ""
                
                # 1. Try direct summary first
                formatted_topic = topic.title().replace(' ', '_')
                wiki_url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{formatted_topic}"
                headers = {'User-Agent': 'Mozilla/5.0'}
                response = requests.get(wiki_url, headers=headers)
                
                if response.status_code == 200:
                    raw_text = response.json().get("extract", "")
                    if raw_text:
                        content_text = " ".join(raw_text.split()[:110]) + "..."
                
                # 2. If direct search fails, use Wikipedia Search API to find the closest match
                if not content_text:
                    search_url = f"https://en.wikipedia.org/w/api.php?action=query&list=search&srsearch={topic}&format=json"
                    search_response = requests.get(search_url, headers=headers)
                    if search_response.status_code == 200:
                        search_results = search_response.json().get("query", {}).get("search", [])
                        if search_results:
                            # Get the title of the top search result
                            best_match_title = search_results[0]['title'].replace(' ', '_')
                            fallback_url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{best_match_title}"
                            fallback_res = requests.get(fallback_url, headers=headers)
                            if fallback_res.status_code == 200:
                                raw_text = fallback_res.json().get("extract", "")
                                if raw_text:
                                    content_text = " ".join(raw_text.split()[:110]) + "..."

                # 3. Ultimate smart backup if absolutely nothing is found on Wikipedia
                if not content_text:
                    content_text = f"Let's explore the essential concepts behind {topic}. It represents a unique subject within modern discussions, heavily influencing contemporary ideas, research, and cultural frameworks. Understanding its foundation allows creators, innovators, and professionals to gain distinct insights into its practical impact and future potential."

                # --- SINGLE CLEAN OUTPUT AREA ---
                st.subheader("📝 Generated Content Summary")
                st.write(content_text)

                # Step 3: Generate Voiceover (Audio)
                tts = gTTS(text=content_text, lang='en', slow=False)
                audio_path = "voiceover.mp3"
                tts.save(audio_path)
                
                st.subheader("🔊 Voiceover")
                st.audio(audio_path, format="audio/mp3")

                # Step 4: Generate Pro Graphic Post using Pillow
                image_path = "post_graphic.png"
                W, H = (800, 800)

                # Base Styling
                base_color = (20, 25, 45)
                img = Image.new('RGB', (W, H), color=base_color)
                draw = ImageDraw.Draw(img)

                # AI Pattern
                pattern_color = (40, 45, 75)
                for _ in range(30):
                    x = random.randint(0, W)
                    y = random.randint(0, H)
                    size = random.randint(2, 6)
                    draw.ellipse([x, y, x+size, y+size], fill=pattern_color)

                # Header & Footer Lines
                line_color = (100, 100, 130)
                header_text = f"AI CONTENT | {topic.upper()}"
                draw.text((50, 40), header_text, fill=(255, 255, 255), font_size=20)
                draw.line([(50, 75), (W-50, 75)], fill=line_color, width=1)
                draw.line([(50, H-75), (W-50, H-75)], fill=line_color, width=1)
                footer_text = "AUTOMATED TOOL"
                draw.text((W-180, H-60), footer_text, fill=(200, 200, 220), font_size=16)

                # Title
                draw.text((50, 100), f"DID YOU KNOW?", fill=(255, 215, 0), font_size=40)

                # Text Container Overlay
                overlay_color = (25, 30, 55)
                text_box_pos = (50, 180, W-50, 700)
                draw.rectangle(text_box_pos, fill=overlay_color)

                # Text Wrap Settings
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
                
                y_text = 200
                line_height = 35
                max_lines = (text_box_pos[3] - text_box_pos[1] - 20) // line_height
                lines = lines[:max_lines]

                for line in lines:
                    draw.text((65, y_text), line, fill=(230, 230, 250), font_size=22)
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
