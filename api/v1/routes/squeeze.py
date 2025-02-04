from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from api.db.database import get_db
from api.core.responses import SUCCESS
from api.utils.success_response import success_response
from api.v1.services.squeeze import squeeze_service
from api.v1.schemas.squeeze import CreateSqueeze
from api.v1.services.user import user_service
from api.v1.models import *

squeeze = APIRouter(prefix="/squeeze", tags=["Squeeze Page"])


@squeeze.post("", response_model=success_response, status_code=201)
def create_squeeze(
    data: CreateSqueeze,
    db: Session = Depends(get_db),
    current_user: User = Depends(user_service.get_current_super_admin),
):
    """Create a squeeze page"""
    user = user_service.fetch_by_email(db, data.email)
    if not user:
        return success_response(status.HTTP_404_NOT_FOUND, "User not found!")
    data.user_id = user.id
    data.full_name = f"{user.first_name} {user.last_name}"
    new_squeeze = squeeze_service.create(db, data)
    return success_response(status.HTTP_201_CREATED, SUCCESS, new_squeeze.to_dict())
