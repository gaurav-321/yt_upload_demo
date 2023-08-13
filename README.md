# YouTube Upload Script

![GitHub License](https://img.shields.io/badge/license-MIT-blue.svg)

This script automates the process of uploading videos to YouTube using the YouTube Data API. It allows you to specify the video file, title, description, tags, category, privacy settings, and more for your YouTube uploads.

Please note that you need to have a Google Cloud project set up with the YouTube Data API enabled and OAuth 2.0 credentials configured. Be cautious when using this script, and make sure you comply with YouTube's terms of use and community guidelines.

## Prerequisites

- Python 3.x
- Required Python packages: `httplib2`, `googleapiclient`, `oauth2client`

## Setup

1. Clone this repository to your local machine.

    ```bash
    git clone https://github.com/gaurav-321/youtube-upload-demo.git

2. Install Packages
   ```bash
   pip install httplib2 google-api-python-client oauth2client
3. Create a Google Cloud project and enable the YouTube Data API.

    Follow the instructions at Google Cloud Console to create a new project.
    Enable the YouTube Data API for your project.

    Create OAuth 2.0 credentials and download the client_secrets.json file.
    Configure the script:

4. Open the client_secrets.json file and fill in the necessary information.

5. Update the video file path, title, description, category, tags, privacy settings, and thumbnail URL in the script.

## Usage
    python new_uploader.py

The script will authenticate with your Google Cloud project and initiate the video upload process to your YouTube channel. It will display progress and status messages in the terminal.

## Disclaimer
This script is provided for educational and convenience purposes only. The author is not responsible for any misuse, violations, or issues arising from the use of this script. Use at your own risk and ensure compliance with YouTube's policies.

## License
This project is licensed under the MIT License - see the LICENSE file for details.