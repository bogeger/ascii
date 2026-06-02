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

    image_to_ascii("filthy.png", target_width)

