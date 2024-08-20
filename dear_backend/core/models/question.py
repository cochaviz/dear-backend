from pydantic import BaseModel


class Question(BaseModel):
    content: str
    user_id: str

    def __str__(self) -> str:
        return f"Question(content={self.content}, user_id={self.user_id})"
