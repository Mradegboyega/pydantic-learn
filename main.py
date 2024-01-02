import requests
from pydantic import BaseModel, confloat, validator
import uuid
from datetime import date, datetime, timedelta
from enums import Department

url = 'https://raw.githubusercontent.com/bugbytes-io/datasets/master/students_v1.json'

response = requests.get(url)
data = response.json()
data.append(
    {
        "id": "d15782d9-3d8f-4624-a88b-c8e836569df8",
        "name": "Michelle Oluwadarasimi",
        "date_of_birth": "2000-08-14",
        "GPA": "4.8",
        "course": "Computer Science",
        "department": "Science and Engineering",
        "fees_paid": True
    }
)


class Student(BaseModel):
    id: uuid.UUID
    name: str
    date_of_birth: date
    GPA: confloat(gt=0, lt=5)
    course: str | None
    department: Department
    fees_paid: bool

    @validator('date_of_birth')
    def must_be_16_or_over(cls, value):
        sixteen_years_ago = datetime.now() - timedelta(days=365*16)
        sixteen_years_ago = sixteen_years_ago.date()

        if value > sixteen_years_ago:
            raise ValueError("Too young to enroll, sorry")

        return value

for student in data:
    model = Student(**student)
    print(model.model_dump())
