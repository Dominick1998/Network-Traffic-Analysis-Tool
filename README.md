# Network Traffic Analysis and Visualization Tool

## Overview

The Network Traffic Analysis and Visualization Tool is a comprehensive web application designed to monitor, analyze, and visualize network traffic in real-time. It provides network administrators with insights into network activities, identifies potential threats, and assists in maintaining network security through an intuitive interface.

## Key Features

- **Traffic Monitoring**: Capture and display network traffic in real-time.
- **Traffic Visualization**: Generate graphical representations of network traffic using interactive charts.
- **Anomaly Detection**: Identify anomalous network traffic using statistical methods.
- **Firewall Management**: Manage firewall rules (block/allow traffic) directly from the interface.
- **Log Management**: View and manage server and security logs with log rotation capabilities.
- **Backup Management**: Create and restore database backups.
- **Security Monitoring**: Detect and log unauthorized access attempts, DDoS attacks, and other threats.
- **Audit Logging**: Track user activities, including logins, backups, and critical system changes.
- **Incident Reporting**: Manually report suspicious activities or network issues.
- **System Health Monitoring**: Monitor server performance, including CPU, memory, disk, and network usage.

## Technologies

- **Backend**: Python, Flask, SQLAlchemy, Scapy, Gunicorn, Flask-RESTful
- **Frontend**: React.js, D3.js, Axios
- **Database**: SQLite/PostgreSQL (configurable)
- **Security**: Flask-JWT-Extended for authentication, psutil for system monitoring, logging modules for security and audit logs.
- **Visualization**: D3.js, Matplotlib for generating charts.

## Installation

1. **Clone the repository:**
    ```bash
    git clone https://github.com/Dominick1998/Network-Traffic-Analysis-Tool.git
    ```

2. **Navigate to the project directory:**
    ```bash
    cd Network-Traffic-Analysis-Tool
    ```

3. **Set up a virtual environment** (optional but recommended):
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

4. **Install the required packages:**
    ```bash
    pip install -r requirements.txt # Required Dependencies 
    ```

5. **Set up the database** (SQLite by default):
    ```bash
    flask db upgrade
    ```

6. **Run the application:**
    ```bash
    flask run
    ```

7. **Access the application** at `http://localhost:5000`.

## API Endpoints

- `/api/traffic`: Fetch network traffic data.
- `/api/anomalies`: Retrieve anomalous network traffic.
- `/api/system_health`: Get server health metrics.
- `/api/logs`: View server logs.
- `/api/backup/create`: Create a database backup.
- `/api/backup/restore`: Restore a database backup.
- `/api/logs/audit`: View audit logs.
- `/api/logs/security`: View security logs.
- `/api/firewall/rules`: Manage firewall rules.

## Security Features

- **JWT Authentication**: Users authenticate via JSON Web Tokens (JWT) to access protected endpoints.
- **Rate Limiting and Throttling**: Prevent excessive API requests.
- **Unauthorized Access Detection**: Log suspicious or unauthorized access attempts.
- **DDoS Detection**: Identify abnormal traffic patterns to detect potential DDoS attacks.
- **Audit Logging**: Track and log key system events and user actions.

## Log Management

- **Audit Log Viewer**: View logs of user activities like logins, backups, and more.
- **Security Log Viewer**: View logs related to security threats, such as unauthorized access and DDoS attacks.
- **Log Rotation**: Automatic log rotation to prevent logs from growing excessively large.

## Backup Management

Administrators can create database backups and restore from backups to ensure data integrity and recoverability in the event of failures.

## System Health Monitoring

This tool provides system health metrics, including CPU usage, memory usage, disk usage, and network activity. Administrators can monitor system performance through an intuitive dashboard.

## Future Features

- **Cloud Deployment**: Enable deployment on cloud platforms like AWS or Azure.
- **Email Notifications**: Automatically notify administrators when security threats or anomalies are detected.
- **Advanced Traffic Analysis**: Implement machine learning models for enhanced anomaly detection.

## Contributing

We welcome contributions! Please fork the repository and submit a pull request for review.

## License

This project is licensed under the MIT License.
