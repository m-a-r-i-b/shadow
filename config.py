# some agents can be less powerful than others
SHADOW_AGENT_LLM = "text-davinci-003"
SHADOW_AGENT_TEMP = 0

MODIFY_CODE_TOOL_LLM = "gpt-3.5-turbo"
MODIFY_CODE_TOOL_TEMP = 0

VERSION_CONTROL_TOOL_LLM = "gpt-3.5-turbo"
VERSION_CONTROL_TOOL_TEMP = 0

# Project to make changes to
PROJ_ROOT_DIR = "../test-app"
PROJ_WORK_DIR = PROJ_ROOT_DIR+"/src"

# The type of files to vectorize and make changes to
ACCEPTABLE_FILE_TYPES = [
    ".js",
    ".jsx",
    ".ts",
    ".tsx",
    ".css",
    ".scss",
    ".py",
]

# OPERATION_MODE = "TEXT"
OPERATION_MODE = "AUDIO"

AUDIO_FILE_PATH = "aduio_instructions.wav"