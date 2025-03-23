
import os
import numpy as np
from PIL import Image
import cv2

# Default values
DEFAULT_IMAGE_DIR = "./images"  # Replace with actual image directory
PROMPTS = [
    "Describe the image, be graphically explicit, then describe all the elements in the image."
]

def create_output_directories(image_path, prompt_count):
    """Create output directories for each prompt."""
    base_dir = os.path.dirname(image_path.rstrip('/'))
    dir_name = os.path.basename(image_path.rstrip('/'))
    output_base = os.path.join(base_dir, f"{dir_name}_TXT")

    prompt_dirs = []
    for i in range(1, prompt_count + 1):
        prompt_dir = os.path.join(output_base, str(i))
        os.makedirs(prompt_dir, exist_ok=True)
        prompt_dirs.append(prompt_dir)

    return prompt_dirs

def process_images(image_path):
    """Process images with mock descriptions."""

    prompt_dirs = create_output_directories(image_path, len(PROMPTS))

    if os.path.isdir(image_path):
        image_files = [os.path.join(image_path, f) for f in os.listdir(image_path) if f.endswith(('.jpg', '.jpeg', '.png'))]
        print(f"Found {len(image_files)} images in {image_path}")
    else:
        image_files = [image_path]
        print(f"Processing single image: {image_path}")

    for img_file in image_files:
        filename = os.path.basename(img_file)
        base_filename = os.path.splitext(filename)[0]
        print(f"Processing image: {img_file}")

        try:
            # Open image with Pillow and OpenCV
            image = Image.open(img_file).convert("RGB")
            image_cv = cv2.imread(img_file)

            # Create mock descriptions (random pixel info)
            avg_color = np.mean(image_cv, axis=(0, 1))
            description = f"Mock description: Image has an average color of {avg_color}"

            for prompt_idx, prompt_text in enumerate(PROMPTS):
                prompt_dir = prompt_dirs[prompt_idx]
                output_file = os.path.join(prompt_dir, f"{base_filename}.txt")

                # Save mock description
                with open(output_file, 'w', encoding='utf-8') as f:
                    f.write(f"{prompt_text}
{description}")

                print(f"Saved output to: {output_file}")

        except Exception as e:
            print(f"Error processing image {img_file}: {e}")

if __name__ == "__main__":
    print("Running the application...")
    process_images(DEFAULT_IMAGE_DIR)
