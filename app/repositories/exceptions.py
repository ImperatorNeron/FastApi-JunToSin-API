class UnhandledRoleError(Exception):
    def __init__(self, role: str):
        super().__init__(f"Unhandled role: {role}")
        self.role = role
