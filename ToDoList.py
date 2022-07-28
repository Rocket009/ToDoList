import sys
import socket
from types import SimpleNamespace
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QDialog
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QFormLayout
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QDialogButtonBox
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QCheckBox
from PyQt5.QtWidgets import QCalendarWidget
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QTimeEdit
from PyQt5.QtCore import *
from functools import partial
import json



class TodoUi(QMainWindow):

    def __init__(self):
        
        super().__init__()

        self.setWindowTitle('To Do List')
        self.windowHeight = 500
        self.windowLength = 500
        self.setFixedSize(self.windowHeight,self.windowLength)
        self.generalLayout = QVBoxLayout()
        self._centralWidget = QWidget(self)
        self.generalLayout.setAlignment(Qt.AlignTop)
        self.setCentralWidget(self._centralWidget)
        self.AddTaskButton = None
        self.CheckMarks = []
        self.Labels = []
        self.EditButtons = []
        self.ViewButtons = []
        self.ViewModel = None
        self.h_layout = []
    def AddViewModel(self,vm):
        self.ViewModel = vm
    def AddLabel(self,data):

        if self.AddTaskButton != None:
            self.AddTaskButton.close()
        v_layout = QHBoxLayout()
        self.h_layout.append(v_layout)
        Labels = QLabel(data)
        checkbox = QCheckBox('')
        editbutton = QPushButton('Edit')
        viewbutton = QPushButton('View')
        self.ViewButtons.append(viewbutton)
        self.CheckMarks.append(checkbox)
        self.Labels.append(Labels)
        self.EditButtons.append(editbutton)
        v_layout.addWidget(checkbox)
        v_layout.addWidget(Labels)
        v_layout.setAlignment(Qt.AlignLeft)
        v_layout.addWidget(viewbutton)
        v_layout.addWidget(editbutton)
        self.generalLayout.addLayout(v_layout)
        self.AddTaskButton = QPushButton('Add task')
        self.generalLayout.addWidget(self.AddTaskButton)
        self._centralWidget.setLayout(self.generalLayout)
        if self.ViewModel != None:
            self.ViewModel.connectSignals()
    
    def RemoveLabel(self,index):
        self.generalLayout.removeItem(self.h_layout[index])
        self.h_layout.pop(index)
        self.ViewButtons[index].close()
        self.ViewButtons.pop(index)
        self.CheckMarks[index].close()
        self.CheckMarks.pop(index)
        self.Labels[index].close()
        self.Labels.pop(index)
        self.EditButtons[index].close()
        self.EditButtons.pop(index)




    
class TaskDialog(QDialog):

        def __init__(self,title):

            super().__init__()
            self.setWindowTitle(title)
            self.dlgLayout = QVBoxLayout()
            formLayout = QFormLayout()
            self.TaskName = QLineEdit()
            self.TaskDescription = QLineEdit()
            formLayout.addRow('Task name: ', self.TaskName)
            self.dlgLayout.addLayout(formLayout)
            self.calender = QCalendarWidget()
            self.btns = QDialogButtonBox(QDialogButtonBox.Cancel | QDialogButtonBox.Ok)
            self.TimeEdit = QTimeEdit()
            self.TaskDescription.adjustSize()
            self.dlgLayout.addWidget(self.calender)
            self.dlgLayout.addWidget(self.TimeEdit)
            self.dlgLayout.addWidget(QLabel('Description'))
            self.dlgLayout.addWidget(self.TaskDescription)
            self.dlgLayout.addWidget(self.btns)
            self.setLayout(self.dlgLayout)




class AddTaskDialog(TaskDialog):
    def __init__(self):

        super().__init__(title='Add Task')




class EditTaskDialog(TaskDialog):
    def __init__(self):

        super().__init__(title='Edit Task')
        self.deleteButton = QPushButton('Delete')
        self.dlgLayout.addWidget(self.deleteButton)


class ViewTaskDialog(TaskDialog):
    def __init__(self):
        
        super().__init__(title='View Task')
        self.TaskName.setReadOnly(True)
        self.TaskDescription.setReadOnly(True)



class Tasks:
    def __init__(self):
            self.TasksL = dict()
    def checkTask(self):
        if len(self.TasksL) > 0:
            for t in self.TasksL.copy():
                if self.TasksL[t]['iscrossed'] == True:
                        self.TasksL.pop(t)
                        if not len(self.TasksL) > 0:
                            break
    def getTaskKey(self,index : int) -> str:
        keys = list(self.TasksL)
        return keys[index]
    def addTask(self,taskname,date='',time='',description=''):
        temp = {'date' : date, 'time' : time, 'description' : description, 'iscrossed' : False}
        self.TasksL.update({taskname : temp})
    def editTask(self,index,taskname,date=None,description=None,time=None):
        keys = list(self.TasksL)
        newT = {taskname if k == keys[index] else k:v for k,v in self.TasksL.items()}
        if date != None:
            newT[taskname]['date'] = date
        if description != None:
            newT[taskname]['description'] = description
        if time != None:
            newT[taskname]['time'] = time
        self.TasksL = newT
    def getTaskIndex(self, task) -> int:
        counter = 0
        keys = list(self.TasksL.keys())
        if not task in keys:
            return None
        for key in self.TasksL:
            if key == task:
                break
            counter += 1
        return counter



class ConfigMaker:
    def __init__(self, tasks : Tasks) -> None:
        try:
            with open('config.json','r') as f:
                tasks.TasksL = json.load(f)
        except IOError:
            pass
    def CreateConfig(self, tasks : Tasks):
        with open('config.json', 'w') as f:
            json.dump(tasks.TasksL,f)



class ViewModel:
    def __init__(self,view : TodoUi):
        self.view = view
        self.Tasks = Tasks()
        self.config = ConfigMaker(self.Tasks)
        if len(self.Tasks.TasksL) > 0:
            self.Tasks.checkTask()
            if len(self.Tasks.TasksL) > 0:
                keys = self.Tasks.TasksL.keys()
                for k in keys:
                    if type(k) is str:
                        self.view.AddLabel(k)
            else:
                self.AddTask()
        else:
            self.AddTask()
        self.connectSignals()
    def closeLables(self,index):
        self.view.Labels[index].close()
        self.view.CheckMarks[index].close()
    def strikeText(self,text : str) -> str:
        result = ''
        for c in text:
            result = result + c + '\u0336'
        return result
    def unstrikeText(self,text : str) -> str:
        result = text.replace('\u0336','')
        return result
    def parseDate(self) -> str:
        date = self.dialog.calender.selectedDate()
        day = date.day()
        month = date.month()
        taskd = str(month) + '/' + str(day)
        return taskd
    def Accepted(self):
        task = self.dialog.TaskName.text()
        date = self.parseDate()
        description = self.dialog.TaskDescription.text()
        time = self.dialog.TimeEdit.time()
        time = self.ParseTime(time)
        self.Tasks.addTask(task,date=date,time=time,description=description)
        self.view.AddLabel(task)
        self.config.CreateConfig(self.Tasks)
        self.dialog.close()
    def Rejected(self):
        self.dialog.close()
    def ParseTime(self,time : QTime) -> str:
        return time.toString()
    def AddTask(self):
        self.dialog = AddTaskDialog()
        self.dialog.btns.accepted.connect(self.Accepted)
        self.dialog.btns.rejected.connect(self.Rejected)
        self.dialog.exec_()
    def RemoveTask(self,index):
        if not self.Tasks.TasksL[self.Tasks.getTaskKey(index)]['iscrossed']:
            text = self.view.Labels[index].text()
            striketext = self.strikeText(text)
            self.view.Labels[index].setText(striketext)
            self.Tasks.TasksL[self.Tasks.getTaskKey(index)]['iscrossed'] = True
        else:
            text = self.view.Labels[index].text()
            unstrike = self.unstrikeText(text)
            self.view.Labels[index].setText(unstrike)
            self.Tasks.TasksL[self.Tasks.getTaskKey(index)]['iscrossed'] = False
        self.config.CreateConfig(self.Tasks)
    def AcceptedEdit(self,index):
        taskname = self.dialog.TaskName.text()              
        self.view.Labels[index].setText(taskname)
        description = self.dialog.TaskDescription.text()
        qtime = self.dialog.TimeEdit.time()
        time = self.ParseTime(qtime)
        self.Tasks.editTask(index,taskname=taskname,date=self.parseDate(),description=description,time=time)
        self.config.CreateConfig(self.Tasks)
        self.dialog.close()
    def deleteTask(self,index):
        key = self.Tasks.getTaskKey(index)
        self.Tasks.TasksL.pop(key)
        self.dialog.close()
        self.disconnectSignals()
        self.view.RemoveLabel(index)
        self.connectSignals()
        self.config.CreateConfig(self.Tasks)
    def unparseDate(self,index) -> QDate:
        key = self.Tasks.getTaskKey(index)
        date = self.Tasks.TasksL[key]['date']
        loc = date.find('/')
        newstr = date.replace('/','')
        month = newstr[:loc]
        day = newstr[loc:]
        qdate = QDate(2022, int(month), int(day))
        if not qdate.isValid():
            raise Exception('Date not valid')
        return qdate
    def unparseTime(self,index) -> QTime:
        key = self.Tasks.getTaskKey(index)
        time = self.Tasks.TasksL[key]['time']
        qtime = QTime().fromString(time)
        return qtime
    def getTaskDescription(self,index) -> str:
        key = self.Tasks.getTaskKey(index)
        return self.Tasks.TasksL[key]['description']
    def editTask(self,index):
        self.dialog = EditTaskDialog()
        self.dialog.TaskName.setText(self.Tasks.getTaskKey(index))
        self.dialog.calender.setSelectedDate(self.unparseDate(index))
        self.dialog.TimeEdit.setTime(self.unparseTime(index))
        self.dialog.TaskDescription.setText(self.getTaskDescription(index))
        self.dialog.btns.accepted.connect(partial(self.AcceptedEdit,index))
        self.dialog.btns.rejected.connect(self.Rejected)
        self.dialog.deleteButton.clicked.connect(partial(self.deleteTask,index))
        self.dialog.exec_()
    def viewTask(self,index):
        self.dialog = ViewTaskDialog()
        self.dialog.TaskName.setText(self.Tasks.getTaskKey(index))
        self.dialog.calender.setSelectedDate(self.unparseDate(index))
        self.dialog.TimeEdit.setTime(self.unparseTime(index))
        self.dialog.TaskDescription.setText(self.getTaskDescription(index))
        self.dialog.btns.accepted.connect(self.Rejected)
        self.dialog.btns.rejected.connect(self.Rejected)
        self.dialog.exec_()
    def connectSignals(self):
        self.view.AddTaskButton.clicked.connect(self.AddTask)
        index = 0
        for c in self.view.CheckMarks:
            c.stateChanged.connect(partial(self.RemoveTask,index))
            self.view.EditButtons[index].clicked.connect(partial(self.editTask,index))
            self.view.ViewButtons[index].clicked.connect(partial(self.viewTask,index))
            index += 1
    def disconnectSignals(self):
        self.view.AddTaskButton.clicked.disconnect()
        index = 0
        for c in self.view.CheckMarks:
            c.stateChanged.disconnect()
            self.view.EditButtons[index].clicked.disconnect()
            self.view.ViewButtons[index].clicked.disconnect()
            index += 1
    def OpenDialog(self):
        self.OnOpenDialog()



class ToDoInterface:
    def __init__(self,vm : ViewModel,ui : TodoUi, app : QApplication):
        self.vm = vm
        self.ui = ui
        self.app = app
        self.taskName = ''
        self.taskDate = ''
        self.taskTime = ''
        self.taskDescription = ''

    def open_view_dialog(self):
        self.vm.viewTask(0)
  
    def is_dialog_open(self) -> bool:
        try:
            val = self.vm.dialog.isVisible()
            return val
        except NameError:
            return False
    def quit_program(self):
        self.app.quit()

    def dialog_click_ok(self) -> str:
        try:
            ok = self.vm.dialog.btns.button(QDialogButtonBox.Ok)
            if ok != None:
                ok.click()
                return 'Ok'
            else:
                return 'DialogErrorOk'
        except NameError:
            return 'DialogErrorOk'
        except: return 'UnknownDialogError'

    def dialog_click_cancel(self) -> str:
        try:
            cancel = self.vm.dialog.btns.button(QDialogButtonBox.Cancel)
            if cancel != None:
                cancel.click()
                return 'Ok'
            else:
                return 'DialogErrorCancel'
        except NameError:
            return 'DialogErrorCancel'
        except: return 'UnknownDialogError'
    def open_add_dialog(self):
        self.vm.AddTask()
    def add_task_name(self,task):
        self.vm.dialog.TaskName.setText(task)
        self.taskName = task
    def unparseDate(self,date):
        loc = date.find('/')
        newstr = date.replace('/','')
        month = newstr[:loc]
        day = newstr[loc:]
        qdate = QDate(2022, int(month), int(day))
        if not qdate.isValid():
            raise Exception('Date not valid')
        return qdate
    def add_task_date(self,date):
        self.vm.dialog.calender.setSelectedDate(self.unparseDate(date))
        self.taskDate = date
    def add_task_time(self,time):
        self.vm.dialog.TimeEdit.setTime(QTime().fromString(time))
        self.taskTime = time
    def add_task_description(self,description):
        self.vm.dialog.TaskDescription.setText(description)
        self.taskDescription = description
    def add_task_ok(self):
        self.vm.Accepted()
    def add_task_cancel(self):
        self.vm.Rejected()
    def is_task_added(self) -> str:
        keys = list(self.vm.Tasks.TasksL.keys())
        tasks = self.vm.Tasks.TasksL
        index = len(keys) - 1
        if keys[index] != self.taskName:
            return 'false'
        elif tasks[self.taskName]['date'] != self.taskDate:
            return 'false'
        elif tasks[self.taskName]['time'] != self.taskTime:
            return 'false'
        elif tasks[self.taskName]['description'] != self.taskDescription:
            return 'false'
        else: return 'true'
    def cross_task(self, index):
        self.vm.RemoveTask(self.vm.Tasks.getTaskIndex(index))
    def does_task_exist(self,task) -> str:
        keys = list(self.vm.Tasks.TasksL.keys())
        if task in keys:
            return 'true'
        else:
            return 'false'
    def is_task_crossed(self,task):
        if self.vm.Tasks.TasksL[task]['iscrossed']:
            return 'true'
        else: return 'false'
    def click_delete_button(self):
        self.vm.dialog.deleteButton.click()
    def open_edit_dialog(self,task):
        self.vm.editTask(self.vm.Tasks.getTaskIndex(task))




class EventParsor:

    def __init__(self,vm,ui,app):
        self.interface = ToDoInterface(vm,ui,app)
        self.thread = QThread()
        self.Sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.Sock.bind(('localhost', 50000))
        self.Sock.listen(1)
        self.sock, addr = self.Sock.accept()
        self.threadflag = SimpleNamespace()
        self.threadflag.flag = True
        self.server = RecvServer(self.sock,self.threadflag)
        self.server.moveToThread(self.thread)
        self.thread.started.connect(self.server.run)
        self.server.data_sig.connect(self.parseData)
        self.thread.start()

    def sendData(self,data : str):
        self.sock.sendall(bytes(data,'utf-8'))
    def parseData(self,data):
        match data:
            case 'open_view_dialog':
                self.sendData('Ok')
                self.interface.open_view_dialog()
            case 'dialog_click_ok':
                val = self.interface.dialog_click_ok()
                self.sendData(val)
            case 'dialog_click_cancel':
                val = self.interface.dialog_click_cancel()
                self.sendData(val)
            case 'is_dialog_open':
                bol = self.interface.is_dialog_open()
                if bol == True: stri = 'true'
                else: stri = 'false'
                self.sendData(stri)
                self.sendData(stri)
            case 'quit_program':
                self.threadflag.flag = False
                self.sock.close()
                self.thread.terminate()
                self.interface.quit_program()
            case 'open_add_dialog':
                self.sendData('Ok')
                self.interface.open_add_dialog()
            case 'add_task_ok':
                self.interface.add_task_ok()
                self.sendData('Ok')
            case 'add_task_cancel':
                self.interface.add_task_cancel()
                self.sendData('Ok')
            case 'is_task_added':
                bol = self.interface.is_task_added()
                self.sendData(bol)
            case 'click_delete_button':
                self.sendData('Ok')
                self.interface.click_delete_button()

        if 'add_task_name' in data:
            arg = data[len('add_task_name') + 1:]
            self.sendData('Ok')
            self.interface.add_task_name(arg)
        elif 'add_task_date' in data:
            arg = data[len('add_task_date') + 1:]
            self.sendData('Ok')
            self.interface.add_task_date(arg)
        elif 'add_task_time' in data:
            arg = data[len('add_task_time') + 1:]
            self.sendData('Ok')
            self.interface.add_task_time(arg)
        elif 'add_task_description' in data:
            arg = data[len('add_task_description') + 1:]
            self.sendData('Ok')
            self.interface.add_task_description(arg)
        elif 'cross_task' in data:
            arg = data[len('cross_task') + 1:]
            self.sendData('Ok')
            self.interface.cross_task(arg)
        elif 'does_task_exist' in data:
            arg = data[len('does_task_exist') + 1:]
            bol = self.interface.does_task_exist(arg)
            self.sendData(bol)
        elif 'is_task_crossed' in data:
            arg = data[len('is_task_crossed') + 1:]
            bol = self.interface.is_task_crossed(arg)
            self.sendData(bol)
        elif 'open_edit_dialog' in data:
            arg = data[len('open_edit_dialog') + 1:]
            self.sendData('Ok')
            self.interface.open_edit_dialog(arg)
        



class RecvServer(QObject):
    data_sig = pyqtSignal(str)
    def __init__(self,Sock : socket.socket, threadflag):
        super().__init__()
        self.Sock = Sock
        self.threadflag = threadflag
    def run(self):
        while self.threadflag.flag:
            try:
                data = self.Sock.recv(1024)
            except ConnectionAbortedError:
                break
            self.data_sig.emit(str(data,'utf-8'))



def robotmain():
    
    todo = QApplication(sys.argv)
    view = TodoUi()
    viewModel = ViewModel(view)
    eventparsor = EventParsor(viewModel,view,todo)
    view.AddViewModel(viewModel)
    view.show()
    todo.exec_()

def main():
    todo = QApplication(sys.argv)
    view = TodoUi()
    viewModel = ViewModel(view)
    view.AddViewModel(viewModel)
    view.show()
    sys.exit(todo.exec_())

if __name__ == "__main__":
    main()