"""
Chatterbox TTS Enhanced - Production Deployment
"""
import sys
import os

# Project root for relative paths
project_root = os.path.dirname(os.path.abspath(__file__))
if project_root not in sys.path:
    sys.path.append(project_root)

import gradio as gr
from modules.config import LANGUAGE_CONFIG, SUPPORTED_LANGUAGES
from modules.voice_manager import (
    load_voices, 
    get_voices_for_language, 
    get_all_voices_with_gender,
    resolve_voice_path,
    clone_voice,
    delete_voice
)
from modules.generation_functions import (
    generate_speech,
    generate_multilingual_speech,
    convert_voice
)

# Import UI components
from modules.ui_components import (
    create_header,
    create_tts_tab,
    create_multilingual_tab,
    create_voice_conversion_tab,
    create_clone_voice_tab
)

# Load voices at startup
available_voices = load_voices()

# ---------------------------
# Main Application
# ---------------------------
with gr.Blocks(title="Chatterbox TTS Enhanced", theme=gr.themes.Soft()) as demo:
    # State variables
    tts_model_state = gr.State(None)
    vc_model_state = gr.State(None)
    mtl_model_state = gr.State(None)
    
    # Header
    create_header()
    
    # Create tabs
    with gr.Tab("🎤 Text-to-Speech"):
        tts_components = create_tts_tab()
    
    with gr.Tab("🌍 Multilingual TTS"):
        mtl_components = create_multilingual_tab()
    
    with gr.Tab("🔄 Voice Conversion"):
        vc_components = create_voice_conversion_tab()
    
    with gr.Tab("🧬 Clone Voice"):
        clone_components = create_clone_voice_tab()
    
    # ---------------------------
    # Event Handlers - TTS Tab
    # ---------------------------
    tts_components['generate_btn'].click(
        fn=generate_speech,
        inputs=[
            tts_components['text'],
            tts_components['voice_select'],
            tts_components['exaggeration'],
            tts_components['temp'],
            tts_components['seed_num'],
            tts_components['cfg_weight'],
            tts_components['min_p'],
            tts_components['top_p'],
            tts_components['repetition_penalty']
        ],
        outputs=[
            tts_components['progress_bar'],
            tts_components['audio_output'],
            tts_components['status_box']
        ]
    )
    
    # Update preview when voice changes
    def update_tts_preview(voice_name):
        path = resolve_voice_path(voice_name, "en")
        return path

    tts_components['voice_select'].change(
        fn=update_tts_preview,
        inputs=[tts_components['voice_select']],
        outputs=[tts_components['preview_audio']]
    )
    
    # ---------------------------
    # Event Handlers - Multilingual Tab
    # ---------------------------
    mtl_components['generate_btn'].click(
        fn=generate_multilingual_speech,
        inputs=[
            mtl_components['text'],
            mtl_components['voice_select'],
            mtl_components['language_select'],
            mtl_components['exaggeration'],
            mtl_components['temp'],
            mtl_components['seed_num'],
            mtl_components['cfg_weight']
        ],
        outputs=[
            mtl_components['progress_bar'],
            mtl_components['audio_output'],
            mtl_components['status_box']
        ]
    )
    
    # Update language change
    mtl_components['language_select'].change(
        fn=lambda lang: (
            LANGUAGE_CONFIG.get(lang, {}).get("text", ""),
            gr.update(choices=get_voices_for_language(lang), value=f"Default ({SUPPORTED_LANGUAGES.get(lang, lang)})")
        ),
        inputs=[mtl_components['language_select']],
        outputs=[mtl_components['text'], mtl_components['voice_select']]
    )
    
    # Update preview when voice changes (Multilingual)
    def update_mtl_preview(voice_name, language_code):
        path = resolve_voice_path(voice_name, language_code)
        return path

    mtl_components['voice_select'].change(
        fn=update_mtl_preview,
        inputs=[mtl_components['voice_select'], mtl_components['language_select']],
        outputs=[mtl_components['sample_audio']]
    )
    
    # ---------------------------
    # Event Handlers - Voice Conversion Tab
    # ---------------------------
    vc_components['convert_btn'].click(
        fn=convert_voice,
        inputs=[vc_components['input_audio'], vc_components['target_voice_select']],
        outputs=[vc_components['progress_bar'], vc_components['audio_output'], vc_components['status_box']]
    )
    
    # Update preview when voice changes (VC)
    def update_vc_preview(voice_name):
        if voice_name == "None": 
            return None
        
        # Remove gender symbols if present
        clean_name = voice_name.replace(" ♂️", "").replace(" ♀️", "")
        
        # Check if it's a default voice string like "Default (English)"
        if clean_name.startswith("Default ("):
            # Extract language name
            lang_name = clean_name.split("(")[1].split(")")[0]
            # Find code
            for code, name in SUPPORTED_LANGUAGES.items():
                if name == lang_name:
                    return LANGUAGE_CONFIG.get(code, {}).get("audio")
        
        # Try different possible names with gender suffixes
        from modules.voice_manager import VOICES
        possible_names = [
            clean_name,
            f"{clean_name}_male",
            f"{clean_name}_female"
        ]
        
        # Check cloned voices
        for name in possible_names:
            if name in VOICES["samples"]:
                return VOICES["samples"][name]
        
        # Try finding it with language suffixes if not found directly
        for code in SUPPORTED_LANGUAGES:
            for name in possible_names:
                full_name = f"{name}_{code}"
                if full_name in VOICES["samples"]:
                    return VOICES["samples"][full_name]
        
        return None

    vc_components['target_voice_select'].change(
        fn=update_vc_preview,
        inputs=[vc_components['target_voice_select']],
        outputs=[vc_components['preview_audio']]
    )
    
    # ---------------------------
    # Event Handlers - Clone Voice Tab
    # ---------------------------
    # Update all voice dropdowns when cloning
    clone_components['clone_btn'].click(
        fn=clone_voice,
        inputs=[
            clone_components['ref_audio_input'],
            clone_components['new_voice_name'],
            clone_components['voice_language'],
            clone_components['voice_gender']
        ],
        outputs=[clone_components['clone_status'], tts_components['voice_select']]
    ).then(
        fn=lambda: gr.update(choices=get_voices_for_language("en")),
        outputs=[tts_components['voice_select']]
    ).then(
        fn=lambda lang: gr.update(choices=get_voices_for_language(lang)),
        inputs=[mtl_components['language_select']],
        outputs=[mtl_components['voice_select']]
    ).then(
        fn=lambda: gr.update(choices=["None"] + get_all_voices_with_gender()),
        outputs=[vc_components['target_voice_select']]
    ).then(
        fn=lambda: "\n".join(load_voices()) if load_voices() else "No voices cloned yet",
        outputs=[clone_components['current_voices_display']]
    ).then(
        fn=lambda: gr.update(choices=["None"] + get_all_voices_with_gender(), value="None"),
        outputs=[clone_components['voice_to_delete']]
    )
    
    # Delete voice functionality in Clone Voice tab
    clone_components['delete_btn'].click(
        fn=delete_voice,
        inputs=[clone_components['voice_to_delete']],
        outputs=[clone_components['delete_status'], clone_components['voice_to_delete']]
    ).then(
        fn=lambda: gr.update(choices=get_voices_for_language("en")),
        outputs=[tts_components['voice_select']]
    ).then(
        fn=lambda lang: gr.update(choices=get_voices_for_language(lang)),
        inputs=[mtl_components['language_select']],
        outputs=[mtl_components['voice_select']]
    ).then(
        fn=lambda: gr.update(choices=["None"] + get_all_voices_with_gender()),
        outputs=[vc_components['target_voice_select']]
    ).then(
        fn=lambda: "\n".join(load_voices()) if load_voices() else "No voices cloned yet",
        outputs=[clone_components['current_voices_display']]
    )


if __name__ == "__main__":
    # Production configuration with environment variable support
    PORT = int(os.getenv("GRADIO_SERVER_PORT", "7860"))
    HOST = os.getenv("GRADIO_SERVER_NAME", "0.0.0.0")
    
    demo.queue(
        max_size=50,
        default_concurrency_limit=3,  # Adjust based on your server capacity
    ).launch(
        server_name=HOST,  # Listen on all interfaces
        server_port=PORT,  # Use environment variable or default
        share=False,  # Disable public sharing
        show_error=True,
        # Uncomment to add authentication:
        # auth=("admin", "your_secure_password"),
        # For API access:
        show_api=True,  # Enable API documentation
    )
