from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import os

# Authenticate with Google
gauth = GoogleAuth()
gauth.LoadCredentialsFile("mycreds.txt")

if gauth.credentials is None:
    print("🔐 No credentials found. Opening Google authentication link...")
    gauth.CommandLineAuth()
elif gauth.access_token_expired:
    print("🔄 Token expired. Refreshing...")
    gauth.Refresh()
else:
    gauth.Authorize()

gauth.SaveCredentialsFile("mycreds.txt")
drive = GoogleDrive(gauth)

# Folder on your local PC
video_folder = os.path.join(os.getcwd(), "videos")
if not os.path.exists(video_folder):
    os.makedirs(video_folder)

# Create a test file
test_file_path = os.path.join(video_folder, "test_upload.txt")
with open(test_file_path, "w") as f:
    f.write("Test file uploaded from CCTV IntelliGuard")

# Google Drive folder ID (replace with your own)
folder_id = "1dDQVhGP191-cgVVfep99DoRllymQLqV4"  # 👈 your folder ID

# Upload to that folder
upload_file = drive.CreateFile({
    'title': 'test_upload.txt',
    'parents': [{'id': folder_id}]
})
upload_file.SetContentFile(test_file_path)
upload_file.Upload()

print("✅ Upload successful! File is inside your CCTV IntelliGuard folder.")
