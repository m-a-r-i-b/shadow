from pydantic import BaseModel, Field

class Task(BaseModel):
    tool_name: str = Field(description="The tool to be used")
    instruction: str = Field(description="The instruction for the tool")

