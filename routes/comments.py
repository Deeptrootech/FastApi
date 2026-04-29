from fastapi import APIRouter, Depends, HTTPException

from database.database import get_db
from dependency import is_authenticated
from models.comments import Comment
from models.issues import Issue
from schema.comment import AddComment
from utils.activity_log import create_activity_log

router = APIRouter()


@router.post("/issues/{issue_id}/comments")
def add_comments(comment_payload: AddComment, issue_id: int, db=Depends(get_db), current_user=Depends(is_authenticated)):
    issue = db.query(Issue).filter(Issue.id == issue_id).first()
    if not issue:
        raise HTTPException(status_code=404, detail="Issue not found")

    comment = Comment(user_id=current_user.id, issue_id=issue_id, text=comment_payload.text)
    db.add(comment)
    db.commit()
    db.refresh(comment)

    create_activity_log(issue.id, "comment_added", current_user.id,
                        f"{current_user.name} added a comment to issue {issue.title}")
    return comment
