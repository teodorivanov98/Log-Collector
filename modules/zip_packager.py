import zipfile
import os

def zip_output_dir(output_dir):
    zip_filename = output_dir.rstrip('/') + ".zip"
    with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk(output_dir):
            for file in files:
                filepath = os.path.join(root, file)
                arcname = os.path.relpath(filepath, start=output_dir)
                zipf.write(filepath, arcname)
    return zip_filename