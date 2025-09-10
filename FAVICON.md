# Favicon for SecurePass

This document explains the favicon implementation for SecurePass and how to generate a higher quality version.

## Current Implementation

The application includes a basic favicon.ico file located at `static/images/favicon.ico`. This was generated with a simple script that creates a minimal ICO file.

## Better Quality Favicon

To generate a higher quality favicon with multiple resolutions:

1. Install Pillow:
   ```bash
   pip install Pillow
   ```

2. Run the favicon generator:
   ```bash
   python generate_favicon.py
   ```

This will create a new favicon.ico file with multiple resolutions (16x16, 32x32, 48x48) for better display on different devices.

## Favicon Design

The favicon features a lock icon in purple (#bb86fc) on a dark background (#121212), matching the application's color scheme. The lock represents security and password management, which are the core functions of SecurePass.

## Usage

The favicon is automatically included in all pages through the base template (`templates/base.html`). The template includes both SVG and ICO versions for maximum compatibility:

```html
<link rel="icon" type="image/svg+xml" href="{{ url_for('static', filename='images/favicon.svg') }}">
<link rel="icon" type="image/x-icon" href="{{ url_for('static', filename='images/favicon.ico') }}">
```

## Customization

To create a custom favicon:

1. Modify the SVG file at `static/images/favicon.svg`
2. Use an online converter or install Pillow to convert the SVG to ICO
3. Alternatively, create your own ICO file and replace `static/images/favicon.ico`

## Browser Compatibility

The implementation includes both SVG and ICO formats for maximum browser compatibility:
- Modern browsers will use the SVG version
- Older browsers will fall back to the ICO version