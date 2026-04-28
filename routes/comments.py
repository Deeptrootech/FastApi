from fastapi import APIRouter

router = APIRouter()


@router.get("/issues/{issue_id}/comments")
def get_comments(issue_id: int):
    return {"message": f"{issue_id} ---> comments"}
