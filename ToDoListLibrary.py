from robot.api.deco import keyword,library
from api_connector import api_connector
import exceptions

@library
class ToDoListLibrary:

    ROBOT_LIBRARY_SCOPE = 'GLOBAL'

    def __init__(self):
        self.api = api_connector()
        self.result = ''
    
    @keyword
    def open_view_dialog(self):
        self.api.send_keyword('open_view_dialog')
    
    @keyword
    def is_dialog_open(self):
        self.api.send_keyword('is_dialog_open')
        self.result = self.api.get_result()
    def dialog_check_exceptions(self,result):
        match result:
            case 'DialogErrorOk': raise exceptions.DialogErrorOk
            case 'DialogErrorCancel': raise exceptions.DialogErrorCancel
            case 'UnknownDialogError': raise exceptions.DialogError('There is an error with the Dialog')
    @keyword
    def dialog_click_ok(self):
        result = self.api.send_keyword('dialog_click_ok')
        self.dialog_check_exceptions(result)
    @keyword
    def dialog_click_cancel(self):
        result = self.api.send_keyword('dialog_click_cancel')
        self.dialog_check_exceptions(result)

    @keyword
    def dialog_result_should_be(self, expected):
        if self.result != expected:
            raise exceptions.DialogOpenError(expected)

    @keyword
    def quit_program(self):
        self.api.send_keyword('quit_program')
    
    @keyword
    def open_add_dialog(self):
        self.api.send_keyword('open_add_dialog')

    @keyword
    def add_task_ok(self):
        self.api.send_keyword('add_task_ok')

    @keyword
    def add_task_cancel(self):
        self.api.send_keyword('add_task_cancel')
    
    @keyword
    def add_task_name(self, name):
        self.api.send_keyword_args('add_task_name',name)

    @keyword
    def add_task_date(self,date):
        self.api.send_keyword_args('add_task_date',date)

    @keyword
    def add_task_time(self,time):
        self.api.send_keyword_args('add_task_time',time)

    @keyword
    def add_task_description(self,des):
        self.api.send_keyword_args('add_task_description',des)

    @keyword
    def is_task_added(self):
        self.result = self.api.send_keyword('is_task_added')
        print(self.result)
    
    @keyword
    def added_task_result_should_be(self, expected):
        if self.result != expected:
            raise exceptions.TasksError

    @keyword
    def cross_task(self,index):
        self.api.send_keyword_args('cross_task',index)

    @keyword
    def does_task_exist(self,task):
        self.result = self.api.send_keyword_args('does_task_exist',task)
    
    @keyword
    def task_exist_result_should_be(self,expected):
        if self.result != expected:
            print(self.result)
            raise exceptions.TaskDoesNotExist
    
    @keyword
    def is_task_crossed(self,task):
        self.result = self.api.send_keyword_args('is_task_crossed',task)
        print(self.result)

    @keyword
    def is_task_crossed_result_should_be(self,expected):
        if self.result != expected:
            print(self.result)
            raise exceptions.TaskCrossedError

    @keyword
    def click_delete_button(self):
        self.api.send_keyword('click_delete_button')

    @keyword
    def open_edit_dialog(self,task):
        self.api.send_keyword_args('open_edit_dialog', task)