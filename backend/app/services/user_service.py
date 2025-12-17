from typing import List
from sqlalchemy import or_
from sqlalchemy.orm import Session
import models

class UserService:
    def __init__(self,db:Session):
        self.db=db

    def search_users(
            self,
            query: str
        ) -> List[models.User]:

        q=f"%{query}%"

        users=(
            self.db.query(models.User)
            .filter(
                models.User.email.ilike(q),
                or_(
                    models.User.email.ilike(q),
                    models.User.first_name.ilike(q),
                    models.User.last_name.ilike(q),
                )
            )
            .all()
        )

        return users