from pathlib import Path

import fire
from climate_data_pipeline.main import ClimateDataPipeline


def main(config_file: str):
    """
    Execute the Climate Data Pipeline with the specified configuration file.

    Parameters
    ----------
    config_file : str
        Path to the configuration file required to run the pipeline.

    Raises
    ------
    RuntimeError
        If the specified configuration file does not exist.
    """
    # Ensure the configuration file exists
    if not Path(config_file).exists():
        raise RuntimeError(f"{config_file} does not exist.")


    # Initialize and run the ClimateDataPipeline
    ClimateDataPipeline(config_file).run()


if __name__ == "__main__":
    fire.Fire(main)
