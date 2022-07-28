*** Settings ***
Library  DebugLibrary
Library  ToDoListLibrary.py
Suite Teardown   quit program

*** Test Cases ***
Open view dialog
    open view dialog
    is dialog open
    dialog result should be    true

Test Ok Button
    open view dialog
    is dialog open
    dialog result should be    true
    dialog click ok
    is dialog open 
    dialog result should be    false

Test Cancel Button
    open view dialog
    is dialog open
    dialog result should be    true
    dialog click cancel 
    is dialog open
    dialog result should be    false

Open Add dialog
    open add dialog
    is dialog open
    dialog result should be     true
    dialog click cancel
Add Task
    open add dialog
    is dialog open
    dialog result should be     true
    add task name   Test name 1
    add task date   5/31
    add task time   06:00:00
    add task description    This is a test of the description
    add task ok
    is task added
    added task result should be     true

Does Task Exist
    does task exist   Test name 1
    task exist result should be   true

Cross task
    does task exist     Test name 1
    task exist result should be     true
    cross task  Test name 1
    is task crossed     Test name 1
    is task crossed result should be     true

Uncross task
    cross task  Test name 1
    is task crossed     Test name 1
    is task crossed result should be     false

Delete Task
    open edit dialog    Test name 1
    click delete button
    does task exist     Test name 1
    task exist result should be     false