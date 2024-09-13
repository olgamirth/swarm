import typer

from .main import BeeMeasure

app = typer.Typer()
bee_measure = BeeMeasure()


@app.command()
def run_all():
    bee_measure.run_all()


@app.command()
def take_photo():
    file_name = bee_measure.take_landingboard_photo()
    typer.echo(f"Photo saved as {file_name}")


@app.command()
def process_photo(file_name: str):
    processed_file_name = bee_measure.process_bee_photo(file_name)
    typer.echo(f"Processed photo saved as {processed_file_name}")


@app.command()
def upload_photo(file_name: str):
    url = bee_measure.upload_photo_to_s3(file_name)
    typer.echo(f"Photo uploaded to {url}")


@app.command()
def calculate_bee_density(url: str):
    count = bee_measure.calculate_bee_density_marvin(url)
    typer.echo(f"Bee density count: {count}")


@app.command()
def store_bee_densities(url: str, count: int):
    bee_measure.store_bee_densities()
    typer.echo(f"Bee density count: {count}")


@app.command()
def check_swarm_event():
    result = bee_measure.check_swarm_event()
    typer.echo(f"Swarm event detection output: {result}")
