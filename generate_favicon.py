#!/usr/bin/env python3
"""
Favicon generator for SecurePass Web App.
This script generates favicon files from SVG.
"""

import os
from pathlib import Path

def create_favicon_ico():
    """Create a favicon.ico file using PIL/Pillow"""
    try:
        from PIL import Image, ImageDraw
        
        # Create a 32x32 image with dark background
        size = (32, 32)
        image = Image.new('RGBA', size, (18, 18, 18, 255))  # Dark background (#121212)
        draw = ImageDraw.Draw(image)
        
        # Draw a lock shape in purple (#bb86fc)
        # Lock body (rectangle)
        draw.rectangle([8, 12, 24, 24], fill=(187, 134, 252, 255))
        # Lock shackle (top part)
        draw.rectangle([10, 6, 22, 12], fill=(187, 134, 252, 255))
        draw.ellipse([8, 6, 10, 8], fill=(187, 134, 252, 255))
        draw.ellipse([22, 6, 24, 8], fill=(187, 134, 252, 255))
        
        # Save as ICO
        favicon_path = Path('static/images/favicon.ico')
        favicon_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Create multiple sizes for ICO
        sizes = [16, 32, 48]
        images = []
        for s in sizes:
            resized = image.resize((s, s), Image.Resampling.LANCZOS)
            images.append(resized)
        
        images[0].save(
            favicon_path,
            format='ICO',
            sizes=[(size, size) for size in sizes]
        )
        
        print(f"High-quality favicon created successfully at {favicon_path}")
        print("The favicon includes multiple resolutions: 16x16, 32x32, and 48x48")
        return True
        
    except ImportError:
        print("Pillow is not installed. Creating a simple ICO file...")
        
        # Create a simple ICO file with basic hex data
        favicon_data = (
            b"\x00\x00\x01\x00\x01\x00\x20\x20\x10\x00\x00\x00\x00\x00\xa8\x00"
            b"\x00\x00\x16\x00\x00\x00\x28\x00\x00\x00\x20\x00\x00\x00\x40\x00"
            b"\x00\x00\x01\x00\x04\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
            b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
            b"\x00\x00\x00\x00\x00\x80\x00\x00\x80\x00\x00\x00\x80\x80\x00\x80"
            b"\x00\x00\x00\x80\x00\x80\x00\x80\x80\x00\x00\x80\x80\x80\x00\xc0"
            b"\xc0\xc0\x00\x00\x00\x80\x00\x00\x00\x80\x00\x00\x00\x80\x80\x00"
            b"\x00\x80\x00\x00\x00\x80\x00\x80\x00\x80\x80\x00\x00\x80\x80\x80"
            b"\x00\x00\x00\x00\x00\x00\x00\xff\x00\x00\x00\xff\x00\x00\x00\xff"
            b"\xff\x00\x00\x00\x00\x00\x00\x00\xff\x00\x00\x00\xff\x00\x00\x00"
            b"\xff\xff\x00\x00\x00\x00\x00\x00\x00\xff\xff\xff\x00\x00\x00\x00"
            b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
            b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
            b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
            b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
            b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
            b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
            b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
            b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
            b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
            b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
            b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
        )
        
        favicon_path = Path('static/images/favicon.ico')
        favicon_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(favicon_path, 'wb') as f:
            f.write(favicon_data)
            
        print(f"Simple favicon created at {favicon_path}")
        print("To create a higher quality favicon, install Pillow with: pip install Pillow")
        return True
    except Exception as e:
        print(f"Error creating favicon: {e}")
        return False

if __name__ == "__main__":
    create_favicon_ico()