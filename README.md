quiz_application_frontend
Overview The frontend of the Quiz App is built with React and provides an interactive user interface for taking quizzes, viewing results, and managing quiz-related data. It communicates with the Django backend via API endpoints.

Features User authentication (login and logout) Browse and take quizzes View quiz history and performance analytics Responsive design with Bootstrap Prerequisites Before running the frontend, ensure you have the following installed:

Node.js (v14 or higher) npm (Node package manager)

Available Scripts npm start: Runs the app in development mode. npm build: Builds the app for production to the build folder. npm test: Runs the test suite.

Project Structure src/: Contains the source code for the application. components/: Reusable React components. pages/: React components for different pages. App.js: Main application component. index.js: Entry point for the React application.

API Endpoints The frontend interacts with the following backend API endpoints: POST /api/scores/: Submits quiz scores. POST /api/logins/: Logs in a user. POST /api/logouts/: Logs out a user. POST /api/signups/: Logs in a user.

Contact For any questions or issues, please contact:

Email: belindaseshie5@gmail.com
