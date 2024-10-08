from pathlib import Path
import pandas as pd
import typer
from loguru import logger
from VitalMetrics.config import RAW_DATA_DIR, PROCESSED_DATA_DIR
from VitalMetrics.features import feature_engineering


app = typer.Typer()


@app.command()
def main(
    # Paths for input and output files
    train_input_path: Path = RAW_DATA_DIR / "palmer-penguins-dataset-for-eda/penguins_train.csv",
    test_input_path: Path = RAW_DATA_DIR / "palmer-penguins-dataset-for-eda/penguins_test.csv",
    train_output_path: Path = PROCESSED_DATA_DIR / "penguin_train_features.csv",
    test_output_path: Path = PROCESSED_DATA_DIR / "penguin_test_features.csv",
):
    """Function to load dataset, split into train/test, generate features, and save to output files."""

    # Load dataset
    logger.info(f"Loading dataset from {train_input_path} and {test_input_path}...")
    try:
        train_df = pd.read_csv(train_input_path)
        test_df = pd.read_csv(test_input_path)
        logger.success("Datasets loaded successfully.")
    except Exception as e:
        logger.error(f"Failed to load dataset: {e}")
        return

    logger.info(f"Train set: {len(train_df)} samples, Test set: {len(test_df)} samples.")

    # Feature engineering (encoding and scaling)
    train_df = feature_engineering(train_df)
    test_df = feature_engineering(test_df)

    # Save the transformed features
    logger.info(f"Saving processed training features to {train_output_path}...")
    try:
        train_df.to_csv(train_output_path, index=False)
        logger.success("Training features saved successfully.")
    except Exception as e:
        logger.error(f"Failed to save training features: {e}")

    logger.info(f"Saving processed test features to {test_output_path}...")
    try:
        test_df.to_csv(test_output_path, index=False)
        logger.success("Test features saved successfully.")
    except Exception as e:
        logger.error(f"Failed to save test features: {e}")
