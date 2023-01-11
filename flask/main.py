#!/usr/bin/env python
import os

image_tag = 'spativis-converter'
os.system(f"docker run --detach --network=astronomy_default -v data:/data {image_tag}")