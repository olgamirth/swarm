import typer
import cv2
import numpy as np
import boto3
import time
import datetime
import os

from picamera2 import Picamera2, Preview
from botocore.exceptions import NoCredentialsError

app = typer.Typer()


def date_and_seconds_from_midnight() -> str:
    """
    This function will return a date and time string in the format of
    YYYYMMDD.sec where sec is the secods since midnight for the given day.
    """

    # Get the current datetime
    now = datetime.datetime.now()

    # Format the date part o the string to YYYYMMDD
    date_str = now.strftime('%Y%m%d')

    # Seconds since midnight
    midnight = datetime.datetime.combine(now.date(), datetime.time(0, 0))
    seconds_since_midnight = int((now - midnight).total_seconds())

    # Combine date and seconds in the required format
    result = f"{date_str}.{seconds_since_midnight}"

    return result


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

    file_name = f"bees-{date_and_seconds_from_midnight()}.jpg"
    beecam.capture_file(file_name)
    beecam.stop_preview()


@app.command()
def process_bee_photo(file_name: str, x: int, y: int):
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


@app.command()
def upload_photo_to_s3(file_path: str):
    typer.echo(f"Uploading {file_path} to S3...")
def upload_to_s3(file_name, bucket, object_name=None):
    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = file_name

    # Create an S3 client
    s3_client = boto3.client('s3')

    try:
        # Upload the file
        response = s3_client.upload_file(file_name, bucket, object_name)
        print(f"File {file_name} uploaded to {bucket}/{object_name}")
    except FileNotFoundError:
        print("The file was not found")
    except NoCredentialsError:
        print("Credentials not available")


@app.command()
def calculate_bee_density_marvin(remote_file_path: str):
    typer.echo(f"Calculating bee density for {remote_file_path} using Marvin AI...")


@app.command()
def calculate_bee_density_opencv(file_path: str):
    typer.echo(f"Calculating bee density for {file_path} using OpenCV...")


@app.command()
def check_swarm_event(last_n_entries: int = 10) -> bool:
    typer.echo(f"Checking if swarm event based on {last_n_entries} log entries...")
