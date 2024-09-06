import typer
import cv2
import boto3
import time
import os

from picamera2 import Picamera2, Preview
from botocore.exceptions import NoCredentialsError
from datetime import datetime
from decouple import config

app = typer.Typer()


@app.command()
def take_landingboard_photo():
    """
    Use the PiCamera2 module to take a picture of a Langstroth hive landing
    board
    """

    beecam = Picamera2()
    camera_config = beecam.create_preview_configuration()
    beecam.configure(camera_config)
    beecam.start_preview(Preview.NULL)
    beecam.start()
    time.sleep(2)

    # It's much easier to determine when the image was taken when filename
    # is in the format bees-YYYYMMDD.sec.jpg
    now = datetime.now()
    iso_datetime = now.strftime("%Y-%m-%dT%H:%M:%S")
    file_name = f"bees-{iso_datetime}.jpg"

    beecam.capture_file(file_name)
    beecam.stop_preview()


@app.command()
def process_bee_photo(file_name: str, x: int = 640, y: int = 480):
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

    except Exception as e:
        typer.echo(f"An error occurred: {e}")

    # Convert image to grayscale
    try:
        gray_image = cv2.cvtColor(resized_image, cv2.COLOR_BGR2GRAY)

    except Exception as e:
        typer.echo(f"An error occurred during grayscale processing: {e}")

    return gray_image


@app.command()
def upload_photo_to_s3(file_name: str, object_name: str = None) -> str:
    """
    Upload photo from process_bee_photo() and return S3 URL to file
    """
    typer.echo(f"Uploading {file_name} to S3...")

    bucket = config('BUCKET')
    session = boto3.Session(
        aws_access_key_id=config('ACCESS_KEY'),
        aws_secret_access_key=config('SECRET_KEY'),
        region_name=config('REGION')
    )

    s3_client = session.client('s3')

    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = file_name

    try:
        # Upload the file
        response = s3_client.upload_file(file_name, bucket, object_name)
        print(f"File {file_name} uploaded to {bucket}/{object_name}")
    except FileNotFoundError:
        print("The file was not found")
    except NoCredentialsError:
        print("Credentials not available")

    return response


@app.command()
def calculate_bee_density_marvin(remote_file_path: str):
    typer.echo(f"Calculating bee density for {remote_file_path} using Marvin AI...")


@app.command()
def calculate_bee_density_opencv(file_path: str):
    typer.echo(f"Calculating bee density for {file_path} using OpenCV...")


@app.command()
def check_swarm_event(last_n_entries: int = 10) -> bool:
    typer.echo(f"Checking if swarm event based on {last_n_entries} log entries...")
