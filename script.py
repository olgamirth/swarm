from pathlib import Path

import cv2


def calculate_bee_density(image_path):
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    _, thresh = cv2.threshold(image, 127, 255, cv2.THRESH_BINARY_INV)
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    bee_density = len(contours)
    return bee_density


def main():
    for image_path in Path("bee-photos").glob("*.jpg"):
        bee_density = calculate_bee_density(image_path)
        print(f"{image_path.name}: {bee_density}")


if __name__ == "__main__":
    main()
