# Development Guide

## Linting
To run pylint on the source code:

```bash
python -m pylint src/main.py src/news_fetcher.py src/script_generator.py src/audio_generator.py src/podcast_producer.py
```

## Testing
To run unit tests:


## Debugging (VS Code)
We have included a `.vscode/launch.json` file to make debugging easy.

1. Go to the **Run and Debug** view in VS Code (Ctrl+Shift+D).
2. Select a configuration:
    - **Python: Daily Podcast**: Runs the app in daily mode.
    - **Python: Weekly Podcast**: Runs the app in weekly mode.
    - **Python: Debug Tests**: Debugs the currently open test file.
3. Set breakpoints in your code (click to the left of the line number).
4. Press **F5** to start debugging.
