import os
import re
import requests


def download_image(url, output_dir):
    num_retries = 2
    for i in range(num_retries):
        try:
            response = requests.get(url)
            response.raise_for_status()
            image_name = os.path.basename(url)
            with open(os.path.join(output_dir, image_name), "wb") as f:
                f.write(response.content)
                print(f"Downloaded {image_name} to {output_dir}")
            break
        except (requests.exceptions.RequestException, IOError) as e:
            print(f"Failed to download {url} (attempt {i+1}/{num_retries})")
            if i == num_retries - 1:
                print(f"Gave up downloading {url}: {str(e)}")


def main(input_file):
    # Create output directory
    output_dir = "images"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Open input file
    with open(input_file, "r", encoding='utf-8') as f:
        lines = f.readlines()

    # Find all image URLs and download them
    img_urls = []
    for line in lines:
        matches = re.findall(r'<img\s.*?src="(.*?)".*?/>', line)
        for match in matches:
            img_urls.append(match)

    # Remove duplicates from the image URL list
    img_urls = list(set(img_urls))

    # Download all images
    for img_url in img_urls:
        download_image(img_url, output_dir)

    # Replace image URLs in input file
    output_lines = []
    for line in lines:
        replaced_urls = []  # List to store replaced URLs for the current line
        output_line = line  # Create a copy of the original line to modify
        for img_url in img_urls:
            if img_url not in replaced_urls:  # Check if URL already replaced
                output_line = output_line.replace(
                    img_url, f"{output_dir}/{os.path.basename(img_url)}")
                replaced_urls.append(img_url)  # Add URL to replaced list
        output_lines.append(output_line)

        # Clear replaced URLs list for the next line
        replaced_urls = []

    with open(f"output.txt", "w", encoding='utf-8') as f:
        for line in output_lines:
            f.write(line)


if __name__ == "__main__":
    input_file = "input.txt"
    main(input_file)
    print(f"ALL DONE!!!")
