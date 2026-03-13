# Automated Video Generation - n8n Workflow Design

This document details how the Python script maps logically to a scalable n8n workflow to fully automate the video generation process end-to-end.

## Scenario
A repeatable automation process that intakes structural text (like announcements) and outlays a generated MP4 file spanning 30-60 seconds combining Audio TTS narration and visual slide rendering without any manual video editing.

---

## 1. n8n Workflow Architecture

If building completely natively within n8n nodes, we approach this by utilizing standard control-flow logic and relying on the Execute Command node to trigger FFmpeg / Moviepy abstractions. 

### Trigger Phase
* **Read File Node** or **Webhook Node**: 
  * Detects when a new `input.txt` file is deposited into a directory OR parses a structured JSON payload submitted via an internal university form containing the announcement script.

### Transformations Phase
* **Code Node (Data Splitting)**:
  * Ingests the raw string payload and uses Javascript (`.split('\n\n')`) to break the text up into distinct arrays (scenes). This ensures one paragraph maps directly to one video slide.
* **Loop Node (Iteration over scenes)**:
  * Iterates through the returned array of scenes sequentially.
* **HTTP Request / Execute Command Node (TTS Engine)**:
  * Takes the current scene's text and pipes it to a free local TTS engine (e.g., executing `gTTS` or `pyttsx3` via CLI command) to render the audio track.
  * Outputs the resulting `.mp3` local file path back to n8n.
* **Execute Command Node (Pillow / ImageMagick)**:
  * Invokes a sub-process passing the scene text, ensuring it word-wraps, and outputs a clean `.png` title card with a designated font and resolution.
* **Execute Command Node (FFmpeg / Moviepy Scene Assembly)**:
  * Concatenates the generated Image card and MP3 track.
  * *Configuration injected here:* Uses FFmpeg logic to measure the audio duration and match the static image presentation to duration + interval padding.  

### Compilation & Output Phase
* **Execute Command Node (Final Render)**:
  * Takes the list of sequential scene video paths and merges them together into the final `explainer_video.mp4`.
* **Sub-Workflow / Error Trigger Nodes (Resilience)**:
  * If the HTTP node storing the audio fails, or the input payload is empty, an Error Trigger branch halts the video processing to save CPU cycles and pushes an alert.

---

## 2. Python Implementation Decisions
To demonstrate this logic Practically, the provided `video_generator.py` script embodies the complete end-to-end architecture described above. Next to n8n, it handles everything natively via Moviepy.

### Key Decisions:
1. **Configurable Parameters:** Near the top of the file, we implemented modular toggles for `RESOLUTION = (1920, 1080)`, `FONT_SIZE = 80`, and most importantly `SLIDE_DURATION_PAD = 0.5`. This padding adds an extra half-second onto the slide *after* the TTS voice completes speaking, making the transitions feel much more human and natural instead of instantly jumping text.
2. **Text Normalization / Wrapping:** `Pillow` lacks native word-wrapping. The script calculates a math ratio of `Maximum letters per line` derived from the configurable Screen Resolution divided by the Font Size padding, utilizing the native `textwrap` module to automatically chop massive paragraphs to fit any screen configuration without bleeding off the edges.
3. **No Paid APIs:** `gTTS` connects seamlessly to Google Translate's free TTS endpoint. This satisfies the rule with vastly superior enunciation natively over system-level robotic voices like `pyttsx3`.
4. **Temporary Artifact Management**: At the very end of the script using a `try-except-finally` structure, the program tracks all transient `.mp3` and `.png` slide elements and deletes them, leaving only the pristine, raw `explainer_video.mp4` output file behind ensuring disk-space longevity on servers.
