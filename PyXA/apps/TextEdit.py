""".. versionadded:: 0.0.1

Control the macOS TextEdit application using JXA-like syntax.
"""

from typing import List, Union
from AppKit import NSFileManager, NSURL

from PyXA import XABase
from PyXA import XABaseScriptable

_YES = 2036691744
_NO = 1852776480
_ASK = 1634954016
_STANDARD_ERRORS = 1819767668
_DETAILED_ERRORS = 1819763828

class XATextEditApplication(XABaseScriptable.XASBApplication, XABase.XACanConstructElement, XABase.XAAcceptsPushedElements, XABase.XACanOpenPath):
    """A class for managing and interacting with TextEdit.app.

     .. seealso:: :class:`XATextEditWindow`, :class:`XATextEditDocument`

    .. versionadded:: 0.0.1
    """
    def __init__(self, properties):
        super().__init__(properties)
        self.xa_wcls = XATextEditWindow

    def print(self, path: Union[str, NSURL], show_prompt: bool = True):
        if isinstance(path, str):
            path = NSURL.alloc().initFileURLWithPath_(path)
        self.xa_scel.print_printDialog_withProperties_(path, show_prompt, None)

    # Documents
    def documents(self, filter: dict = None) -> List['XATextEditDocument']:
        """Returns a list of documents matching the filter.

        :param filter: A dictionary specifying property-value pairs that all returned documents will have
        :type filter: dict
        :return: The list of documents
        :rtype: List[XATextEditDocument]

        :Example 1: Listing all documents

        >>> import PyXA
        >>> app = PyXA.application("TextEdit")
        >>> print(app.documents())
        [<<class 'PyXA.apps.TextEdit.XATextEditDocument'>Current Document>, <<class 'PyXA.apps.TextEdit.XATextEditDocument'>Another Document>, ...]

        :Example 2: List documents after applying a filter

        >>> import PyXA
        >>> app = PyXA.application("TextEdit")
        >>> print(app.documents({"name": "Another Document"}))
        [<<class 'PyXA.apps.TextEdit.XATextEditDocument'>Another Document>]

        .. versionadded:: 0.0.1
        """
        return self.scriptable_elements("documents", filter, XATextEditDocument)

    def document(self, filter: Union[int, dict]) -> 'XATextEditDocument':
        """Returns the first document that matches the filter.

        :param filter: Either an array index or a dictionary specifying property-value pairs that the returned document will have
        :type filter: Union[int, dict]
        :return: The first matching document
        :rtype: XATextEditDocument

        :Example 1: Get a document by index

        >>> import PyXA
        >>> app = PyXA.application("TextEdit")
        >>> print(app.document(0))
        <<class 'PyXA.apps.TextEdit.XATextEditDocument'>Current Document>

        :Example 2: Get a document by applying a filter

        >>> import PyXA
        >>> app = PyXA.application("TextEdit")
        >>> print(app.document({"name": "Another Document"}))
        <<class 'PyXA.apps.TextEdit.XATextEditDocument'>Another Document>

        .. versionadded:: 0.0.1
        """
        return self.scriptable_element_with_properties("documents", filter, XATextEditDocument)

    def first_document(self) -> 'XATextEditDocument':
        """Returns the document at the first index of the documents array.

        .. versionadded:: 0.0.1
        """
        return self.first_scriptable_element("documents", XATextEditDocument)

    def last_document(self) -> 'XATextEditDocument':
        """Returns the document at the last (-1) index of the documents array.

        .. versionadded:: 0.0.1
        """
        return self.last_scriptable_element("documents", XATextEditDocument)

    def new_document(self, name: Union[str, None] = "Untitled.txt", text: Union[str, None] = "", location: Union[str, None] = None) -> 'XATextEditDocument':
        """Creates a new document with the given name and initializes it with the supplied text. If no location is provided, the document file is created in the user's Documents folder.

        :param name: The name (including file extension) of the document, defaults to "Untitled.txt"
        :type name: Union[str, None], optional
        :param text: The initial text of the document, defaults to ""
        :type text: Union[str, None], optional
        :param location: The containing folder of the new document, defaults to None.
        :type location: Union[str, None]
        :return: A reference to the newly created document.
        :rtype: XATextEditDocument

        :Example:

        >>> import PyXA
        >>> app = PyXA.application("TextEdit")
        >>> doc = app.new_document("New.txt", "Example text")
        >>> print(doc.properties)
        {
            modified = 0;
            name = "New.txt";
            objectClass = "<NSAppleEventDescriptor: 'docu'>";
            path = "/Users/exampleuser/Documents/New.txt";
            text = "Example text";
        }

        .. seealso:: :class:`XATextEditDocument`

        .. versionadded:: 0.0.1
        """
        if location is None:
            location = NSFileManager.alloc().homeDirectoryForCurrentUser().relativePath() + "/Documents/" + name
        else:
            location = location + name
        return self.push("document", {"name": name, "text": text, "path": location}, self.xa_scel.documents(), XATextEditDocument)

class XATextEditWindow(XABaseScriptable.XASBPrintable):
    """A class for managing and interacting with TextEdit windows.

    .. seealso:: :class:`XATextEditApplication`

    .. versionadded:: 0.0.1
    """
    def __init__(self, properties):
        super().__init__(properties)
        self.document = self._new_element(self.document, XATextEditDocument)

class XATextEditDocument(XABase.XACanConstructElement, XABase.XAAcceptsPushedElements, XABase.XATextDocument, XABaseScriptable.XASBPrintable):
    """A class for managing and interacting with TextEdit documents.

    .. seealso:: :class:`XATextEditApplication`

    .. versionchanged:: 0.0.2

       Added :func:`close`, :func:`save`, and :func:`copy`

    .. versionadded:: 0.0.1
    """
    def __init__(self, properties):
        super().__init__(properties)
        self.path = self.xa_elem.path() #: The path at which the document is stored
        self.name = self.xa_elem.name() #: The name of the document, including the file extension
        self.modified #: Whether the document has been modified since the last save

    def close(self):
        """Closes the document.

        .. versionadded:: 0.0.2
        """
        self.xa_elem.delete()

    def save(self, file_path: str = None):
        """Saves the document.

        If a file path is provided, TextEdit will attempt to create a new file at the target location and of the specified file extension. If no file path is provided, a save dialog for the document will open.

        :param file_path: The path to save the document at, defaults to None
        :type file_path: str, optional

        .. versionadded:: 0.0.2
        """
        if file_path is not None:
            url = NSURL.alloc().initFileURLWithPath_(file_path)
            self.xa_elem.saveAs_in_(None, url)
        else:
            self.xa_elem.saveAs_in_(None, None)

    def copy(self):
        """Copies the document file and its contents to the clipboard.

        .. versionadded:: 0.0.2
        """
        url =  NSURL.alloc().initFileURLWithPath_(self.path)
        self.set_clipboard([self.text, url])

    @property
    def modified(self):
        return self.xa_elem.modified()

    def __repr__(self):
        return "<" + str(type(self)) + self.name + ">"