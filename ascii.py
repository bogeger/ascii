from PIL import Image
import subprocess
import os

# wordz to be used
brush = "Filthy  "
ASPECT_RATIO = 2.09  # Terminal character height:width ratio

def image_to_ascii(path, target_width):
    # Get the base filename from the source image path
    base_name = os.path.basename(path)

    target_height = int(target_width / ASPECT_RATIO)
    print(f" Using width: {target_width}, height: {target_height} (aspect ratio {ASPECT_RATIO})")

    # Build output file name
    output_filename = f"{target_width}_ascii_output_{base_name}.txt"

    # Load and resize image
    img = Image.open(path).convert("RGBA")
    img = img.resize((target_width, target_height))

    pixels = img.getdata()
    width, height = img.size
    brush_index = 0
    result = []

    for y in range(height):
        row = ""
        for x in range(width):
            r, g, b, a = pixels[y * width + x]
            if a > 128 and (r + g + b) / 3 < 128:
                row += brush[brush_index]
                brush_index = (brush_index + 1) % len(brush)
            else:
                row += " "
        result.append(row)

    # Save to file
    with open(output_filename, "w") as f:
        f.write("\n".join(result))

    print(f"\n ASCII saved to {output_filename}\n")

    # Print the output using `cat`
    subprocess.run(["cat", output_filename])


if __name__ == "__main__":
    # Scan for PNG and JPG files
    supported_extensions = (".png", ".jpg", ".jpeg")
    files = sorted([f for f in os.listdir(".") if f.lower().endswith(supported_extensions)])

    if not files:
        print("No .png or .jpg files found in the current directory.")
        exit(1)

    print("\nAvailable images:")
    for i, file in enumerate(files, 1):
        print(f"  {i}) {file}")

    while True:
        try:
            choice_input = input(f"\nSelect an image [1-{len(files)}]: ").strip()
            choice_idx = int(choice_input) - 1
            if 0 <= choice_idx < len(files):
                selected_file = files[choice_idx]
                break
            else:
                print(f"Please enter a number between 1 and {len(files)}.")
        except ValueError:
            print("Invalid input. Please enter a number.")

    while True:
        user_input = input("Enter target width (default 192): ").strip()
        if not user_input:
            target_width = 192
            break
        try:
            target_width = int(user_input)
            if target_width <= 0:
                print("Please enter a positive number.")
                continue
            break
        except ValueError:
            print("Invalid input. Please enter a whole number.")

    image_to_ascii(selected_file, target_width)

