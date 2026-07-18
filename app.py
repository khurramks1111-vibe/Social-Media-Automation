import streamlit as st
from gtts import gTTS
from PIL import Image, ImageDraw, ImageFont
import requests
import random

def get_real_wikipedia_summary(search_topic):
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        
        # Step 1: Search Wikipedia for articles matching this topic query
        search_url = f"https://en.wikipedia.org/w/api.php?action=query&list=search&srsearch={search_topic}&format=json"
        search_response = requests.get(search_url, headers=headers)
        
        if search_response.status_code == 200:
            search_data = search_response.json()
            search_results = search_data.get("query", {}).get("search", [])
            
            if search_results:
                # Top result ka real title uthain (e.g., "Co-education" or "Mixed-sex education")
                best_title = search_results[0]['title']
                
                # Step 2: Extract the actual summary of that specific article
                summary_url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{best_title.replace(' ', '_')}"
                summary_response = requests.get(summary_url, headers=headers)
                
                if summary_response.status_code == 200:
                    raw_extract = summary_response.json().get("extract", "")
                    if raw_extract and len(raw_extract.strip()) > 20:
                        words = raw_extract.split()
                        return " ".join(words[:110]) + "...", "OK"

        return None, "NO_RESULTS"
    except Exception as e:
        return None, f"ERROR_{str(e)}"

# --- Main App ---
st.set_page_config(page_title="Pro AI Content Tool", page_icon="🤖", layout="centered")

st.title("🤖 Pro Social Media Content Creator")
st.write("Generate a professional social media graphic and voiceover with 100% Real Web Articles!")

topic = st.text_input("Enter any topic (e.g., 'Co education', 'Artificial intelligence', 'Healthy food'):", "")

if st.button("Generate Pro Content"):
    if topic:
        with st.spinner(f"Searching internet databases for real-time summary of '{topic}'..."):
            try:
                final_text, status = get_real_wikipedia_summary(topic)
                
                # Check status and allocate text
                if status == "OK" and final_text:
                    content_text = final_text
                else:
                    # Clear error layout if web data couldn't be indexed properly
                    st.error(f"⚠️ Internet databases par '{topic}' cant find authentic summary. KKindly try a more standard phrase.")
                    st.stop()

                # Single clean output display
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

                base_color = (20, 25, 45)
                img = Image.new('RGB', (W, H), color=base_color)
                draw = ImageDraw.Draw(img)

                pattern_color = (40, 45, 75)
                for _ in range(30):
                    x = random.randint(0, W)
                    y = random.randint(0, H)
                    size = random.randint(2, 6)
                    draw.ellipse([x, y, x+size, y+size], fill=pattern_color)

                line_color = (100, 100, 130)
                header_text = f"REAL CONTENT | {topic.upper()}"
                draw.text((50, 40), header_text, fill=(255, 255, 255), font_size=20)
                draw.line([(50, 75), (W-50, 75)], fill=line_color, width=1)
                draw.line([(50, H-75), (W-50, H-75)], fill=line_color, width=1)
                footer_text = "AUTOMATED TOOL"
                draw.text((W-180, H-60), footer_text, fill=(200, 200, 220), font_size=16)

                draw.text((50, 100), f"DID YOU KNOW?", fill=(255, 215, 0), font_size=40)

                overlay_color = (25, 30, 55)
                text_box_pos = (50, 180, W-50, 700)
                draw.rectangle(text_box_pos, fill=overlay_color)

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
