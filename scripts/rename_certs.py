import os

cert_dir = r"d:\Sankalpvasekar\assets\certificates"
for filename in os.listdir(cert_dir):
    if " " in filename:
        new_name = filename.replace(" ", "_")
        old_path = os.path.join(cert_dir, filename)
        new_path = os.path.join(cert_dir, new_name)
        os.rename(old_path, new_path)
        print(f"Renamed: {filename} -> {new_name}")
