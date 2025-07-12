import torch
from diffusers import StableDiffusionPipeline

print("Testing Stable Diffusion setup...")
print(f"PyTorch version: {torch.__version__}")
print(f"CUDA available: {torch.cuda.is_available()}")

# This will download the model on first run
try:
    pipe = StableDiffusionPipeline.from_pretrained("runwayml/stable-diffusion-v1-5")
    print("✓ Stable Diffusion loaded successfully!")
except Exception as e:
    print(f"✗ Error loading Stable Diffusion: {e}")