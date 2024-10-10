from backend.database import get_db_session
from backend.models import IncidentReport
from datetime import datetime

def create_incident_report(user_id, title, description, severity):
    """
    Create a new incident report.

    Args:
        user_id (int): ID of the user creating the report.
        title (str): Title of the incident report.
        description (str): Detailed description of the incident.
        severity (str): Severity level of the incident (e.g., 'low', 'medium', 'high').

    Returns:
        dict: Success or failure message.
    """
    session = get_db_session()
    try:
        report = IncidentReport(
            user_id=user_id,
            title=title,
            description=description,
            severity=severity,
            created_at=datetime.utcnow()
        )
        session.add(report)
        session.commit()
        return {'message': 'Incident report created successfully.'}
    except Exception as e:
        session.rollback()
        return {'error': f"Failed to create incident report: {e}"}
    finally:
        session.close()

def get_incident_reports():
    """
    Retrieve all incident reports.

    Returns:
        list: A list of incident reports.
    """
    session = get_db_session()
    try:
        reports = session.query(IncidentReport).all()
        return [
            {
                'title': report.title,
                'description': report.description,
                'severity': report.severity,
                'timestamp': report.created_at.isoformat()
            }
            for report in reports
        ]
    except Exception as e:
        return []
    finally:
        session.close()
