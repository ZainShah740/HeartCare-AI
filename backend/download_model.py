"""
Script to download the trained model from Hugging Face Hub
Run this once before starting the backend server
"""

from huggingface_hub import hf_hub_download
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def download_model():
    """Download model from Hugging Face Hub to backend directory"""
    try:
        logger.info("Downloading model from Hugging Face Hub...")
        
        # Download to current directory
        model_path = hf_hub_download(
            repo_id="ZainShahHere/cardiac_arrest_model",
            filename="cardiac_arrest_model.pkl",
            local_dir=Path(__file__).parent,
            local_dir_use_symlinks=False
        )
        
        logger.info(f"✅ Model downloaded successfully to: {model_path}")
        return model_path
        
    except Exception as e:
        logger.error(f"❌ Failed to download model: {str(e)}")
        logger.error("Please check:")
        logger.error("  1. Hugging Face Hub repository exists")
        logger.error("  2. Model file is named correctly")
        logger.error("  3. You have internet connection")
        raise


if __name__ == "__main__":
    download_model()
