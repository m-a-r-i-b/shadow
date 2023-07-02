from pydantic import BaseModel, Field

class Task(BaseModel):
    tool: str = Field(description="The tool to be used")
    instruction: str = Field(description="The instruction for the tool")

