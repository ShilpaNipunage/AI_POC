from codeVerifierEngine import WorkflowAdapter

class CodeVerifierParams:
    code : str

    def __init__(self, code):
        self.code = code

    def verify_code(self):
        adapter = WorkflowAdapter

        return adapter.verify_code(self.code)
        