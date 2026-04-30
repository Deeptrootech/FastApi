from models.activity_logs import ActivityLog


def create_activity_log(issue_id, action_type, performed_by_id, text, db):
    log = ActivityLog(issue_id=issue_id, action_type=action_type, performed_by_id=performed_by_id, metadata_=text)
    db.add(log)
    db.commit()
    db.refresh(log)
    return log
