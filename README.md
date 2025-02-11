# BgChanger

This web application allows users to upload an image, remove its background, and replace it with a new one. It's built using Flask for the backend and OpenCV for image processing.

## Features

- **Background Removal**: Remove the background from any uploaded image automatically.
- **Background Replacement**: Replace the removed background with a new image.
- **Easy-to-use Interface**: Clean and simple web interface for smooth user experience.
- **Download the Result**: After processing, users can download the final image.

## Technologies Used

- **Flask**: Web framework for backend.
- **Jinja2**: Template rendering engine for Flask.
- **rembg**: Library used for background removal.
- **OpenCV**: Image processing library used for background replacement.
- **NumPy**: Library used for array operations on image data.
- **ONNX Runtime**: Runtime for running the machine learning models used by `rembg`.

## Installation

### Clone the Repository

```bash
git clone https://github.com/your-username/background-remover-web.git
cd background-remover-web
```

### Create a Virtual Environment (optional but recommended)

```bash
python -m venv venv
```

### Activate the Virtual Environment

- **Windows**:
  ```bash
  venv\Scriptsctivate
  ```
- **MacOS/Linux**:
  ```bash
  source venv/bin/activate
  ```

### Install the Dependencies

```bash
pip install -r requirements.txt
```

## Usage

1. Run the Flask application:

```bash
python app.py
```

2. Visit `http://localhost:5000` in your web browser.
3. Upload an image and select the background you want to replace it with.
4. Download the processed image once the background has been removed and replaced.

## Contributing

Feel free to fork this repository, make changes, and create pull requests. Contributions are welcome!

## License

This project is licensed under the MIT License.
