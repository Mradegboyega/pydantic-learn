import requests
from pydantic import BaseModel, confloat, field_validator, conint
import uuid
from datetime import date, datetime, timedelta
from enums import Department
from typing import Literal

url = 'https://raw.githubusercontent.com/bugbytes-io/datasets/master/students_v2.json'

response = requests.get(url)
data = response.json()

class Module(BaseModel):
    id: int | uuid.UUID
    name: str
    professor: str
    credits: Literal[10, 20]
    registration_code: str

    @field_validator('modules', check_fields=False)
    def validate_module_length(cls, value):
        if len(value) != 3:
            raise ValueError('List of modules should have length equal to 3')
        return value


class Student(BaseModel):
    id: uuid.UUID
    name: str
    date_of_birth: date
    GPA: confloat(ge=0, le=5)
    course: str | None
    department: Department
    fees_paid: bool
    modules: list[Module] = []

    @field_validator('date_of_birth')
    def must_be_16_or_over(cls, value):
        sixteen_years_ago = datetime.now() - timedelta(days=365*16)
        sixteen_years_ago = sixteen_years_ago.date()

        if value > sixteen_years_ago:
            raise ValueError("Too young to enroll, sorry")

        return value

# Iterate over data and create Student instances
# for student_data in data:
#     student_model = Student(**student_data)
#     print(student_model)
    
# Iterate over data and create Student instances
for student_data in data:
    student_model = Student(**student_data)
    for module in student_model.modules:
        print(module.model_dump_json(indent=2))


# print(Module.model_json_schema())

print(Student.model_json_schema())
