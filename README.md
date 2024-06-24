# Reverse Image Scraping

## Overview

This repository contains scripts to perform reverse image searches and download similar images from the web using Yandex's image search functionality. These scripts can be useful for dataset augmentation or finding additional data for machine learning models.

## Scripts

### 1. `single_img_scrap.py`
Performs a reverse image search for a single image and downloads a specified number of similar images.

### 2. `random_nth_scrap.py`
Randomly selects every nth image from a folder, performs a reverse image search, and downloads similar images.

### 3. `folder_scrap.py`
Performs a reverse image search for all images in a given folder and downloads a specified number of similar images for each.

## Requirements

Install the necessary dependencies using the provided `requirements.txt` file.

```bash
pip install requirements.txt
```

## Usage Warning

- **Disclaimer**: Use these scripts at your own risk. Setting `verify=False` in requests may lead to security issues. It is recommended to set `verify=True` for secure connections .Sometimes it wont work if verify = true
- **Ethical Use**: Usea at your won risk .Ensure legal image use and website terms compliance.
