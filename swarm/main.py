import time
import os
import sys

import cv2
import boto3
from botocore.exceptions import NoCredentialsError
from datetime import datetime
from decouple import config
from supabase import create_client
import marvin

try:
    from picamera2 import Picamera2, Preview
except ImportError:
    pass


class BeeMeasure:
    def __init__(self):
        self.timestamp = datetime.now()
        self.url = ""
        self.count = 0

    def __call__(self):
        """Call the pipeline in sequence"""
        # file_name = self.take_landingboard_photo()
        file_name = "experiment/bee-photos/bees-1721781121.jpg"
        file_name = self.process_bee_photo(file_name)
        self.url = self.upload_photo_to_s3(file_name)
        self.count = self.calculate_bee_density_marvin()
        self.store_bee_densities()
        self.check_swarm_event()

    def take_landingboard_photo(self):
        """
        Use the PiCamera2 module to take a picture of a Langstroth hive landing
        board
        """
        if sys.platform != "linux":
            print("This command is only available on Linux")
            return

        beecam = Picamera2()
        camera_config = beecam.create_preview_configuration()
        beecam.configure(camera_config)
        beecam.start_preview(Preview.NULL)
        beecam.start()
        time.sleep(2)

        # timestamp managed in class, but still using it for unique file name
        iso_datetime = self.timestamp.strftime("%Y-%m-%dT%H:%M:%S")
        file_name = f"bees-{iso_datetime}.jpg"

        beecam.capture_file(file_name)
        beecam.stop_preview()

        return file_name

    def process_bee_photo(self, file_name: str, x: int = 640, y: int = 480):
        """
        Pre-process the image specified by file_name using OpenCV
        This will include resizing the images to a standard view, converting it
        grayscale, and reducing blur

        TODO: test if this makes a difference for marvin ai? If not might skip
        """
        if not os.path.isfile(file_name):
            print(f"Error: The file {file_name} does not exist")
            return

        try:
            image = cv2.imread(file_name)
            if image is None:
                print(f"Error: the file {file_name} is not a valid image.")
                return

            std_width = x
            std_height = y
            resized_image = cv2.resize(image, (std_width, std_height))

        except Exception as e:
            print(f"An error occurred: {e}")

        try:
            gray_image = cv2.cvtColor(resized_image, cv2.COLOR_BGR2GRAY)

        except Exception as e:
            print(f"An error occurred during grayscale processing: {e}")

        # this overrides the original file (no need to backup?)
        file_name = file_name.replace(".jpg", "-gray.jpg")
        cv2.imwrite(file_name, gray_image)

        return file_name

    def upload_photo_to_s3(self, file_name: str, object_name: str = None) -> str:
        """
        Upload photo from process_bee_photo() and return S3 URL to file
        """
        print(f"Uploading {file_name} to S3...")

        access_key = config("ACCESS_KEY")
        secret_key = config("SECRET_KEY")
        aws_region = config("REGION")
        bucket = config("BUCKET")

        session = boto3.Session(
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
            region_name=aws_region,
        )

        s3_client = session.client("s3")

        # If S3 object_name was not specified, use file_name
        if object_name is None:
            object_name = os.path.basename(file_name)

        try:
            s3_client.upload_file(
                file_name, bucket, object_name, ExtraArgs={"ACL": "public-read"}
            )
            print(f"File {file_name} uploaded to {bucket}/{object_name}")
        except FileNotFoundError:
            print("The file was not found")
        except NoCredentialsError:
            print("Credentials not available")

        s3_file_link = f"https://{bucket}.s3.{aws_region}.amazonaws.com/{object_name}"
        print(s3_file_link)
        return s3_file_link

    def calculate_bee_density_marvin(self) -> int:
        img = marvin.Image(self.url)
        result = marvin.extract(
            img, target=int, instructions="count the number of bees in this picture"
        )
        return result[0]

    def store_bee_densities(self):
        """
        Store latest bee density from Marvin AI in Supabase cloud
        CREATE TABLE bee_density (
            id BIGINT GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
            timestamp TIMESTAMPTZ NOT NULL,
            url TEXT NOT NULL,
            count INTEGER NOT NULL
        );
        # TODO: add url column to db
        """
        supabase_url = config("SUPABASE_URL")
        supabase_key = config("SUPABASE_KEY")
        supabase_table_name = config("SUPABASE_TABLE_NAME")
        supabase = create_client(supabase_url, supabase_key)

        print("Loading bee density and time in supabase cloud database...")

        data = (
            supabase.table(supabase_table_name)
            .insert({"timestamp": str(self.timestamp), "url": self.url, "count": self.count})
            .execute()
        )
        return data

    def check_swarm_event(self, last_n_entries: int = 10) -> bool:
        # if event call _notify_swarm_event
        raise NotImplementedError(
            f"Checking if swarm event based on {last_n_entries} log entries..."
        )

    def _notify_swarm_event(self):
        raise NotImplementedError("Sending notification of swarm event...")
