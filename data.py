from pydantic import Field, BaseModel, ValidationError, model_validator, field_validator
from typing import Literal, Optional
from pydantic import ConfigDict


class Person(BaseModel):
    name: str = Field(..., min_length=2)
    age: int|None = Field(default=None,ge=0,le=100)
    # role: Literal["suspect", "victim", "witness"]
    phone: Optional[str] = None


class RelationShip(BaseModel):
    person1: str
    relation: str
    person2: str


class CaseRecord(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    case_id: str = Field(alias="caseId")
    people: list[Person]
    relationships: list[RelationShip]

    @field_validator("case_id")
    @classmethod
    def clean(cls, case_id):
        return case_id.strip()

    # @model_validator(mode="after")
    # def validate_rship(self):
    #     existing_peps = {person.name for person in self.people}
    #     for relationship in self.relationships:
    #         if relationship.person1 not in existing_peps:
    #             raise ValueError("doesnt exist in peoples ")
    #         if relationship.person2 not in existing_peps:
    #             raise ValueError("doesnt exist")
    #     return self


# raw_data = {
#     "case_id": "          FIR-001                            ",
#     "people": [
#         {"name": "Rahul", "age": 25},
#         {"name": "Amit", "age": 30},
#         {"name": "Priya", "age": 22}
#     ],
#     "relationships": [
#         {
#             "person1": "Rahul",
#             "relation": "knows",
#             "person2": "Priya"
#         },
#         {
#             "person1": "Amit",
#             "relation": "works_with",
#             "person2": "Priya"
#         }
#     ]
# }
#
# Case = CaseRecord(**raw_data)
# case_dict = Case.model_dump()
# print(Case.model_dump_json())
# print("\n")
# print(Case)
# # print(Case.model_dump())
