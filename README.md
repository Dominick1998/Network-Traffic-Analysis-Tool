# Network Traffic Analysis and Visualization Tool

## Overview

The **Network Traffic Analysis and Visualization Tool** is a web-based application designed to monitor, analyze, and visualize network traffic data in real-time. It provides detailed insights into network activity, including anomaly detection, traffic analysis, alerts, and data visualization using interactive charts and tables. The tool also supports data import/export, allowing administrators to manage traffic data efficiently.

This project is built with a comprehensive tech stack including Flask, SQLAlchemy, React.js, and D3.js for both backend processing and frontend visualization.

## Features

### 1. **Real-time Traffic Monitoring**
   - Capture and display network traffic with details like source, destination, protocol, and packet size.
   
### 2. **Data Visualization**
   - Interactive data visualization with traffic charts and anomaly detection graphs, built using D3.js and React.js.

### 3. **Anomaly Detection**
   - Identifies unusual traffic patterns using statistical analysis and flags anomalies.

### 4. **Alerts System**
   - Configurable alerts triggered by predefined network events (e.g., large packets or specific protocol usage).

### 5. **Data Export and Import**
   - Export network traffic data in CSV or JSON format.
   - Import traffic data from CSV files for historical or external data analysis.

### 6. **User Authentication**
   - Secure login/logout functionality with token-based authentication (JWT).

### 7. **Scheduler and Task Management**
   - Periodic tasks such as log rotation, daily summaries, and data cleanup are automated via a scheduler.
   - The scheduler can be paused or resumed from the admin interface.

### 8. **Log Management**
   - Logs all API requests and responses with log rotation to prevent overflow.

### 9. **Data Retention**
   - Configurable data retention policy to automatically delete old traffic data after a set period.

## Tech Stack

### **Backend:**
   - Flask (Python) - Web framework
   - SQLAlchemy - ORM for database interaction
   - PostgreSQL - Database for storing network traffic data
   - Gunicorn - WSGI HTTP server for deployment
   - Flask-JWT-Extended - For token-based authentication
   - Flask-CORS - For cross-origin resource sharing

### **Frontend:**
   - React.js - For creating dynamic user interfaces
   - D3.js - For interactive data visualization
   - CSS - Custom styling for UI components

### **Other Tools:**
   - Scapy - For capturing and analyzing network traffic
   - Pandas & NumPy - For statistical analysis and data handling
   - Pytest & Unittest - For testing backend functionality
   - Pylint - For linting and enforcing code standards

## Installation

### 1. **Clone the Repository**

```bash
git clone https://github.com/YourUsername/Network-Traffic-Analysis-Tool.git
cd Network-Traffic-Analysis-Tool
```

### 2. **Set Up the Python Environment**

We recommend creating a virtual environment to manage dependencies.

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
pip install -r requirements.txt
```

### 3. **Set Up the Database**

Make sure PostgreSQL is installed and running.

```bash
# Create the database
psql -c "CREATE DATABASE network_traffic;"
```

Edit your `.env` file to include database credentials.

```env
DATABASE_URL=postgresql://username:password@localhost/network_traffic
JWT_SECRET_KEY=your_secret_key
```

Run the database migrations:

```bash
flask db upgrade
```

### 4. **Run the Application**

```bash
flask run
```

By default, the app will run on `http://127.0.0.1:5000`.

### 5. **Run Tests**

```bash
pytest
```

This command will run all the backend tests to ensure everything is functioning correctly.

## Usage

1. **Login:** Use the provided login interface to authenticate.
2. **Monitor Traffic:** The dashboard provides real-time traffic monitoring with interactive charts.
3. **Manage Data:** Export data in CSV/JSON, import external data, and configure data retention policies.
4. **Alerts:** View any triggered alerts based on predefined conditions.

## Deployment

### Using Gunicorn:

For production, you can deploy the application using Gunicorn:

```bash
gunicorn -w 4 app:app
```

The app will be hosted at `http://127.0.0.1:8000`.

## Contributing

We welcome contributions from the community! If you'd like to contribute, please fork the repository and create a pull request with your proposed changes.

### 1. **Fork the Repository**
### 2. **Create a New Branch**

```bash
git checkout -b feature-branch
```

### 3. **Push Changes and Create a Pull Request**

```bash
git push origin feature-branch
```

Submit your PR, and we'll review it as soon as possible!

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgements

Special thanks to all the open-source projects and libraries that made this project possible, including:
- Flask
- SQLAlchemy
- React.js
- D3.js
- Scapy
