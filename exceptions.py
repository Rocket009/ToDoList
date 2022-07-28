class DialogError(Exception):
    def __init__(self,error : str):
        super().__init__(error)

class DialogErrorOk(DialogError):
    def __init__(self):
        super().__init__('Error pressing Ok on the Dialog')

class DialogErrorNotAssigned(DialogError):
    def __init__(self):
        super().__init__('Dialog variable was not Assigned')

class DialogErrorCancel(DialogError):
    def __init__(self):
        super().__init__('Error pressing Cancel on the Dialog')

class SocketError(Exception):
    pass

class DialogOpenError(DialogError):
    def __init__(self,expected : str):
        if expected == 'true':
            strin = 'Dialog failed to open'
        elif expected == 'false':
            strin = 'Dialog failed to close'
        else:
            strin = 'expected value is not true, or false'
        super().__init__(strin)

class TasksError(Exception):
    def __init__(self, error='Unkown Task Error'):
        super().__init__(error)

class TaskDoesNotExist(TasksError):
    def __init__(self):
        super().__init__('The task does not exist')

class TaskCrossedError(TasksError):
    def __init__(self,task):
        super().__init__('There is a task crossed error')