"""
Configuration file cho ứng dụng
"""
import os

# Pexels API credentials
PEXELS_API_KEY = os.getenv("PEXELS_API_KEY", "EY2W2pV8aA0CN0sJOrPfKOl6osKlxnWnp9gdHo1HfwnaKuELZJHP7BNm")

# Default fallback image
DEFAULT_BACKGROUND_IMAGE = "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=800&h=1200&fit=crop"

# Image dimensions
IMAGE_WIDTH = 1280
IMAGE_HEIGHT = 720

