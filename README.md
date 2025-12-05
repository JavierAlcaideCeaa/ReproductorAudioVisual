# Video Player Project

This project is a simple video player application built with Python. It provides a user-friendly interface for playing videos with basic controls.

## Project Structure

- **src/**: Contains the source code for the application.
  - **main.py**: Entry point of the application that initializes the video player and sets up the user interface.
  - **player.py**: Manages video playback functionality.
  - **ui.py**: Handles the user interface for video controls.
  - **components/**: Contains the main components of the video player.
    - **video_widget.py**: Responsible for displaying the video.
    - **controls.py**: Manages the playback controls.
  - **styles/**: Contains the stylesheet for the application.
    - **main.qss**: Styles defining the layout and appearance of the player.
  - **types.py**: Contains any necessary types or constants used throughout the application.
  
- **tests/**: Contains unit tests for the application.
  - **test_player.py**: Tests for the VideoPlayer class.
  
- **requirements.txt**: Lists the dependencies required for the project.
- **pyproject.toml**: Configuration file specifying build system requirements and project metadata.
- **.gitignore**: Specifies files and directories that should be ignored by version control.

## Features

- Play, pause, and stop video playback.
- Volume control and other user interface elements.
- Responsive design for various screen sizes.

## Getting Started

1. Clone the repository:
   ```
   git clone <repository-url>
   ```

2. Navigate to the project directory:
   ```
   cd video-player-python
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Run the application:
   ```
   python src/main.py
   ```

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

## License

This project is licensed under the MIT License.