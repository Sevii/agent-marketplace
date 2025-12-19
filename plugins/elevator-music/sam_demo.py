import torch
import torchaudio
from sam_audio import SAMAudio, SAMAudioProcessor

# Load model and processor
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = SAMAudio.from_pretrained("facebook/sam-audio-large").to(device).eval()
processor = SAMAudioProcessor.from_pretrained("facebook/sam-audio-large")

# Load audio file
audio_file = "path/to/audio.wav"

# Describe the sound you want to isolate
description = "A man speaking"

# Process and separate
inputs = processor(audios=[audio_file], descriptions=[description]).to(device)
with torch.inference_mode():
    result = model.separate(inputs, predict_spans=True)

# To further improve performance (at the expense of latency), you can add candidate re-ranking
with torch.inference_mode():
   outputs = model.separate(batch, predict_spans=True, reranking_candidates=8)

# Save results
torchaudio.save("target.wav", result.target[0].unsqueeze(0).cpu(), processor.audio_sampling_rate)
torchaudio.save("residual.wav", result.residual[0].unsqueeze(0).cpu(), processor.audio_sampling_rate)
