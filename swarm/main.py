import typer

app = typer.Typer()


@app.command()
def take_bee_photo():
    typer.echo("Taking a bee photo...")


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
