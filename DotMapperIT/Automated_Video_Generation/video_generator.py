import os
import sys
import uuid
import textwrap
from gtts import gTTS
from gtts.tts import gTTSError
from PIL import Image, ImageDraw, ImageFont
from moviepy.editor import ImageClip, AudioFileClip, concatenate_videoclips
import moviepy.config as cfg

# === Configurable Parameters ===
# These configurations allow easy modification of the video generation rules.
RESOLUTION = (1920, 1080)
BG_COLOR = (20, 20, 30)       # Dark blue-grey background
TEXT_COLOR = (255, 255, 255)  # White text
FONT_SIZE = 80
SLIDE_DURATION_PAD = 0.5      # Extra seconds a slide stays on screen after audio finishes
OUTPUT_FILENAME = "explainer_video.mp4"
INPUT_FILENAME = "input.txt"

def load_input(file_path):
    """ Reads the input text and splits it into scenes based on blank lines. """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Input file '{file_path}' not found.")
        
    with open(file_path, "r", encoding="utf-8") as file:
        content = file.read().strip()
        
    if not content:
        raise ValueError("Input file is empty. Cannot generate video.")
        
    # Split by double newlines to treat each paragraph as a distinct slide/scene
    scenes = [scene.strip() for scene in content.split("\n\n") if scene.strip()]
    return scenes

def create_image_for_scene(text, resolution, bg_color, text_color, font_size):
    """ Uses Pillow to dynamically generate a title card / slide for a given scene. """
    img = Image.new('RGB', resolution, color=bg_color)
    draw = ImageDraw.Draw(img)
    
    # Try to load a nice font, fallback to default (default looks very basic, but works)
    try:
        # For Windows environments, try Arial or standard fonts
        font = ImageFont.truetype("arial.ttf", font_size)
    except IOError:
        font = ImageFont.load_default()
        
    # Wrap text logically so it doesn't overflow screen horizontally
    max_chars_per_line = int(resolution[0] / (font_size * 0.6))
    wrapped_text = "\n".join([textwrap.fill(line, width=max_chars_per_line) for line in text.splitlines()])
    
    # Calculate text bounding box to center it
    text_bbox = draw.textbbox((0, 0), wrapped_text, font=font)
    text_w = text_bbox[2] - text_bbox[0]
    text_h = text_bbox[3] - text_bbox[1]
    
    x = (resolution[0] - text_w) / 2
    y = (resolution[1] - text_h) / 2
    
    # Draw text centered on screen
    draw.text((x, y), wrapped_text, font=font, fill=text_color, align='center')
    
    temp_img_path = f"temp_slide_{uuid.uuid4().hex[:6]}.png"
    img.save(temp_img_path)
    return temp_img_path

def generate_audio_for_scene(text):
    """ Converts text to spoken narration using Google TTS. """
    try:
        tts = gTTS(text=text, lang='en', slow=False)
        temp_audio_path = f"temp_audio_{uuid.uuid4().hex[:6]}.mp3"
        tts.save(temp_audio_path)
        return temp_audio_path
    except gTTSError as e:
        raise ConnectionError(f"TTS Failure: Failed to generate audio for text '{text[:20]}...'. Network issue?") from e

def build_workflow():
    """ Main process workflow """
    print("Starting Automated Video Generation Workflow...")
    base_dir = os.path.dirname(os.path.abspath(__file__))
    input_path = os.path.join(base_dir, INPUT_FILENAME)
    output_path = os.path.join(base_dir, OUTPUT_FILENAME)
    
    temp_files = []
    
    try:
        # Step 1: Input Detection
        print(f"Loading input text from {INPUT_FILENAME}...")
        scenes = load_input(input_path)
        print(f"Successfully loaded {len(scenes)} scenes.")
        
        video_clips = []
        
        # Step 2: Transformations
        for i, text in enumerate(scenes):
            print(f"Processing Scene {i+1}/{len(scenes)}...")
            
            # Generate Audio
            audio_path = generate_audio_for_scene(text)
            temp_files.append(audio_path)
            
            # Load audio to get its duration natively
            audio_clip = AudioFileClip(audio_path)
            duration = audio_clip.duration + SLIDE_DURATION_PAD
            
            # Generate Visuals
            image_path = create_image_for_scene(text, RESOLUTION, BG_COLOR, TEXT_COLOR, FONT_SIZE)
            temp_files.append(image_path)
            
            # Create ImageClip overlayed with audio
            image_clip = ImageClip(image_path).set_duration(duration)
            video_clip = image_clip.set_audio(audio_clip)
            
            video_clips.append(video_clip)
            
        # Step 3: Combine Scenes & Export Output
        print(f"Rendering final .mp4 video ({OUTPUT_FILENAME})...")
        final_video = concatenate_videoclips(video_clips, method="compose")
        final_video.write_videofile(output_path, fps=24, codec="libx264", audio_codec="aac", logger=None)
        
        print(f"Success! Video generated entirely via workflow logic at: {output_path}")
        
    except Exception as e:
        # Error handling mechanism
        print(f"\n[ERROR] An error occurred during automation: {str(e)}", file=sys.stderr)
        sys.exit(1)
    finally:
        # Cleanup temp artifacts silently
        for temp_file in temp_files:
            if os.path.exists(temp_file):
                try:
                    os.remove(temp_file)
                except:
                    pass

if __name__ == "__main__":
    build_workflow()
