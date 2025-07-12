import streamlit as st
import requests
import io
from PIL import Image
import time

# Page configuration
st.set_page_config(
    page_title="AI Image Generator",
    page_icon="✨",
    layout="wide"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        text-align: center;
        padding: 2rem 0;
        background: linear-gradient(135deg, #1e3a8a 0%, #1e40af 50%, #1d4ed8 100%);
        color: white;
        margin: -1rem -1rem 2rem -1rem;
        border-radius: 0 0 20px 20px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    .stTextArea > div > div > textarea {
        height: 120px;
    }
    
    .generated-image {
        display: flex;
        justify-content: center;
        margin: 2rem 0;
    }
    
    .prompt-display {
        background-color: #f8fafc;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
        border-left: 4px solid #3b82f6;
        color: #1e293b;
    }
    
    .setup-instructions {
        background-color: #f1f5f9;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 4px solid #64748b;
        margin: 2rem 0;
        color: #334155;
    }
    
    .setup-instructions h3 {
        color: #1e293b;
        margin-bottom: 1rem;
    }
    
    .setup-instructions a {
        color: #3b82f6;
        text-decoration: none;
    }
    
    .setup-instructions a:hover {
        color: #1d4ed8;
        text-decoration: underline;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="main-header">
    <h1>✨ AI Image Generator</h1>
    <p>Transform your ideas into stunning images with Stable Diffusion</p>
</div>
""", unsafe_allow_html=True)

# Initialize session state
if 'generated_image' not in st.session_state:
    st.session_state.generated_image = None
if 'last_prompt' not in st.session_state:
    st.session_state.last_prompt = ""

# API Configuration
st.sidebar.header("⚙️ Configuration")
api_token = st.sidebar.text_input(
    "HuggingFace API Token",
    type="password",
    help="Get your token from https://huggingface.co/settings/tokens"
)

# Model selection
model_options = {
    "Stable Diffusion XL": "stabilityai/stable-diffusion-xl-base-1.0",
    "Stable Diffusion 2.1": "stabilityai/stable-diffusion-2-1",
    "Stable Diffusion 1.5": "runwayml/stable-diffusion-v1-5"
}

selected_model = st.sidebar.selectbox(
    "Select Model",
    options=list(model_options.keys()),
    help="Choose the Stable Diffusion model to use"
)

# Advanced parameters
st.sidebar.subheader("Advanced Settings")
guidance_scale = st.sidebar.slider("Guidance Scale", 1.0, 20.0, 7.5, 0.5)
num_inference_steps = st.sidebar.slider("Inference Steps", 10, 50, 30, 5)
width = st.sidebar.selectbox("Width", [512, 768, 1024], index=0)
height = st.sidebar.selectbox("Height", [512, 768, 1024], index=0)

# Main content
col1, col2 = st.columns([1, 1])

with col1:
    st.header("💭 Create Your Prompt")
    
    # Prompt input
    prompt = st.text_area(
        "Enter your prompt",
        placeholder="A majestic mountain landscape at sunset with vibrant colors...",
        height=120,
        help="Be descriptive for better results!"
    )
    
    # Example prompts
    st.subheader("Example Prompts")
    example_prompts = [
        "A cyberpunk city at night with neon lights",
        "A peaceful forest with morning sunlight filtering through trees",
        "A majestic dragon flying over a medieval castle",
        "A futuristic robot in a sci-fi laboratory",
        "A beautiful sunset over a calm ocean with sailboats"
    ]
    
    for i, example in enumerate(example_prompts):
        if st.button(f"📝 {example}", key=f"example_{i}"):
            st.session_state.prompt_input = example
            st.rerun()

def generate_image(prompt, api_token, model_name):
    """Generate image using HuggingFace API"""
    
    if not api_token:
        st.error("Please enter your HuggingFace API token in the sidebar")
        return None
    
    if not prompt.strip():
        st.error("Please enter a text prompt")
        return None
    
    # API endpoint
    api_url = f"https://api-inference.huggingface.co/models/{model_name}"
    
    headers = {
        "Authorization": f"Bearer {api_token}",
        "Content-Type": "application/json",
    }
    
    payload = {
        "inputs": prompt,
        "parameters": {
            "guidance_scale": guidance_scale,
            "num_inference_steps": num_inference_steps,
            "width": width,
            "height": height
        }
    }
    
    try:
        with st.spinner("🎨 Generating your image... This may take a few moments"):
            response = requests.post(api_url, headers=headers, json=payload)
            
            if response.status_code == 200:
                image = Image.open(io.BytesIO(response.content))
                return image
            elif response.status_code == 503:
                st.error("Model is loading, please wait a moment and try again.")
                return None
            else:
                st.error(f"Error: {response.status_code} - {response.text}")
                return None
                
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        return None

with col2:
    st.header("🎨 Generated Image")
    
    # Generate button
    if st.button("🚀 Generate Image", type="primary", use_container_width=True):
        if prompt:
            model_name = model_options[selected_model]
            generated_image = generate_image(prompt, api_token, model_name)
            
            if generated_image:
                st.session_state.generated_image = generated_image
                st.session_state.last_prompt = prompt
                st.success("Image generated successfully!")
    
    # Display generated image
    if st.session_state.generated_image:
        st.markdown('<div class="generated-image">', unsafe_allow_html=True)
        st.image(st.session_state.generated_image, caption="Generated Image", use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Download button
        img_buffer = io.BytesIO()
        st.session_state.generated_image.save(img_buffer, format="PNG")
        img_buffer.seek(0)
        
        st.download_button(
            label="📥 Download Image",
            data=img_buffer,
            file_name=f"stable_diffusion_{int(time.time())}.png",
            mime="image/png",
            use_container_width=True
        )
        
        # Display prompt used
        if st.session_state.last_prompt:
            st.markdown(f"""
            <div class="prompt-display">
                <strong>Prompt used:</strong> {st.session_state.last_prompt}
            </div>
            """, unsafe_allow_html=True)

# Setup Instructions
st.markdown("""
<div class="setup-instructions">
    <h3>🔧 Setup Instructions</h3>
    <ol>
        <li>Get a free HuggingFace API token from <a href="https://huggingface.co/settings/tokens" target="_blank">here</a></li>
        <li>Enter your token in the sidebar configuration</li>
        <li>The first generation might take longer as the model loads</li>
        <li>Try descriptive prompts for better results</li>
        <li>Adjust advanced settings in the sidebar to fine-tune your results</li>
    </ol>
</div>
""", unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #666;'>Made with ❤️ using Streamlit and HuggingFace</div>",
    unsafe_allow_html=True
)