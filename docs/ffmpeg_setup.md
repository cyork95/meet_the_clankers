# FFmpeg Setup Guide for Windows

FFmpeg is required for high-quality audio processing (stitching podcasts with silence).

## Option 1: Using Winget (Recommended)
The easiest way to install FFmpeg is using the Windows Package Manager (`winget`).

1. Open PowerShell as Administrator.
2. Run the following command:
   ```powershell
   winget install Gyan.FFmpeg
   ```
3. **Restart your terminal** (or VS Code) to refresh your PATH.

## Option 2: Manual Installation
1. Download the "git full" build from [gyan.dev](https://www.gyan.dev/ffmpeg/builds/).
2. Extract the ZIP file.
3. Move the folder to `C:\ffmpeg`.
4. Add `C:\ffmpeg\bin` to your System PATH environment variable.
   - Search "Edit the system environment variables" in Windows Start.
   - Click "Environment Variables".
   - Under "System variables", find "Path" and click "Edit".
   - Click "New" and add `C:\ffmpeg\bin`.
5. Restart your terminal.

## Verification
To verify installation, run:
```powershell
ffmpeg -version
```
