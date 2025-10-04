from pydantic import BaseModel, Field

class ListReposParams(BaseModel):
    visibility: str = Field(default="all")
    affiliation: str = Field(default="owner,collaborator,organization_member")

class Repo(BaseModel):
    id: int
    name: str
    full_name: str
    private: bool
