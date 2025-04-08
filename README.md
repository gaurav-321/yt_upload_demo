# 📌 yt_upload_demo

YouTube Video Uploader with End Screen & Comment Automation

✨ **Description:**  
This project provides a Python script that automates the process of uploading videos to YouTube, adding an end screen, and posting comments. It includes error handling for retries and quota issues, making it a robust solution for content creators looking to streamline their video upload workflow.

🚀 **Features:**
- Video Upload
  - Resumable uploads with exponential backoff.
  - Error handling for HTTP errors and quota issues.
- End Screen Addition
  - Adds recommended videos to the end screen of uploaded videos.
- Comment Posting
  - Posts a comment on the uploaded video.
- Comprehensive Error Handling

🛠️ **Installation:**  
To set up and use this script, follow these steps:

1. Clone the repository:
   ```sh
   git clone https://github.com/gag3301v/yt_upload_demo.git
   cd yt_upload_demo
   ```

2. Install dependencies using pip:
   ```sh
   pip install --upgrade google-api-python-client
   ```

📦 **Usage:**  
Here’s an example of how to use the script:

```python
from new_uploader import Video

# Create an instance of the Video class with necessary details
video = Video(
    file_path="path/to/your_video.mp4",
    title="Your Video Title",
    description="Description of your video",
    category=22,  # Example category ID for 'Entertainment'
    tags=["tag1", "tag2"],
    privacy_status="public"
)

# Authenticate and upload the video
video.upload()
```

🔧 **Configuration:**  
Ensure you have a Google Cloud project configured with YouTube Data API enabled. You will need to set up OAuth 2.0 credentials and download the `client_secrets.json` file, which should be placed in the root directory of your project.

🧪 **Tests:**  
This project does not include automated tests at this time.

📁 **Project Structure:**
```
yt_upload_demo/
├── new_uploader.py
├── keywords.txt
└── README.md
```

🙌 **Contributing:**  
We welcome contributions! Please fork the repository, make your changes, and submit a pull request.

📄 **License:**  
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

Built with ❤️ by gag3301v