from pydantic import BaseModel

import marvin


class BeeDensity(BaseModel):
    density: int
    estimate_number_of_bees: int


bee_pictures = [
    f"https://bee-data.s3.us-east-2.amazonaws.com/{i}.jpg" for i in range(1, 9)
]


for picture in bee_pictures:
    img = marvin.Image(picture)
    result = marvin.cast(
        img,
        target=BeeDensity,
        instructions="Make an estimate of the number of bees in this photo and the density of bees around the hive",
    )
    print(
        f"{picture} -> {result.estimate_number_of_bees} bees with a density of {result.density}"
    )
