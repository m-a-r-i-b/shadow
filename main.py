

# some agents can be less powerful than others
init_agents()


prompt = "test task1 test task2"
identified_tasks = identifyTasks(prompt)

for task in identified_tasks:

    relevant_agent = identifyAgent(task)
    relevant_agent.execute(task)
