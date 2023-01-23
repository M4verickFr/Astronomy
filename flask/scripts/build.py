import os
import time

image_tag = 'spativis-converter'
os.popen(f"docker build /converter/ -t {image_tag}:latest").read()

while True:
    if (int(os.popen(f"docker images | grep {image_tag} | wc -l").read()) == 1): break
    time.sleep(1)