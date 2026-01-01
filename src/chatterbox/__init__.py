try:
    from importlib.metadata import version
    __version__ = version("chatterbox-tts")
except Exception:
    # Fallback if package not installed (running from source)
    __version__ = "1.0.0"


from .tts import ChatterboxTTS
from .vc import ChatterboxVC
from .mtl_tts import ChatterboxMultilingualTTS, SUPPORTED_LANGUAGES