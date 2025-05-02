import os
# Set the directory to look for kaggle.json
os.environ['KAGGLE_CONFIG_DIR'] = os.path.dirname(os.path.abspath(__file__))
import zipfile
from kaggle.api.kaggle_api_extended import KaggleApi


def unzip_all_in_folder(folder):
    """Recursively unzip all zip files in the folder."""
    for root, dirs, files in os.walk(folder):
        for file in files:
            if file.endswith(".zip"):
                zip_path = os.path.join(root, file)
                print(f"Extracting {zip_path}...")
                with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                    zip_ref.extractall(root)
                os.remove(zip_path)  # Optional: remove zip file after extraction

def download_home_depot_data(destination_folder="home_depot_data"):
    # Authenticate with the Kaggle API
    api = KaggleApi()
    api.authenticate()

    # Ensure destination directory exists
    os.makedirs(destination_folder, exist_ok=True)

    # Download the main ZIP file
    print("Downloading dataset...")
    api.competition_download_files('home-depot-product-search-relevance', path=destination_folder)
    print("Initial download complete.")

    # Extract top-level ZIP file
    top_zip = os.path.join(destination_folder, 'home-depot-product-search-relevance.zip')
    if os.path.exists(top_zip):
        print(f"Extracting top-level archive: {top_zip}")
        with zipfile.ZipFile(top_zip, 'r') as zip_ref:
            zip_ref.extractall(destination_folder)
        os.remove(top_zip)

    # Recursively unzip any remaining zip files
    print("Unzipping nested archives...")
    unzip_all_in_folder(destination_folder)
    print("All datasets unzipped.")

if __name__ == "__main__":
    download_home_depot_data()
