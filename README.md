# Drone Lens

Drone Lens is a Django application for analyzing drone footage of aircraft. The application allows users to upload videos, trim them into segments, categorize them, and perform defect analysis.

## Features

### Video Management
- **Upload Videos**: Upload drone footage videos to the system
- **Video Trimming**: Trim videos into multiple segments with custom names
- **Video Categorization**: Organize video segments by categories
- **Video Download**: Download video segments directly from the analysis page

### Analysis
- **Defect Analysis**: Analyze video segments for defects
- **Categorized Analysis**: Filter and view analyses by category
- **Progress Tracking**: Track analysis progress for each defect
- **Auto-Save Results**: Analysis results are automatically saved and displayed in real-time

### Export
- **Export Results**: Export analysis results in various formats (PDF, CSV, JSON)
- **Print Reports**: Print analysis reports directly from the browser

## Installation

1. Clone the repository:
```
git clone https://github.com/yourusername/drone-lens.git
cd drone-lens
```

2. Install dependencies:
```
pip install -r requirements.txt
```

3. Install FFmpeg (required for video processing):
```
sudo apt-get update
sudo apt-get install ffmpeg
```

4. Run migrations:
```
python manage.py migrate
```

5. Start the development server:
```
python manage.py runserver
```

## Usage

### Video Upload and Trimming
1. Navigate to the "File" tab
2. Use the upload form to upload a video
3. Click on the "Trim" button for a video to access the trimming interface
4. Set start and end times for each segment
5. Name each segment and assign categories
6. Click "Add Segment" to add it to the list
7. Click "Process All Segments" to create the segments

### Video Analysis
1. Navigate to the "Analyze" tab
2. Use the category filter to find specific video segments
3. Click "Analyze" on a video segment
4. Fill in the analysis form with defect information
5. Save the analysis

### Export Results
1. Navigate to the "Analyze" tab
2. Click "Export Results"
3. Choose your preferred export format (PDF, CSV, JSON)
4. View the preview and print if needed

## Project Structure

- `core/` - Main application directory
  - `models.py` - Database models
  - `views.py` - View functions
  - `urls.py` - URL routing
  - `templates/` - HTML templates
  - `static/` - Static files (CSS, JS, images)
- `media/` - User-uploaded files
  - `videos/` - Original uploaded videos
  - `video_segments/` - Trimmed video segments
- `DroneLens/` - Project settings

## Dependencies

- Django
- FFmpeg
- MoviePy
- Django Crispy Forms

## License

This project is licensed under the MIT License - see the LICENSE file for details.
