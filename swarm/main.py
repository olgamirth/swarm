import typer
import cv2
import numpy as np
import os

app = typer.Typer()


@app.command()
def process_bee_photo(file_name: str):
    """
    Pre-process the image specified by file_name using OpenCV
    This will include resizing the images to a standard view, converting it
    grayscale, and reducing blur
    """
    if not os.path.isfile(file_name):
        typer.echo(f"Error: The file {file_name} does not exist")
        return

    try:
        # Read the image file"
        image = cv2.imread(file_name)
        if image is None:
            typer.echo(f"Error: the file {file_name} is not a valid image.")
            return

        # resize image to standard size
        std_width = x
        std_height = y
        resized_image = cv2.resize(image, (std_width, std_height))

        """
        Convert the images to grayscale to reduce computational complexity,
        since color information is not critical for this task. Grayscale images
        have only one channel instead of three (RGB), which will make the
        processing faster and potentially improving focus on shapes and
        patterns.
        """
        gray_image = cv2.cvtColor(resized_image, cv2.COLOR_BGR2GRAY)

    except Exception as e:
        typer.echo(f"An error occurred: {e}")


@app.command()
def upload_photo_to_s3(file_path: str):
    typer.echo(f"Uploading {file_path} to S3...")


@app.command()
def calculate_bee_density_marvin(remote_file_path: str):
    typer.echo(f"Calculating bee density for {remote_file_path} using Marvin AI...")


@app.command()
def calculate_bee_density_opencv(file_path: str):
    typer.echo(f"Calculating bee density for {file_path} using OpenCV...")


@app.command()
def check_swarm_event(last_n_entries: int = 10) -> bool:
    typer.echo(f"Checking if swarm event based on {last_n_entries} log entries...")
