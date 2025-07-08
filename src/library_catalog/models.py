from typing import Optional

from pydantic import BaseModel

class BaseBook(BaseModel):
    """ Базовый класс Pydantic для реализаци модели книги  """

    id: int



class NewBook(BaseBook):
    """ Класс Pydantic реализозации создания книги """

    title: str
    author: str
    year_publication: int
    genre: str
    number_pages: int
    access: bool = True
    description: str
    rating: float
    cover_url: str

    class Config:
        orm_mode = True

class BookUpdate(BaseModel):
    """ Класс Pydantic реализации обновлении книги  """

    title: Optional[str] = None
    author: Optional[str] = None
    year_publication: Optional[int] = None
    genre: Optional[str] = None
    number_pages: Optional[int] = None
    access: Optional[bool] = None
    description: Optional[str] = None
    rating: Optional[float] = None
    cover_url: Optional[str] = None


