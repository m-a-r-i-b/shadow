import abc


class BaseTool:

    @abc.abstractmethod
    def parse_output(self, raw_result, parsed_output):
        raise NotImplementedError()

    @abc.abstractmethod
    def execute_task(self, arg1):
        # print("recieved args 1= ",arg1)
        # print("recieved args 2= ",arg2)
        # prompt = self.prompt_template.format(**kwargs)
        # raw_result = self.llm._call(prompt)
        # parsed_result = self.parse_output(raw_result)
        # return "Job is done"
        raise NotImplementedError()

