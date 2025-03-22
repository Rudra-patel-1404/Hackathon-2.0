# Resource Hub

A modern web application for sharing and discovering learning resources. Built with Flask and MongoDB.

## Features

- User authentication (login/register)
- Resource upload and download
- Subject-based resource organization
- Search functionality
- User profiles
- Modern, responsive UI with futuristic design

## Prerequisites

- Python 3.8 or higher
- MongoDB
- pip (Python package manager)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/resource-hub.git
cd resource-hub
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
Create a `.env` file in the root directory with the following content:
```
SECRET_KEY=your-secret-key
MONGO_URI=mongodb://localhost:27017/resource_hub
```

5. Initialize the database:
```bash
python init_db.py
```

## Running the Application

1. Start MongoDB:
```bash
mongod
```

2. Run the Flask application:
```bash
python run.py
```

3. Open your browser and navigate to:
```
http://localhost:5000
```

## Project Structure

```
resource-hub/
├── app/
│   ├── __init__.py
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   ├── auth.py
│   │   └── resources.py
│   └── templates/
│       ├── base.html
│       ├── index.html
│       ├── login.html
│       ├── register.html
│       ├── upload.html
│       ├── explore.html
│       ├── search.html
│       ├── profile.html
│       └── resource.html
├── uploads/
├── config.py
├── run.py
├── requirements.txt
└── README.md
```

## Contributing

1. Fork the repository
2. Create a new branch for your feature
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Flask web framework
- MongoDB database
- Bootstrap for the UI components
- Font Awesome for icons
- Google Fonts for typography 