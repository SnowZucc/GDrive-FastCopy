# GDrive-FastCopy
 
Small script for copying files faster to Google Drive (which limits copying to 3 files per second) by compressing large directories before sending them.
Requires a rclone mount to Google Drive.
Defaults to directories with a depth of 2 with > 50 files but you can change these settings.

This script handles files that have already been copied in a basic way using a log file.
Note: this script does not handle files modified since the copy. You will need to send everything.

## Requirements
### Windows
An rclone mount to Google Drive
Extract rclone release into the rclone directory