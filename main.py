import glob
import os
import typer
from pathlib import Path

# Before running do pip install "kiss-icp[all] from venv terminal

DataPath = Path('E:/Datasets/2011_09_30_drive_0028.bag')
ConfigPath = Path('./configs/config.yaml')
Topic = '/points_raw'

app = typer.Typer(add_completion=False, rich_markup_mode="rich")

@app.command()
def kiss_icp_pipeline():
    from kiss_icp.datasets import dataset_factory
    from kiss_icp.pipeline import OdometryPipeline

    OdometryPipeline(
        dataset=dataset_factory(
            dataloader="rosbag",
            data_dir=DataPath,
            topic=Topic,
        ),
        config=Path(ConfigPath),
        visualize=True,
    ).run().print()


def run():
    app()


if __name__ == "__main__":
    run()
