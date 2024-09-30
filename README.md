# Network Traffic Analysis and Visualization Tool

## Overview

The **Network Traffic Analysis and Visualization Tool** is a comprehensive platform designed to monitor, analyze, and visualize network traffic in real time. The tool supports custom alerting, performance monitoring, threat detection (such as DDoS attacks), and logging of user activities. It is built to assist administrators in maintaining network security, performance, and troubleshooting through interactive visualizations and data analysis.

## Features

- **Traffic Data Visualization**: Captures and displays network traffic data in real time, with detailed charts and tables.
- **Anomaly Detection**: Detects anomalies in network traffic and sends email notifications for further investigation.
- **Custom Alerts**: Allows administrators to define custom alerts based on network traffic conditions, such as high traffic volume from specific IPs or protocols.
- **Threat Detection**: Detects potential threats, such as Distributed Denial of Service (DDoS) attacks.
- **User Activity Logging**: Logs user actions such as login attempts, data exports, and other key activities for auditing purposes.
- **Data Export/Import**: Supports exporting network traffic data as CSV or JSON and importing traffic data from CSV files.
- **Performance Monitoring**: Monitors system performance, including CPU and memory usage, to ensure optimal system operation.
- **Log Management**: Allows administrators to view and download server logs for debugging and monitoring.
- **Customizable Data Retention**: Allows administrators to set a retention period for network traffic data to manage storage effectively.

## Technology Stack

- **Backend**: Python (Flask), SQLAlchemy (Database ORM)
- **Frontend**: JavaScript (React), D3.js (for data visualization)
- **Database**: SQL/NoSQL options (e.g., PostgreSQL, MongoDB)
- **Visualization**: D3.js and Chart.js
- **Performance Monitoring**: psutil (for system resource tracking)

## Setup and Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/network-traffic-analysis-tool.git
   ```

2. Navigate to the project directory:
   ```bash
   cd network-traffic-analysis-tool
   ```

3. Create and activate a Python virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # For Linux/Mac
   .\venv\Scripts\activate   # For Windows
   ```

4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

5. Set up environment variables (e.g., for database configuration, email notifications).

6. Initialize the database:
   ```bash
   flask db init
   flask db migrate
   flask db upgrade
   ```

7. Run the Flask server:
   ```bash
   flask run
   ```

8. Access the frontend by opening `http://localhost:5000` in your browser.

## Usage

- **Network Traffic**: View captured network traffic and visualize it using interactive charts.
- **Anomalies**: Detect network anomalies and receive email notifications.
- **Alerts**: Set custom alert rules to monitor specific traffic patterns.
- **Logs**: View and download system logs for debugging.
- **Performance Monitoring**: Monitor system performance, including CPU and memory usage, from the frontend interface.

## API Endpoints

- `/api/health`: Check the health of the server.
- `/api/login`: User authentication (JWT-based).
- `/api/traffic`: Retrieve network traffic data.
- `/api/anomalies`: Detect anomalies in network traffic.
- `/api/alerts`: Manage custom alert rules (create, view, delete).
- `/api/logs`: View and download server logs.
- `/api/threats`: Detect potential DDoS attacks or other threats.
- `/api/performance`: Get system performance metrics (CPU, memory).
- `/api/user_activity`: Retrieve logs of user activities.

### **Explanation:**
- **Flask**: The core backend framework.
- **SQLAlchemy and Flask-SQLAlchemy**: For database operations.
- **psutil**: Used for system performance monitoring (CPU and memory usage).
- **Flask-JWT-Extended**: For user authentication and token management.
- **pymongo** and **psycopg2-binary**: Database connectors for MongoDB and PostgreSQL, respectively (depending on the chosen database).
- **D3.js, React, and Chart.js**: Frontend libraries for data visualization and UI management.

## Contributing

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Commit your changes (`git commit -m "Add feature"`).
4. Push to the branch (`git push origin feature-branch`).
5. Create a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

