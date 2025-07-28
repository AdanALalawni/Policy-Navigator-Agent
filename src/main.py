
from agent_creation import read_prompt, create_agent
prompt = read_prompt("prompt.txt")
create_agent(
        name="Policy Navigators",
        description="Agent to search about policies and regulations",
        prompt=prompt
    )