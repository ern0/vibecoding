#!/usr/bin/env python3
"""
Convert all images in a directory to data URIs and generate JavaScript code.
"""

import os
import base64
import mimetypes
from pathlib import Path

def get_mime_type(file_path):
    """Get MIME type for an image file."""
    mime_type, _ = mimetypes.guess_type(file_path)
    if mime_type is None:
        # Fallback for common image types
        ext = file_path.lower().split('.')[-1]
        mime_types = {
            'jpg': 'image/jpeg',
            'jpeg': 'image/jpeg',
            'png': 'image/png',
            'gif': 'image/gif',
            'svg': 'image/svg+xml',
            'webp': 'image/webp',
            'bmp': 'image/bmp',
            'ico': 'image/x-icon'
        }
        mime_type = mime_types.get(ext, 'application/octet-stream')
    return mime_type

def image_to_data_uri(image_path):
    """Convert an image file to a data URI."""
    mime_type = get_mime_type(image_path)
    
    with open(image_path, 'rb') as f:
        image_data = f.read()
    
    base64_data = base64.b64encode(image_data).decode('utf-8')
    data_uri = f'data:{mime_type};base64,{base64_data}'
    
    return data_uri

def convert_directory_to_js(directory_path, output_file='images.js', sort_images=True):
    """
    Convert all images in a directory to data URIs and generate JavaScript code.
    
    Args:
        directory_path: Path to the directory containing images
        output_file: Output file name for the JavaScript code
        sort_images: Sort images alphabetically by filename
    """
    # Supported image extensions
    image_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.svg', '.webp', '.bmp', '.ico'}
    
    # Get all image files from directory
    image_files = []
    for file in os.listdir(directory_path):
        file_path = os.path.join(directory_path, file)
        if os.path.isfile(file_path):
            ext = os.path.splitext(file)[1].lower()
            if ext in image_extensions:
                image_files.append((file, file_path))
    
    if not image_files:
        print(f"No images found in directory: {directory_path}")
        return
    
    # Sort if requested
    if sort_images:
        image_files.sort(key=lambda x: x[0])
    
    print(f"Found {len(image_files)} images:")
    for filename, _ in image_files:
        print(f"  - {filename}")
    
    # Generate JavaScript code
    js_lines = ["        const images = ["]
    
    for i, (filename, filepath) in enumerate(image_files, 1):
        print(f"Processing {i}/{len(image_files)}: {filename}...")
        
        try:
            data_uri = image_to_data_uri(filepath)
            
            # Add comment with filename
            js_lines.append(f"            // Image {i}: {filename}")
            js_lines.append(f"            '{data_uri}',")
            js_lines.append("")
        except Exception as e:
            print(f"  Error processing {filename}: {e}")
            continue
    
    # Remove last empty line and comma
    if js_lines[-1] == "":
        js_lines.pop()
    if js_lines[-1].endswith(','):
        js_lines[-1] = js_lines[-1][:-1]
    
    js_lines.append("        ];")
    
    # Write to file
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(js_lines))
    
    print(f"\n✓ JavaScript code written to: {output_file}")
    print(f"✓ Total images converted: {len(image_files)}")
    print(f"\nYou can now copy the contents of '{output_file}' and replace the 'const images = [...]' section in your HTML file.")

def main():
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Convert images in a directory to data URIs for JavaScript',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python convert_images.py ./images
  python convert_images.py ./photos -o carousel_images.js
  python convert_images.py ./pics --no-sort
        """
    )
    
    parser.add_argument(
        'directory',
        help='Directory containing images to convert'
    )
    
    parser.add_argument(
        '-o', '--output',
        default='images.js',
        help='Output JavaScript file (default: images.js)'
    )
    
    parser.add_argument(
        '--no-sort',
        action='store_true',
        help='Do not sort images alphabetically'
    )
    
    args = parser.parse_args()
    
    # Validate directory
    if not os.path.isdir(args.directory):
        print(f"Error: '{args.directory}' is not a valid directory")
        return 1
    
    # Convert images
    convert_directory_to_js(
        args.directory,
        args.output,
        sort_images=not args.no_sort
    )
    
    return 0

if __name__ == '__main__':
    exit(main())
