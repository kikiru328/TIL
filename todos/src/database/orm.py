# Modeling

from sqlalchemy.orm import declarative_base
from sqlalchemy import Boolean, Column, Integer, String

Base = declarative_base() # default format

class ToDo(Base):
    __tablename__ = "todo"

    id = Column(Integer, primary_key=True, index=True)
    contents = Column(String, nullable=False)
    is_done = Column(Boolean, nullable=False)

    # repr: re-print
    def __repr__(self):
        return f"ToDo(id= {self.id}, contents= {self.contents}, is_done= {self.is_done}"



