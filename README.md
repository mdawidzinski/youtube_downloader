# YouTube Downloader

This is a YouTube Downloader program written in Python that allows users to download audio and video files in MP3 and MP4 formats, as well as download specific segments of video files. The program follows the MVC (Model-View-Controller) architectural pattern.

## Features

    Download audio and video files from YouTube.
    Save files in MP3 and MP4 formats.
    Download specific segments of video files.
    Choose the destination path for saving the downloaded files.
    Save the selected path in JSON format for future use.
    Utilizes the following libraries:
        pytube: For downloading YouTube files.
        ffmpeg: For trimming video files.
        tkinter: For the graphical user interface (GUI).
        
 ## Installation 
    pip install -r requirements.txt

## Usage

    Launch the program by running main.py.
    Enter the URL of the YouTube video you want to download.
    Select the desired audio or video format (MP3 or MP4).
    If you want to download a specific segment of the video, enter the start and end time in seconds.    
    Click the "Download" button to start the download process.
    Wait for the download to complete.
    You can always change the default saving path in the menu. The program will remember your selection 
    for future use.
    
    
  ## Known Issues

    One drawback of the program is that it first downloads the entire video file and then trims it locally. 
    This can be time-consuming, especially for large video files. Consider the duration of the video before 
    downloading and trimming a specific segment.
    
    
## Legal Compliance

    This program is intended for personal use only and should be used in accordance with YouTube's 
    terms of service and the applicable copyright laws. Please note the following:

    Respect copyright: Ensure that you have the necessary rights or permissions to download and use 
    the content you access through this program. Do not infringe on the intellectual property rights of others.

    Personal use: This program is intended for personal, non-commercial use. Do not use it to download 
    or distribute content in violation of YouTube's terms of service or any applicable laws.

    Usage responsibility: The user of this program is solely responsible for any actions they perform, 
    including the downloading and usage of content. The developer of this program is not liable for any 
    misuse or copyright infringement.
   
    
## License

     This project is licensed under the MIT License.     
