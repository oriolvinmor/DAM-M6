from sqlalchemy import Column, Integer, String
from config.base import Base

# Definir el modelo de la tabla
class Student(Base):
    __tablename__ = 'students'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), index=True)  # Especifica la longitud para VARCHAR
    spec = Column(String(50), index=True)  # Especifica la longitud para VARCHAR
    age = Column(Integer)

    def __init__(self, name: str, age: int, spec: str):
        self.name = name
        self.age = age
        self.spec = spec

    def __repr__(self):
        return f"<Student(id={self.id}, name='{self.name}', spec='{self.spec}', age={self.age})>"

    def __str__(self):
        return f"Student(id={self.id}, name='{self.name}', spec='{self.spec}', age={self.age})"

    def serialize(self):
        """Return object data in easily serializable format."""
        return {
            'id': self.id,
            'name': self.name,
            'spec': self.spec,
            'age': self.age
        }
