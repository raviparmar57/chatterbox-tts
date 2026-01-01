# Chatterbox TTS Models Information

## 📦 Model Source & Auto-Download

### **Where Models Come From**
All models are **automatically downloaded** from Hugging Face Hub when you first run the application.

**Repository:** `ResembleAI/chatterbox`  
**URL:** https://huggingface.co/ResembleAI/chatterbox

---

## 🤖 Models Used in Chatterbox TTS

This application uses **three main model types**, each with different capabilities:

### **1. ChatterboxTTS (English-Only Model)**
The standard English TTS model with voice cloning.

#### **Model Components:**
| Component | File | Size | Purpose |
|-----------|------|------|---------|
| **T3 (Text-to-Speech Tokens)** | `t3_cfg.safetensors` | ~500MB | Converts text to speech tokens |
| **S3Gen (Speech Generator)** | `s3gen.safetensors` | ~400MB | Generates audio from speech tokens |
| **Voice Encoder** | `ve.safetensors` | ~50MB | Extracts voice characteristics for cloning |
| **Tokenizer** | `tokenizer.json` | <1MB | Text tokenization |
| **Preset Voices** | `conds.pt` | ~10MB | Built-in voice presets |

**Total Size:** ~1GB

#### **Capabilities:**
- ✅ English text-to-speech
- ✅ Voice cloning from audio samples
- ✅ Emotion/exaggeration control
- ✅ Multiple built-in voices
- ❌ No multilingual support

---

### **2. ChatterboxMultilingualTTS (23 Languages)**
Extended model supporting multiple languages with voice cloning.

#### **Model Components:**
| Component | File | Size | Purpose |
|-----------|------|------|---------|
| **T3 Multilingual** | `t3_mtl23ls_v2.safetensors` | ~800MB | Multilingual text-to-speech tokens |
| **S3Gen** | `s3gen.pt` | ~400MB | Speech generator (shared) |
| **Voice Encoder** | `ve.pt` | ~50MB | Voice characteristics encoder |
| **MTL Tokenizer** | `grapheme_mtl_merged_expanded_v1.json` | ~5MB | Multilingual tokenizer |
| **Chinese Support** | `Cangjie5_TC.json` | ~2MB | Chinese character support |
| **Preset Voices** | `conds.pt` | ~10MB | Built-in voice presets |

**Total Size:** ~1.3GB

#### **Supported Languages (23):**
```
Arabic (ar)          Italian (it)       Swedish (sv)
Chinese (zh)         Japanese (ja)      Swahili (sw)
Danish (da)          Korean (ko)        Turkish (tr)
Dutch (nl)           Malay (ms)
English (en)         Norwegian (no)
Finnish (fi)         Polish (pl)
French (fr)          Portuguese (pt)
German (de)          Russian (ru)
Greek (el)           Spanish (es)
Hebrew (he)          
Hindi (hi)
```

#### **Capabilities:**
- ✅ 23 language support
- ✅ Voice cloning in any supported language
- ✅ Emotion/exaggeration control
- ✅ Cross-lingual voice transfer
- ✅ Built-in multilingual voices

---

### **3. ChatterboxVC (Voice Conversion)**
Voice conversion model - changes voice characteristics of existing audio.

#### **Model Components:**
| Component | File | Size | Purpose |
|-----------|------|------|---------|
| **S3Gen** | `s3gen.safetensors` | ~400MB | Speech generator for conversion |
| **Preset Voices** | `conds.pt` | ~10MB | Target voice presets |

**Total Size:** ~410MB

#### **Capabilities:**
- ✅ Convert any voice to target voice
- ✅ Maintain original content/language
- ✅ Real-time processing
- ❌ No text input (audio-to-audio only)

---

## 🔄 How Auto-Download Works

### **On First Run:**

When you start the application, it automatically:

1. **Checks Hugging Face Hub** for model files
2. **Downloads missing models** to cache directory
3. **Stores in local cache** (no re-download needed)
4. **Loads models** into memory

### **Cache Locations:**

Models are cached in:
- **Linux/Mac:** `~/.cache/huggingface/hub/`
- **Windows:** `C:\Users\<username>\.cache\huggingface\hub\`

### **Download Methods:**

#### **For Single Files (TTS & VC):**
```python
from huggingface_hub import hf_hub_download

hf_hub_download(
    repo_id="ResembleAI/chatterbox", 
    filename="t3_cfg.safetensors"
)
```

#### **For Multiple Files (Multilingual):**
```python
from huggingface_hub import snapshot_download

snapshot_download(
    repo_id="ResembleAI/chatterbox",
    allow_patterns=["ve.pt", "t3_mtl23ls_v2.safetensors", ...]
)
```

---

## 📊 Model Architecture Details

### **T3 (Text-to-Token Transformer)**
- **Architecture:** Transformer-based language model
- **Function:** Converts text → discrete speech tokens
- **Input:** Text (tokenized)
- **Output:** Speech tokens (acoustic representation)
- **Features:** 
  - Voice conditioning
  - Emotion control
  - CFG (Classifier-Free Guidance) support

### **S3Gen (Speech Token Generator)**
- **Architecture:** Neural vocoder with flow-matching
- **Function:** Converts speech tokens → audio waveform
- **Input:** Discrete speech tokens
- **Output:** 24kHz audio waveform
- **Features:**
  - High-quality audio synthesis
  - Voice embedding conditioning
  - Real-time capable

### **Voice Encoder**
- **Architecture:** Speaker embedding network
- **Function:** Extracts voice characteristics
- **Input:** Audio waveform (16kHz)
- **Output:** Speaker embedding vector
- **Features:**
  - Voice cloning support
  - Cross-lingual transfer

---

## 💾 Storage Requirements

### **For VPS Deployment:**

#### **Minimum Requirements:**
- **Disk Space:** 3GB free (for all models + cache)
- **RAM:** 4GB minimum (8GB recommended)
- **Download Time:** 10-20 minutes (depends on internet speed)

#### **Download Sizes:**
| Model Type | Download Size | Disk Space After |
|------------|---------------|------------------|
| English TTS | ~1GB | ~1GB |
| Multilingual TTS | ~1.3GB | ~1.3GB |
| Voice Conversion | ~410MB | ~410MB |
| **Total (All Models)** | **~2.7GB** | **~2.7GB** |

---

## 🚀 First-Time Setup Process

### **What Happens on First Deployment:**

1. **Install Dependencies** (`pip install -r requirements.txt`)
   - PyTorch: ~2GB download
   - Other packages: ~500MB

2. **Start Application** (`python app_production.py`)
   - Application starts
   - Models not found in cache

3. **Auto-Download Models** (happens automatically)
   ```
   🔄 Downloading models from Hugging Face...
   ⬇️  Downloading t3_cfg.safetensors... [500MB]
   ⬇️  Downloading s3gen.safetensors... [400MB]
   ⬇️  Downloading ve.safetensors... [50MB]
   ⬇️  Downloading tokenizer.json... [<1MB]
   ⬇️  Downloading conds.pt... [10MB]
   ✅ All models downloaded successfully!
   ```

4. **Load Models into Memory**
   ```
   🔄 Loading models...
   ✅ TTS model loaded
   ```

5. **Application Ready**
   ```
   Running on: http://0.0.0.0:7860
   ```

### **Subsequent Runs:**
- Models are **already cached** ✅
- No re-download needed ✅
- Faster startup time ✅

---

## 🔧 Manual Model Management

### **Pre-download Models (Optional)**

If you want to download models before running the app:

```python
from huggingface_hub import hf_hub_download, snapshot_download

# Download English TTS models
for file in ["ve.safetensors", "t3_cfg.safetensors", "s3gen.safetensors", "tokenizer.json", "conds.pt"]:
    hf_hub_download(repo_id="ResembleAI/chatterbox", filename=file)

# Download Multilingual models
snapshot_download(
    repo_id="ResembleAI/chatterbox",
    allow_patterns=["ve.pt", "t3_mtl23ls_v2.safetensors", "s3gen.pt", 
                    "grapheme_mtl_merged_expanded_v1.json", "conds.pt", "Cangjie5_TC.json"]
)
```

### **Check Cache Location**

```bash
# Linux/Mac
ls -lh ~/.cache/huggingface/hub/models--ResembleAI--chatterbox/

# Windows
dir C:\Users\<username>\.cache\huggingface\hub\models--ResembleAI--chatterbox\
```

### **Clear Cache (If Needed)**

```bash
# Linux/Mac
rm -rf ~/.cache/huggingface/hub/models--ResembleAI--chatterbox/

# Windows
rmdir /s C:\Users\<username>\.cache\huggingface\hub\models--ResembleAI--chatterbox\
```

---

## 🌐 Offline Deployment

If you need to deploy on a VPS **without internet access**:

1. **Download models on a machine with internet:**
   ```bash
   python -c "from huggingface_hub import snapshot_download; snapshot_download('ResembleAI/chatterbox')"
   ```

2. **Copy cache directory to VPS:**
   ```bash
   scp -r ~/.cache/huggingface/ user@vps-ip:~/.cache/
   ```

3. **Application will find models in cache** ✅

---

## 📝 Model Licensing

- **Model:** ResembleAI Chatterbox
- **License:** Check https://huggingface.co/ResembleAI/chatterbox for license details
- **Usage:** Follow ResembleAI's terms of service
- **Commercial Use:** Verify licensing terms before commercial deployment

---

## 🔍 Model Performance

### **Generation Speed (CPU):**
- **English TTS:** ~5-10 seconds per sentence
- **Multilingual TTS:** ~5-10 seconds per sentence
- **Voice Conversion:** ~2-5 seconds per audio clip

### **Generation Speed (GPU - CUDA):**
- **English TTS:** ~1-2 seconds per sentence
- **Multilingual TTS:** ~1-2 seconds per sentence
- **Voice Conversion:** <1 second per audio clip

### **Quality:**
- **Sample Rate:** 24kHz
- **Bit Depth:** 16-bit
- **Watermark:** Perth watermarking applied (for tracking)
- **Naturalness:** High-quality synthetic speech
- **Voice Similarity:** Good voice cloning accuracy

---

## ❓ FAQ

### **Q: Do I need a Hugging Face account?**
A: No, the models are publicly available and download automatically.

### **Q: Can I use custom/local models?**
A: Yes! Use `ChatterboxTTS.from_local(path, device)` instead of `from_pretrained()`.

### **Q: How much internet data will be used?**
A: ~2.7GB for all models on first run. No data usage after caching.

### **Q: Can I delete models I don't use?**
A: Yes, delete specific files from the cache directory. The app will re-download if needed.

### **Q: Does it work offline after first download?**
A: Yes! Once models are cached, no internet connection is needed.

### **Q: Can I use GPU acceleration?**
A: Yes! Set `DEVICE = "cuda"` in `modules/config.py` if you have a compatible NVIDIA GPU.

---

## 🎯 Summary

- ✅ **Automatic Download:** Models download automatically from Hugging Face
- ✅ **No Manual Setup:** Just run the app, everything is handled
- ✅ **Cached Locally:** No re-download after first run
- ✅ **3 Model Types:** English TTS, Multilingual TTS (23 languages), Voice Conversion
- ✅ **~3GB Total:** Reasonable size for VPS deployment
- ✅ **10-20 min First Run:** Initial download time (one-time only)

**Your VPS needs:**
- 3GB+ free disk space
- 4GB+ RAM
- Internet connection (first run only)
- No GPU required (but recommended for speed)
