Getting User Input
==================


Alerts
------



    >>> import PyXA
    >>> response = PyXA.XAAlert(
    >>>     title = "Alert!",
    >>>     message = "",
    >>>     style = PyXA.XAAlertStyle.INFORMATIONAL,
    >>>     buttons = ["Ok", "Cancel"]
    >>> ).display()
    >>> print(response)
    1000


Dialogs
-------


    >>> import PyXA
    >>> response = PyXA.XADialog(
    >>>     text = "This is a dialog",
    >>>     title = "Notice",
    >>>     buttons = ["Ok", "Cool", "Thanks"],
    >>>     icon = "caution",
    >>> ).display()
    >>> print(response)
    Cool


    >>> import PyXA
    >>> response = PyXA.XADialog(
    >>>     text = "What is your name?",
    >>>     title = "What is your name?",
    >>>     buttons = ["Continue"],
    >>>     default_button = "Continue",
    >>>     icon = "note",
    >>>     default_answer = ""
    >>> ).display()
    >>> print("Your name is", response[1])
    Your name is Steven

    >>> import PyXA
    >>> response = PyXA.XADialog(
    >>>     text = "Enter the secret",
    >>>     title = "Super Secret",
    >>>     buttons = ["Continue"],
    >>>     default_button = "Continue",
    >>>     icon = "note",
    >>>     default_answer = "",
    >>>     hidden_answer = True
    >>> ).display()
    >>> print("The secret message was", response[1])
    The secret message was 42



Menus
-----

    >>> import PyXA
    >>> response = PyXA.XAMenu(
    >>>     menu_items = ['Option 1', 'Option 2', 'Option 3'],
    >>>     title = "Select Item",
    >>>     prompt = "Select an item",
    >>>     default_items = ['Option 2'],
    >>>     ok_button_name = "Okay",
    >>>     cancel_button_name = "Cancel",
    >>>     multiple_selections_allowed = False,
    >>>     empty_selection_allowed = False
    >>> ).display()
    >>> print(response)
    Option 2


File and Folder Pickers
-----------------------

    >>> import PyXA
    >>> response = PyXA.XAFilePicker(
    >>>     prompt = "Choose File",
    >>>     types = ["png"],
    >>>     default_location = "/",
    >>>     show_invisibles = False,
    >>>     multiple_selections_allowed = False,
    >>>     show_package_contents = False
    >>> ).display()
    >>> print(response)
    <<class 'PyXA.XABase.XAPath'>file:///Users/ExampleUser/Desktop/Example.png>


    >>> import PyXA
    >>> response = PyXA.XAFolderPicker(
    >>>     prompt = "Choose Folder",
    >>>     default_location = "/",
    >>>     show_invisibles = False,
    >>>     multiple_selections_allowed = True,
    >>>     show_package_contents = False
    >>> ).display()
    >>> print(response)
    [<<class 'PyXA.XABase.XAPath'>file:///Applications/>, <<class 'PyXA.XABase.XAPath'>file:///Library/>]


File Name Dialogs
-----------------

    >>> import PyXA
    >>> response = PyXA.XAFileNameDialog(
    >>>     prompt = "Choose Folder",
    >>>     default_name = "New File",
    >>>     default_location = "/Users/Shared",
    >>> ).display()
    >>> print(response)
    <<class 'PyXA.XABase.XAPath'>file:///Users/Shared/New%20File>


Color Pickers
-------------

    >>> import PyXA
    >>> response = PyXA.XAColorPicker(
    >>>     style = PyXA.XAColorPickerStyle.CRAYONS
    >>> ).display()
    >>> print(response)
    <<class 'PyXA.XABase.XAColor'>r=1.0, g=0.8323456645, b=0.4732058644, a=1.0>