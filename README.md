# Weather Microservice Project

## Overview

This project is a full-stack weather microservice application built with a Flask backend and React frontend. It uses the OpenWeatherMap One Call API 3.0 to provide current weather data and a 7-day forecast based on a city name input.

---

## Features Implemented

- **Flask Backend**  
  - Organized backend code inside a dedicated `backend/` folder for clear separation.  
  - Implemented `/weather` endpoint to fetch current weather using One Call API 3.0.  
  - Added `/forecast` endpoint for 7-day weather forecasts utilizing the same API.  
  - Robust error handling and validation for API requests.  
  - File-based logging with rotating log files (`app.log`) capturing all requests and errors for maintainability and debugging.

- **React Frontend**  
  - Created a React app inside `frontend/` folder using Create React App.  
  - Axios-based API calls to backend endpoints.  
  - User interface allows searching for a city’s current weather and 7-day forecast.  
  - Loading state and error handling to enhance user experience.

- **Project Structure**  
  - Separate folders for backend (`backend/`) and frontend (`frontend/`) codebases.  
  - Backend dependencies managed with `requirements.txt`.  
  - Frontend dependencies managed with `package.json` and Node.js/npm.

---

## Setup Instructions

### Backend

1. Navigate to the backend folder:
   ```
   cd backend
   ```

2. Create and activate a virtual environment:
   ```
   python3 -m venv venv
   source venv/bin/activate     # For macOS/Linux
   venv\Scripts\activate        # For Windows
   ```

3. Install Python dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Set up your `.env` file with your OpenWeatherMap API key:
   ```
   OPENWEATHER_API_KEY=your_api_key_here
   ```

5. Start the Flask server:
   ```
   python app.py
   ```

### Frontend

1. Navigate to the frontend directory:
   ```
   cd frontend
   ```

2. Install Node dependencies:
   ```
   npm install
   ```

3. Set up `.env` with the backend API URL:
   ```
   REACT_APP_API_URL=http://127.0.0.1:5000
   ```

4. Start the React development server:
   ```
   npm start
   ```

Open the React UI at `http://localhost:3000`, enter a city name, and fetch weather details.

---

## Future Improvements

- Enhance UI design and user interactivity.  
- Add caching to reduce API calls and improve response times.  
- Include user authentication and personalized weather settings.  
- Integrate a database for storing user preferences, search history, or cached weather data.  
- Add comprehensive unit and integration tests.  
- Prepare for deployment with Docker and CI/CD pipelines.

---

