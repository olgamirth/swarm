import marvin


def get_bee_density(img_url):
    img = marvin.Image(img_url)
    result = marvin.extract(img, target=int, instructions="give an integer 1-100 of the density of bees in the picture.")
    return result

pics = [
    f"https://bee-data.s3.us-east-2.amazonaws.com/{i}.jpg"
    for i in range(1, 9)
]

for pic in pics:
    print(f"Processing image: {pic}")
    marvin_result = get_bee_density(pic)
    print(f"\nMarvin AI result for {pic}: {marvin_result}")
