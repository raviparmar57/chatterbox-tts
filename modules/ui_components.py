"""
UI Components for Chatterbox TTS Enhanced
Contains function to create each tab's UI layout
"""
import gradio as gr
from .config import LANGUAGE_CONFIG, SUPPORTED_LANGUAGES
from .voice_manager import load_voices, get_voices_for_language, get_all_voices_with_gender


def create_header():
    """Create the application header."""
    gr.HTML("""
        <h1 style="font-size: 2.5em; margin-bottom: 0.5rem; text-align: center;">🎙️ Chatterbox TTS (Supports 23 Languages) </h1>
        <p style='text-align: center; font-size: 1.2em; color: #666;'>High-Quality Voice Cloning, Text-to-Speech & Voice Conversion</p>
        
        <!-- Channel Section -->
        <div style="display: flex; justify-content: center; align-items: center; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    padding: 1.5rem; border-radius: 12px; box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15); 
                    margin: 1.5rem auto; max-width: 700px;">
            <div style="display: flex; align-items: center; gap: 1.5rem; width: 100%;">
                               <img src="data:image/jpeg;base64,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" alt="Channel Logo" style="width: 60px; height: 60px; border-radius: 50%; border: 2px solid #ccc; object-fit: cover;">

            <div style="text-align: left; flex-grow: 1; color: white;">
                <h3 style="margin: 0; font-size: 1.5rem; font-weight: 600;">Chatterbox by The Oracle Guy</h3>
                <p style="font-size: 1rem; margin-top: 0.5rem; opacity: 0.9;">Subscribe for more such future releases!</p>
            </div>
            <!-- Subscribe Button -->
            <a href="https://www.youtube.com/@theoracleguy_AI?sub_confirmation=1" target="_blank"
                style="background-color: #E74C3C; color: white; padding: 10px 20px; font-size: 1.1rem;
                        text-decoration: none; border-radius: 4px; font-weight: 600; display: inline-flex;
                        align-items: center; gap: 12px; box-shadow: 0 4px 8px rgba(255, 0, 0, 0.2);
                        transition: background-color 0.3s, box-shadow 0.3s;">
                Subscribe
            </a>
        </div>
    </div>
    """)


def create_tts_tab():
    """Create the UI for Text-to-Speech tab."""
    with gr.Row():
        with gr.Column():
            text = gr.Textbox(
                value="Hey there! I'm The Oracle Guy, and I'm unlocking the secrets of AI!",
                label="Text to synthesize (unlimited length - smart chunking enabled)",
                max_lines=5,
                placeholder="Enter text to convert to speech..."
            )
            
            voice_select_tts = gr.Dropdown(
                label="Select Voice",
                choices=get_voices_for_language("en"),
                value=f"Default ({SUPPORTED_LANGUAGES['en']})",
                info="Select a cloned voice or use default"
            )
            
            preview_audio_tts = gr.Audio(label="Voice Preview", interactive=False, visible=True)
            
            gr.Markdown("**Language:** English only for this tab. Use Multilingual TTS for other languages.")
            
            exaggeration = gr.Slider(0.25, 2, step=.05, label="Exaggeration (Neutral = 0.5)", value=.5)
            cfg_weight = gr.Slider(0.0, 1, step=.05, label="CFG/Pace", value=0.5)

            with gr.Accordion("⚙️ Advanced Options", open=False):
                seed_num = gr.Number(value=0, label="Random seed (0 for random)")
                temp = gr.Slider(0.05, 5, step=.05, label="Temperature", value=.8)
                min_p = gr.Slider(0.00, 1.00, step=0.01, label="min_p (0.00 disables)", value=0.05)
                top_p = gr.Slider(0.00, 1.00, step=0.01, label="top_p (1.0 disables)", value=1.00)
                repetition_penalty = gr.Slider(1.00, 2.00, step=0.1, label="Repetition Penalty", value=1.2)

            generate_btn = gr.Button("🎙️ Generate Speech", variant="primary", size="lg")

        with gr.Column():
            progress_bar_tts = gr.Slider(label="Progress", minimum=0, maximum=100, value=0, interactive=False)
            status_box_tts = gr.Textbox(label="Status", value="Ready to generate...", lines=3, interactive=False)
            audio_output_tts = gr.Audio(label="Generated Audio", autoplay=True, show_download_button=True)

    return {
        "text": text,
        "voice_select": voice_select_tts,
        "exaggeration": exaggeration,
        "cfg_weight": cfg_weight,
        "seed_num": seed_num,
        "temp": temp,
        "min_p": min_p,
        "top_p": top_p,
        "repetition_penalty": repetition_penalty,
        "generate_btn": generate_btn,
        "progress_bar": progress_bar_tts,
        "status_box": status_box_tts,
        "audio_output": audio_output_tts,
        "preview_audio": preview_audio_tts
    }


def create_multilingual_tab():
    """Create the UI for Multilingual TTS tab."""
    with gr.Row():
        with gr.Column():
            text_mtl = gr.Textbox(
                value=LANGUAGE_CONFIG["fr"]["text"],
                label="Text to synthesize (unlimited length - smart chunking enabled)",
                max_lines=5,
                placeholder="Enter text in any supported language..."
            )
            
            language_select_mtl = gr.Dropdown(
                label="Language",
                choices=[(f"{name} ({code})", code) for code, name in sorted(SUPPORTED_LANGUAGES.items())],
                value="fr",
                info="Select the language of your text"
            )
            
            voice_select_mtl = gr.Dropdown(
                label="Select Voice",
                choices=get_voices_for_language("fr"),
                value=f"Default ({SUPPORTED_LANGUAGES['fr']})",
                info="Select a voice for this language"
            )
            
            sample_audio_mtl = gr.Audio(
                label="Voice Preview",
                value=LANGUAGE_CONFIG["fr"]["audio"],
                interactive=False
            )
            
            exaggeration_mtl = gr.Slider(0.25, 2, step=.05, label="Exaggeration (Neutral = 0.5)", value=.5)
            cfg_weight_mtl = gr.Slider(0.0, 1, step=.05, label="CFG/Pace", value=0.5)

            with gr.Accordion("⚙️ Advanced Options", open=False):
                seed_num_mtl = gr.Number(value=0, label="Random seed (0 for random)")
                temp_mtl = gr.Slider(0.05, 5, step=.05, label="Temperature", value=.8)

            generate_btn_mtl = gr.Button("🎙️ Generate Speech", variant="primary", size="lg")

        with gr.Column():
            progress_bar_mtl = gr.Slider(label="Progress", minimum=0, maximum=100, value=0, interactive=False)
            status_box_mtl = gr.Textbox(label="Status", value="Ready to generate...", lines=3, interactive=False)
            audio_output_mtl = gr.Audio(label="Generated Audio", autoplay=True, show_download_button=True)
            
            gr.Markdown(f"""
            ### Supported Languages ({len(SUPPORTED_LANGUAGES)}):
            {', '.join([f"**{name}**" for name in sorted(SUPPORTED_LANGUAGES.values())])}
            """)

    return {
        "text": text_mtl,
        "language_select": language_select_mtl,
        "voice_select": voice_select_mtl,
        "sample_audio": sample_audio_mtl,
        "exaggeration": exaggeration_mtl,
        "cfg_weight": cfg_weight_mtl,
        "seed_num": seed_num_mtl,
        "temp": temp_mtl,
        "generate_btn": generate_btn_mtl,
        "progress_bar": progress_bar_mtl,
        "status_box": status_box_mtl,
        "audio_output": audio_output_mtl
    }


def create_voice_conversion_tab():
    """Create the UI for Voice Conversion tab."""
    with gr.Row():
        with gr.Column():
            gr.Markdown("""
            ### Convert any voice to another!
            Upload an audio file and select a target voice to convert it.
            """)
            
            input_audio_vc = gr.Audio(
                label="Input Audio",
                sources=["upload", "microphone"],
                type="filepath"
            )
            
            target_voice_select = gr.Dropdown(
                label="Target Voice",
                choices=["None"] + get_all_voices_with_gender(),
                value="None",
                info="Select target voice or use default"
            )
            
            preview_audio_vc = gr.Audio(label="Target Voice Preview", interactive=False, visible=True)
            
            convert_btn = gr.Button("🔄 Convert Voice", variant="primary", size="lg")

        with gr.Column():
            progress_bar_vc = gr.Slider(label="Progress", minimum=0, maximum=100, value=0, interactive=False)
            status_box_vc = gr.Textbox(label="Status", value="Ready to convert...", lines=3, interactive=False)
            audio_output_vc = gr.Audio(label="Converted Audio", autoplay=True, show_download_button=True)

    return {
        "input_audio": input_audio_vc,
        "target_voice_select": target_voice_select,
        "preview_audio": preview_audio_vc,
        "convert_btn": convert_btn,
        "progress_bar": progress_bar_vc,
        "status_box": status_box_vc,
        "audio_output": audio_output_vc
    }


def create_clone_voice_tab():
    """Create the UI for Clone Voice tab."""
    with gr.Row():
        with gr.Column():
            gr.Markdown("""
            ### Clone any voice instantly!
            
            **How to clone:**
            1. Upload or record a clear audio sample (5-30 seconds)
            2. Name your voice and select gender
            3. Select the language
            4. Click "Clone Voice"
            5. Use it in any tab!
            
            **Tips for best results:**
            - Use clear, high-quality audio
            - Avoid background noise
            - 10-20 seconds is ideal
            - Multiple sentences work better
            """)
            
            new_voice_name = gr.Textbox(
                label="Voice Name",
                placeholder="e.g., Amitabh, Priyanka, Morgan..."
            )
            
            voice_gender = gr.Radio(
                label="Gender",
                choices=[("Male ♂️", "male"), ("Female ♀️", "female")],
                value="male",
                info="Select the gender for display purposes"
            )
            
            voice_language = gr.Dropdown(
                label="Voice Language",
                choices=[(f"{name} ({code})", code) for code, name in sorted(SUPPORTED_LANGUAGES.items())],
                value="en",
                info="Select the language of the voice sample"
            )
            
            ref_audio_input = gr.Audio(
                label="Reference Audio Sample",
                sources=["upload", "microphone"],
                type="filepath"
            )
            clone_btn = gr.Button("🧬 Clone Voice", variant="primary", size="lg")
            
        with gr.Column():
            clone_status = gr.Textbox(label="Cloning Status", lines=3)
            gr.Markdown("""
            ### Your Cloned Voices:
            After cloning, your voice will appear in all tabs.
            
            **Voice Storage:**
            - Saved in `voice_samples` folder
            - Manage from this tab
            - Delete when no longer needed
            
            **Current Voices:**
            """)
            
            # Load current voices for initial display
            current_voices = load_voices()
            voices_display_text = "\n".join(current_voices) if current_voices else "No voices cloned yet"
            
            current_voices_display = gr.Textbox(
                value=voices_display_text,
                label="Cloned Voices",
                lines=5,
                interactive=False
            )
            
            with gr.Row():
                voice_to_delete = gr.Dropdown(
                    label="Select Voice to Delete",
                    choices=["None"] + current_voices,
                    value="None",
                    info="Select a cloned voice to delete"
                )
                delete_btn_clone = gr.Button("🗑️ Delete Voice", variant="secondary", size="sm")
            
            delete_status_clone = gr.Textbox(label="Delete Status", lines=2)

    return {
        "new_voice_name": new_voice_name,
        "voice_gender": voice_gender,
        "voice_language": voice_language,
        "ref_audio_input": ref_audio_input,
        "clone_btn": clone_btn,
        "clone_status": clone_status,
        "current_voices_display": current_voices_display,
        "voice_to_delete": voice_to_delete,
        "delete_btn": delete_btn_clone,
        "delete_status": delete_status_clone
    }
