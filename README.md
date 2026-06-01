# Push Your Limits

A lightweight Flask website for medical students to upload study files, extract images, and generate quiz practice.

## Features

- Quiet, study-friendly UI
- Sections for files, videos, and quizzes
- Editor login required to upload or hide content
- Request access form sends a notification email to `luffy5656taro@gmail.com`
- Interactive quizzes with instant feedback and scoring

## Setup

1. Create a Python virtual environment.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Copy `.env.example` to `.env` and set `SECRET_KEY`.
4. Optional: configure SMTP variables to send access request emails.

Dependencies include `python-pptx` so PowerPoint uploads can be parsed automatically.

## Run

```bash
export FLASK_APP=app.py
export FLASK_ENV=development
flask run --host=0.0.0.0
```

Then open `http://localhost:5000`.

## Default editor account

- Username: `admin`
- Password: `study2026`

## Notes

- Uploaded files are stored in `/uploads`.
- Extracted images are stored in `/uploads/images`.
- Content and user accounts are stored in `/data`.
