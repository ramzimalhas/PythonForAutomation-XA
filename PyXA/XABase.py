""".. versionadded:: 0.0.1

General classes and methods applicable to any PyXA object.
"""

import time
from typing import Any, Union, List, Dict
import threading

import AppKit
from ScriptingBridge import SBApplication, SBElementArray
from Foundation import NSURL, NSString

class XAObject():
    """A general class for PyXA scripting objects.

    .. seealso:: :class:`XASBObject`

    .. versionadded:: 0.0.1
    """
    def __init__(self, properties: dict = None):
        """Instantiates a PyXA scripting object.

        :param properties: A dictionary of properties to assign to this object.
        :type properties: dict, optional

        .. versionadded:: 0.0.1
        """
        self.xa_prnt = properties.get("parent", None)
        self.xa_apsp = properties.get("appspace", None)
        self.xa_wksp = properties.get("workspace", None)
        self.xa_elem = properties.get("element", None)
        self.xa_scel = properties.get("scriptable_element", None)
        self.xa_aref = properties.get("appref", None)
        self.xa_sevt = properties.get("system_events", SBApplication.alloc().initWithBundleIdentifier_("com.apple.systemevents"))
        
        try:
            self.element_properties = properties["element"].properties()
        except:
            self.element_properties = None

        if self.element_properties is not None:
            for attr in self.element_properties:
                try:
                    if not hasattr(self, attr):
                        self.__setattr__(attr, self.element_properties[attr])
                except:
                    pass

    def _new_element(self, obj: AppKit.NSObject, obj_class: type = 'XAObject') -> 'XAObject':
        """Wrapper for creating a new PyXA object.

        :param folder_obj: The Objective-C representation of an object.
        :type folder_obj: NSObject
        :return: The PyXA representation of the object.
        :rtype: XAObject
        
        .. versionadded:: 0.0.1
        """
        properties = {
            "parent": self,
            "appspace": self.xa_apsp,
            "workspace": self.xa_wksp,
            "element": obj,
            "appref": self.xa_aref,
            "system_events": self.xa_sevt,
        }
        return obj_class(properties)

    def has_element(self) -> bool:
        """Whether this object has an AppleScript/JXA/Objective-C scripting element associated with it.

        :return: True if this object's element attribute is set, False otherwise.
        :rtype: bool

        .. versionadded:: 0.0.1
        """
        return self.xa_elem is not None

    def has_element_properties(self) -> bool:
        """Whether the scripting element associated with this object has properties attached to it.

        :return: True if this object's properties attribute is set, False otherwise.
        :rtype: bool

        .. versionadded:: 0.0.1
        """
        return self.element_properties != None

    def set_element(self, element: 'XAObject') -> 'XAObject':
        """Sets the element attribute to the supplied element and updates the properties attribute accordingly.

        :param element: The new scripting element to reference via the element attribute.
        :type element: XAObject
        :return: A reference to this PyXA object.
        :rtype: XAObject

        .. versionadded:: 0.0.1
        """
        self.xa_elem = element
        self.element_properties = element.properties()
        return self

    def set_properties(self, properties: dict) -> 'XAObject':
        """Updates the value of multiple properties of the scripting element associated with this object.

        :param properties: A dictionary defining zero or more property names and updated values as key-value pairs.
        :type properties: dict
        :return: A reference to this PyXA object.
        :rtype: XAObject

        .. versionadded:: 0.0.1
        """
        self.xa_elem.setValuesForKeysWithDictionary_(properties)
        return self

    def set_property(self, property_name: str, value: Any) -> 'XAObject':
        """Updates the value of a single property of the scripting element associated with this object.

        :param property: The name of the property to assign a new value to.
        :type property: str
        :param value: The value to assign to the specified property.
        :type value: Any
        :return: A reference to this PyXA object.
        :rtype: XAObject

        .. versionadded:: 0.0.1
        """
        self.xa_elem._scriptingSetValue_forKey_(value, property_name)
        self.__setattr__(property_name, value)
        return self

    def set_clipboard(self, content: Any) -> None:
        """Sets the clipboard to the specified content.

        :param content: The item or object to set the clipboard to. Can be a list of items.
        :type content: Any

        .. seealso:: :func:`get_clipboard`, :func:`get_clipboard_strings`

        .. versionadded:: 0.0.1
        """
        pb = AppKit.NSPasteboard.generalPasteboard()
        pb.clearContents()
        pb.writeObjects_(AppKit.NSArray.arrayWithObject_(content))

### Mixins
## Action Mixins
class XACanPrintPath(XAObject):
    """A class for scriptable objects that can print the file at a given path.
    """
    def print(self, target: Union[str, NSURL]) -> XAObject:
        """pens the file/website at the given filepath/URL.

        :param target: The path to a file or the URL to a website to print.
        :type target: Union[str, NSURL]
        :return: A reference to the PyXA object that called this method.
        :rtype: XAObject

        .. note::
        
            The implementation of a printing method various across applications, and some do not have the same method signature. If this presents a problem for a specific application, a custom print method should be defined for that application class.

        .. versionadded:: 0.0.1
        """
        if not isinstance(target, NSURL):
            target = xa_path(target)
        self.xa_elem.print(target)
        return self

class XACanOpenPath(XAObject):
    """A class for scriptable objects that can open an item at a given path (either in its default application or in an application whose PyXA object extends this class).
    
    .. seealso:: :class:`XABaseScriptable.XASBPrintable`

    .. versionadded:: 0.0.1
    """
    def open(self, target: Union[str, NSURL]) -> XAObject:
        """Opens the file/website at the given filepath/URL.

        :param target: The path to a file or the URL to a website to open.
        :type target: Union[str, NSURL]
        :return: A reference to the PyXA object that called this method.
        :rtype: XAObject

        .. versionadded:: 0.0.1
        """
        url = target
        if not isinstance(url, NSURL):
            url = xa_url(target)
        if target.startswith("/"):
            url = NSURL.alloc().initFileURLWithPath_(target)
        self.wksp.openURLs_withAppBundleIdentifier_options_additionalEventParamDescriptor_launchIdentifiers_([url], self.xa_elem.bundleIdentifier(), 0, None, None)
        return self

class XAAcceptsPushedElements(XAObject):
    """A class for scriptable objects that either have lists or are themselves lists that other scriptable objects can be pushed onto.

    .. versionadded:: 0.0.1
    """
    def push(self, element_specifier: Union[str, AppKit.NSObject], properties: dict, location: SBElementArray, object_class = XAObject) -> XAObject:
        """Appends the supplied element or an element created from the supplied specifier and properties to the scriptable object list at the specified location.

        :param element_specifier: Either the scripting class to create a new object of or an existing instance of a scripting class.
        :type element_specifier: Union[str, NSObject]
        :param properties: _description_
        :type properties: dict
        :param location: _description_
        :type location: SBElementArray'
        :param object_class: The PyXA class to wrap the newly created object in, defaults to XAObject
        ;type object_class: type
        :return: A reference to the new created PyXA object.
        :rtype: XAObject

        .. versionadded:: 0.0.1
        """
        if isinstance(element_specifier, str):
            element_specifier = self.construct(element_specifier, properties)
        location.addObject_(element_specifier)
        properties = {
            "parent": self,
            "appspace": self.xa_apsp,
            "workspace": self.xa_wksp,
            "element": element_specifier,
            "appref": self.xa_aref,
            "system_events": self.xa_sevt,
        }
        return object_class(properties)


class XACanConstructElement(XAObject):
    """A class for scriptable objects that are able to create new scriptable objects.

    .. versionadded:: 0.0.1
    """
    def construct(self, specifier: str, properties: dict) -> AppKit.NSObject:
        """Initializes a new NSObject of the given specifier class with the supplied dictionary of properties.

        :param specifier: The scripting class to create a new object of.
        :type specifier: str
        :param properties: A dictionary of property names and values appropriate for the specified scripting class.
        :type properties: dict
        :return: A reference to the newly created NSObject.
        :rtype: NSObject

        .. versionadded:: 0.0.1
        """
        if self.scel is not None:
            return self.xa_scel.classForScriptingClass_(specifier).alloc().initWithProperties_(properties)
        return self.xa_elem.classForScriptingClass_(specifier).alloc().initWithProperties_(properties)
        
## Relation Mixins
class XAHasElements(XAObject):
    def elements(self, specifier, filter, obj_type):
        ls = self.xa_elem.__getattribute__(specifier)()
        if filter is not None:
            predicate = AppKit.NSPredicate.predicateWithFormat_(xa_predicate_format(filter))
            ls = ls.filteredArrayUsingPredicate_(predicate)

        elements = []
        for element in ls:
            properties = {
                "parent": self,
                "appspace": self.xa_apsp,
                "workspace": self.xa_wksp,
                "element": element,
                "appref": self.xa_aref,
                "system_events": self.xa_sevt,
            }
            elements.append(obj_type(properties))
        return elements

    def element_with_properties(self, specifier, filter, obj_type):
        if isinstance(filter, int):
            element = self.xa_elem.__getattribute__(specifier)()[filter]
            properties = {
                "parent": self,
                "appspace": self.xa_apsp,
                "workspace": self.xa_wksp,
                "element": element,
                "appref": self.xa_aref,
                "system_events": self.xa_sevt,
            }
            return obj_type(properties)
        return self.elements(specifier, filter, obj_type)[0]

    def first_element(self, specifier, obj_type):
        element = self.xa_elem.__getattribute__(specifier)()[0]
        properties = {
            "parent": self,
            "appspace": self.xa_apsp,
            "workspace": self.xa_wksp,
            "element": element,
            "appref": self.xa_aref,
            "system_events": self.xa_sevt,
        }
        return obj_type(properties)

    def last_element(self, specifier, obj_type):
        element = self.xa_elem.__getattribute__(specifier)()[-1]
        properties = {
            "parent": self,
            "appspace": self.xa_apsp,
            "workspace": self.xa_wksp,
            "element": element,
            "appref": self.xa_aref,
            "system_events": self.xa_sevt,
        }
        return obj_type(properties)

## Property Mixins
# class XASBCloseSavePrintable(XAObject):
#     def close(self) -> XAObject:
#         """Closes a document, window, or item.

#         :return: A reference to the PyXA object that called this method.
#         :rtype: XAObject
#         """
#         self.element.close()
#         return self

#     def save(self, location: str = "~/Documents") -> XAObject:
#         """Saves a document, window, or item.

#         :return: A reference to the PyXA object that called this method.
#         :rtype: XAObject
#         """
#         self.element.saveIn_(location)
#         return self

#     def print(self, properties: dict = None, print_dialog = None) -> XAObject:
#         """Prints a document, window, or item.

#         :return: A reference to the PyXA object that called this method.
#         :rtype: XAObject
#         """
#         self.element.printWithProperties_printDialog_(properties, None)
#         return self


class XAShowable(XAObject):
    def show(self) -> XAObject:
        """Shows a document, window, or item.

        :return: A reference to the PyXA object that called this method.
        :rtype: XAObject

        .. versionadded:: 0.0.1
        """
        self.xa_elem.show()


class XARevealable(XAObject):
    def reveal(self) -> XAObject:
        """Reveals a document, window, or item, selecting it from a list of other items.

        :return: A reference to the PyXA object that called this method.
        :rtype: XAObject

        .. versionadded:: 0.0.1
        """
        self.xa_elem.reveal()

class XASelectable(XAObject):
    def select(self) -> XAObject:
        """Selects a document or item. This may open a new window, depending on which kind of object and application it acts on.

        :return: A reference to the PyXA object that called this method.
        :rtype: XAObject

        .. versionadded:: 0.0.1
        """
        self.xa_elem.select()

class XADeletable(XAObject):
    def delete(self) -> XAObject:
        """Deletes a document or item.

        :return: A reference to the PyXA object that called this method.
        :rtype: XAObject

        .. versionadded:: 0.0.1
        """
        deletion_thread = threading.Thread(target=self.xa_elem.delete, name="Delete", daemon=True)
        deletion_thread.start()

### Elements
class XAProcess(XAHasElements):
    def __init__(self, properties):
        super().__init__(properties)
        self.wcls = properties["window_class"]

    def windows(self, filter: dict = None) -> List['XAWindow']:
        return super().elements("windows", filter, self.xa_wcls)

    def window(self, filter: Union[int, dict]) -> 'XAWindow':
        return super().element("windows", filter, self.xa_wcls)

    def front_window(self) -> 'XAWindow':
        return super().first_element("windows", self.xa_wcls)

class XAApplication(XAObject):
    """A general application class for both officially scriptable and non-scriptable applications.

    .. seealso:: :class:`XASBApplication`, :class:`XAWindow`

    .. versionadded:: 0.0.1
    """
    def __init__(self, properties):
        super().__init__(properties)
        self.xa_wcls = XAWindow

        properties = {"name": self.xa_elem.localizedName()}
        predicate = AppKit.NSPredicate.predicateWithFormat_(xa_predicate_format(properties))
        process = self.xa_sevt.processes().filteredArrayUsingPredicate_(predicate)[0]

        properties = {
            "parent": self,
            "appspace": self.xa_apsp,
            "workspace": self.xa_wksp,
            "element": process,
            "appref": self.xa_aref,
            "system_events": self.xa_sevt,
            "window_class": self.xa_wcls
        }
        self.xa_prcs = XAProcess(properties)

    def activate(self) -> 'XAApplication':
        """Activates the application, bringing its window(s) to the front and launching the application beforehand if necessary.

        :return: A reference to the PyXA application object.
        :rtype: XAApplication

        .. seealso:: :func:`terminate`, :func:`unhide`, :func:`focus`

        .. versionadded:: 0.0.1
        """
        self.xa_elem.activateWithOptions_(AppKit.NSApplicationActivateIgnoringOtherApps)
        return self

    def terminate(self) -> 'XAApplication':
        """Quits the application. Synonymous with quit().

        :return: A reference to the PyXA application object.
        :rtype: XAApplication

        :Example:

        >>> import PyXA
        >>> safari = PyXA.application("Safari")
        >>> safari.terminate()

        .. seealso:: :func:`quit`, :func:`activate`

        .. versionadded:: 0.0.1
        """
        self.xa_elem.terminate()
        return self

    def quit(self) -> 'XAApplication':
        """Quits the application. Synonymous with terminate().

        :return: A reference to the PyXA application object.
        :rtype: XAApplication

        :Example:

        >>> import PyXA
        >>> safari = PyXA.application("Safari")
        >>> safari.quit()

        .. seealso:: :func:`terminate`, :func:`activate`

        .. versionadded:: 0.0.1
        """
        self.xa_elem.terminate()
        return self

    def hide(self) -> 'XAApplication':
        """Hides all windows of the application.

        :return: A reference to the PyXA application object.
        :rtype: XAApplication

        :Example:

        >>> import PyXA
        >>> safari = PyXA.application("Safari")
        >>> safari.hide()

        .. seealso:: :func:`unhide`

        .. versionadded:: 0.0.1
        """
        self.xa_elem.hide()
        return self

    def unhide(self) -> 'XAApplication':
        """Unhides (reveals) all windows of the application, but does not does not activate them.

        :return: A reference to the PyXA application object.
        :rtype: XAApplication

        :Example:

        >>> import PyXA
        >>> safari = PyXA.application("Safari")
        >>> safari.unhide()

        .. seealso:: :func:`hide`

        .. versionadded:: 0.0.1
        """
        self.xa_elem.unhide()
        return self

    def focus(self) -> 'XAApplication':
        """Hides the windows of all applications except this one.

        :return: A reference to the PyXA application object.
        :rtype: XAApplication

        :Example:

        >>> import PyXA
        >>> safari = PyXA.application("Safari")
        >>> safari.focus()

        .. seealso:: :func:`unfocus`

        .. versionadded:: 0.0.1
        """
        for app in self.xa_wksp.runningApplications():
            if app.localizedName() != self.xa_elem.localizedName():
                app.hide()
            else:
                app.unhide()
        return self

    def unfocus(self) -> 'XAApplication':
        """Unhides (reveals) the windows of all other applications, but does not activate them.

        :return: A reference to the PyXA application object.
        :rtype: XAApplication

        :Example:

        >>> import PyXA
        >>> safari = PyXA.application("Safari")
        >>> safari.unfocus()

        .. seealso:: :func:`focus`

        .. versionadded:: 0.0.1
        """
        for app in self.xa_wksp.runningApplications():
                app.unhide()
        return self

    def _get_processes(self, processes):
        for process in self.xa_sevt.processes():
            processes.append(process)

    # Windows
    def windows(self, filter: dict = None) -> List['XAWindow']:
        return self.xa_prcs.windows(filter)

    def window(self, filter: Union[int, dict]) -> 'XAWindow':
        return self.xa_prcs.window(filter)

    def front_window(self) -> 'XAWindow':
        return self.xa_prcs.front_window()

    # def windows(self) -> List['XAWindow']:
    #     # properties = {"name": self.xa_elem.localizedName()}
    #     # predicate = NSPredicate.predicateWithFormat_(xa_predicate_format(properties))
    #     # process = self.system_events.processes().filteredArrayUsingPredicate_(predicate)[0]

    #     # windows = []
    #     # for window in process.windows():
    #     #     windows.append(XAWindow(self, self.appspace, self.workspace, window, self.appref, self.system_events))
    #     # return windows

    #     # print(elements)
    #     # return elements
    #     # windowList = CGWindowListCopyWindowInfo(kCGWindowListOptionOnScreenOnly, kCGNullWindowID)
    #     # print(windowList)
    #     # windows = []
    #     # for window in windowList:
    #     #     if window["kCGWindowOwnerName"] == self.xa_elem.localizedName():
    #     #         windows.append(XAWindow(self, self.appspace, self.workspace, self.name, window, self.appref))
    #     # return windows

class XASound(XAObject):
    """A wrapper class for NSSound objects and associated methods.

    .. versionadded:: 0.0.1
    """
    def __init__(self, sound_file: Union[str, NSURL]):
        if isinstance(sound_file, str):
            if "/" in sound_file:
                sound_file = NSURL.alloc().initWithString_(sound_file)
            else:
                sound_file = NSURL.alloc().initWithString_("/System/Library/Sounds/" + sound_file + ".aiff")
        self.sound = AppKit.NSSound.alloc()
        self.sound.initWithContentsOfURL_byReference_(sound_file, True)

    def play(self) -> 'XASound':
        """Plays the sound from the beginning.

        :return: A reference to this sound object.
        :rtype: XASound

        :Example:

        >>> import PyXA
        >>> glass_sound = PyXA.sound("Glass")
        >>> glass_sound.play()

        .. seealso:: :func:`pause`, :func:`stop`

        .. versionadded:: 0.0.1
        """
        self.sound.stop()
        self.sound.play()
        time.sleep(self.sound.duration())
        return self

    def pause(self) -> 'XASound':
        """Pauses the sound.

        :return: A reference to this sound object.
        :rtype: XASound

        :Example:

        >>> import PyXA
        >>> glass_sound = PyXA.sound("Glass")
        >>> glass_sound.pause()

        .. seealso:: :func:`resume`, :func:`stop`

        .. versionadded:: 0.0.1
        """
        self.sound.pause()
        return self

    def resume(self) -> 'XASound':
        """Plays the sound starting from the time it was last paused at.

        :return: A reference to this sound object.
        :rtype: XASound

        :Example:

        >>> import PyXA
        >>> glass_sound = PyXA.sound("Glass")
        >>> glass_sound.resume()

        .. seealso:: :func:`pause`, :func:`play`

        .. versionadded:: 0.0.1
        """
        self.sound.resume()
        return self

    def stop(self) -> 'XASound':
        """Stops playback of the sound and rewinds it to the beginning.

        :return: A reference to this sound object.
        :rtype: XASound

        :Example:

        >>> import PyXA
        >>> glass_sound = PyXA.sound("Glass")
        >>> glass_sound.stop()

        .. seealso:: :func:`pause`, :func:`play`

        .. versionadded:: 0.0.1
        """
        self.sound.stop()
        return self

    def set_volume(self, volume: int) -> 'XASound':
        """Sets the volume of the sound.

        :param volume: The desired volume of the sound in the range [0.0, 1.0].
        :type volume: int
        :return: A reference to this sound object.
        :rtype: XASound

        :Example:

        >>> import PyXA
        >>> glass_sound = PyXA.sound("Glass")
        >>> glass_sound.set_volume(1.0)

        .. seealso:: :func:`volume`

        .. versionadded:: 0.0.1
        """
        self.sound.setVolume_(volume)
        return self

    def volume(self) -> float:
        """Returns the current volume of the sound.

        :return: The volume level of the sound.
        :rtype: int

        :Example:

        >>> import PyXA
        >>> glass_sound = PyXA.sound("Glass")
        >>> print(glass_sound.volume())
        1.0

        .. seealso:: :func:`set_volume`

        .. versionadded:: 0.0.1
        """
        return self.sound.volume()

    def loop(self, times: int) -> 'XASound':
        """Plays the sound the specified number of times.

        :param times: The number of times to loop the sound.
        :type times: int
        :return: A reference to this sound object.
        :rtype: XASound

        :Example:

        >>> import PyXA
        >>> glass_sound = PyXA.sound("Glass")
        >>> glass_sound.loop(10)

        .. versionadded:: 0.0.1
        """
        self.sound.setLoops_(times)
        self.sound.play()
        time.sleep(self.sound.duration() * times)
        self.sound.stop()
        self.sound.setLoops_(0)
        return self


def xa_url(url: str) -> NSURL:
    """Converts a string-type filepath/URL into an NSURL object. Synonymous with xa_path().

    :param url: The filepath or URL to convert.
    :type url: str
    :return: The NSURL form of the supplied filepath/URL.
    :rtype: NSURL

    :Example:

    >>> from XABase import xa_url
    >>> url = xa_url("https://www.google.com")
    >>> print(type(url))
    # TODO: This

    .. seealso:: :func:`xa_path`

    .. versionadded:: 0.0.1
    """
    return NSURL.alloc().initWithString_(url)

def xa_path(filepath: str):
    """Converts a string-type filepath/URL into an NSURL object. Synonymous with xa_url().

    :param url: The filepath or URL to convert.
    :type url: str
    :return: The NSURL form of the supplied filepath/URL.
    :rtype: NSURL

    .. versionadded:: 0.0.1
    """
    return NSURL.alloc().initWithString_(filepath)

def xa_predicate_format(ref_dict: dict):
    """Constructs a predicate format string from the keys and values of the supplied reference dictionary.add()

    Predicate format strings are of the form "(key1 = 'value1') && (key2 = 'value2')..."

    :param ref_dict: The dictionary to construct a predicate format string from.
    :type ref_dict: dict
    :return: The resulting predicate format string.
    :rtype: str

    .. versionadded:: 0.0.1
    """
    predicate_format = ""
    for key, value in ref_dict.items():
        if isinstance(value, list) or isinstance(value, tuple):
            if value[0] == ">":
                predicate_format += f"({key} > {value[1]}) &&"
            elif value[0] == "<":
                predicate_format += f"({key} < {value[1]}) &&"
            elif value[0] == "!":
                predicate_format += f"({key} != {value[1]}) &&"
            elif value[0].lower() == "contains":
                predicate_format += f"({key} CONTAINS '{value[1]}') &&"
            elif value[0].lower() == "like":
                predicate_format += f"({key} LIKE '{value[1]}') &&"
            elif value[0].lower() == "matches":
                predicate_format += f"({key} MATCHES '{value[1]}') &&"
            elif value[0].lower() == "beginswith":
                predicate_format += f"({key} BEGINSWITH '{value[1]}') &&"
            elif value[0].lower() == "endswith":
                predicate_format += f"({key} ENDSWITH '{value[1]}') &&"
        else:
            value = value.replace("'", "\\'")
            predicate_format += f"({key} = '{value}') &&"
    return predicate_format[:-3]

### UI Components
class XAUIElement(XAHasElements):
    def __init__(self, properties):
        super().__init__(properties)
        self.xa_scut = {}

    def entire_contents(self) -> 'XAUIElement':
        print(self.xa_elem.entireContents())
        return self

    def all(self, specifier, in_class = "groups", force_update = False):
        if (specifier, in_class) in self.xa_scut and not force_update:
            return self.xa_scut[(specifier, in_class)]

        valid_specifiers = {
            "windows": XAWindow,
            "buttons": XAButton,
            "actions": XAUIAction,
        }
        target_class = valid_specifiers[specifier]

        target_objects = []
        sub_objects = self.__getattribute__(in_class)()
        for item in sub_objects:
            target_objects.extend(item.all(specifier, in_class))

        if isinstance(self, target_class):
            target_objects.append(self)
        else:
            target_objects.extend(self.__getattribute__(specifier)())

        self.xa_scut[(specifier, in_class)] = target_objects
        return target_objects

    ## Windows
    def windows(self, filter: dict = None) -> List['XAWindow']:
        return self.elements("windows", filter, XAWindow)

    def window(self, filter: Union[int, dict]) -> 'XAWindow':
        return self.element_with_properties("windows", filter, XAWindow)

    def first_window(self) -> 'XAWindow':
        return self.first_element("windows", XAWindow)

    def last_window(self) -> 'XAWindow':
        return self.last_element("windows", XAWindow)

    # Buttons
    def buttons(self, filter: dict = None) -> List['XAButton']:
        return self.elements("buttons", filter, XAButton)

    def button(self, filter: Union[int, dict]) -> 'XAButton':
        return self.element_with_properties("buttons", filter, XAButton)

    def first_button(self) -> 'XAButton':
        return self.first_element("buttons", XAButton)

    def last_button(self) -> 'XAButton':
        return self.last_element("buttons", XAButton)

    # Actions
    def actions(self, filter: dict = None) -> List['XAUIAction']:
        return self.elements("actions", filter, XAUIAction)

    def action(self, filter: Union[int, dict]) -> 'XAUIAction':
        return self.element_with_properties("actions", filter, XAUIAction)

    def first_action(self) -> 'XAUIAction':
        return self.first_element("actions", XAUIAction)

    def last_action(self) -> 'XAUIAction':
        return self.last_element("actions", XAUIAction)

class XAWindow(XAUIElement):
    """A general window class for windows of both officially scriptable and non-scriptable applications.

    .. seealso:: :class:`XAApplication`, :class:`XASBWindow`

    .. versionadded:: 0.0.1
    """
    def __init__(self, properties):
        super().__init__(properties)

    # Actions
    def close(self) -> 'XAWindow':
        """Collapses (minimizes) the window.

        :return: A reference to the now-collapsed window object.
        :rtype: XAWindow

        .. versionadded:: 0.0.1
        """
        close_button = self.button({"subrole": "AXCloseButton"})
        close_button.click()
        return self

    def collapse(self) -> 'XAWindow':
        """Collapses (minimizes) the window.

        :return: A reference to the now-collapsed window object.
        :rtype: XAWindow

        .. versionadded:: 0.0.1
        """
        if hasattr(self.xa_elem.properties(), "miniaturized"):
            self.xa_elem._setValue_forKey_(True, "miniaturized")
        else:
            close_button = self.button({"subrole": "AXMinimizeButton"})
            close_button.click()
        return self

    def uncollapse(self) -> 'XAWindow':
        """Uncollapses (unminimizes/expands) the window.

        :return: A reference to the uncollapsed window object.
        :rtype: XAWindow

        .. versionadded:: 0.0.1
        """
        process_predicate = AppKit.NSPredicate.predicateWithFormat_(xa_predicate_format({"name": "Dock"}))
        dock_process = self.xa_sevt.applicationProcesses().filteredArrayUsingPredicate_(process_predicate)[0]

        app_predicate = AppKit.NSPredicate.predicateWithFormat_(xa_predicate_format({"name": self.xa_prnt.xa_prnt.element.localizedName()}))
        app_icon = dock_process.lists()[0].UIElements().filteredArrayUsingPredicate_(app_predicate)[0]
        app_icon.actions()[0].perform()
        return self

class XAButton(XAUIElement):
    def __init__(self, properties):
        super().__init__(properties)

    def click(self):
        self.action({"name": "AXPress"}).perform()
        return self

    def press(self):
        self.actions({"name": "AXPress"}).perform()
        return self

    def option_click(self):
        self.actions({"name": "AXZoomWindow"}).perform()
        return self

    def show_menu(self):
        self.actions({"name": "AXShowMenu"}).perform()
        return self

class XAUIAction(XAUIElement):
    def __init__(self, properties):
        super().__init__(properties)

    def perform(self):
        self.xa_elem.perform()
        return self

# Text Elements
class XAHasParagraphs(XAHasElements):
    """A generic class for objects that have paragraphs.

    .. versionadded:: 0.0.1
    """
    def paragraphs(self, filter: dict = None) -> List['XAParagraph']:
        """Returns a list of paragraphs matching the filter.

        .. seealso:: :func:`elements`

        .. versionadded:: 0.0.1
        """
        return self.elements("paragraphs", filter, XAParagraph)

    def paragraph(self, filter: Union[int, dict]) -> 'XAParagraph':
        """Returns the first paragraph that matches the filter.

        .. seealso:: :func:`element_with_properties`

        .. versionadded:: 0.0.1
        """
        return self.element_with_properties("paragraphs", filter, XAParagraph)

    def first_paragraph(self) -> 'XAParagraph':
        """Returns the paragraph at the first index of the paragraphs array.

        .. seealso:: :func:`first_element`

        .. versionadded:: 0.0.1
        """
        return self.first_element("paragraphs", XAParagraph)

    def last_paragraph(self) -> 'XAParagraph':
        """Returns the paragraph at the last (-1) index of the paragraphs array.

        .. seealso:: :func:`last_element`

        .. versionadded:: 0.0.1
        """
        return self.last_element("paragraphs", XAParagraph)


class XAHasWords(XAHasElements):
    """A generic class for objects that have words.

    .. versionadded:: 0.0.1
    """
    def words(self, filter: dict = None) -> List['XAWord']:
        """Returns a list of words matching the filter.

        .. seealso:: :func:`elements`

        .. versionadded:: 0.0.1
        """
        return self.elements("words", filter, XAWord)

    def word(self, filter: Union[int, dict]) -> 'XAWord':
        """Returns the first word that matches the filter.

        .. seealso:: :func:`element_with_properties`

        .. versionadded:: 0.0.1
        """
        return self.element_with_properties("words", filter, XAWord)

    def first_word(self) -> 'XAWord':
        """Returns the word at the first index of the words array.

        .. seealso:: :func:`first_element`

        .. versionadded:: 0.0.1
        """
        return self.first_element("words", XAWord)

    def last_word(self) -> 'XAWord':
        """Returns the word at the last (-1) index of the words array.

        .. seealso:: :func:`last_element`

        .. versionadded:: 0.0.1
        """
        return self.last_element("words", XAWord)


class XAHasCharacters(XAHasElements):
    """A generic class for objects that have text characters.

    .. versionadded:: 0.0.1
    """
    def characters(self, filter: dict = None) -> List['XACharacter']:
        """Returns a list of characters matching the filter.

        .. seealso:: :func:`elements`

        .. versionadded:: 0.0.1
        """
        return self.elements("characters", filter, XACharacter)

    def character(self, filter: Union[int, dict]) -> 'XACharacter':
        """Returns the first character that matches the filter.

        .. seealso:: :func:`element_with_properties`

        .. versionadded:: 0.0.1
        """
        return self.element_with_properties("characters", filter, XACharacter)

    def first_character(self) -> 'XACharacter':
        """Returns the character at the first index of the characters array.

        .. seealso:: :func:`first_element`

        .. versionadded:: 0.0.1
        """
        return self.first_element("characters", XACharacter)

    def last_character(self) -> 'XACharacter':
        """Returns the character at the last (-1) index of the characters array.

        .. seealso:: :func:`last_element`

        .. versionadded:: 0.0.1
        """
        return self.last_element("characters", XACharacter)


class XAHasAttributeRuns(XAHasElements):
    """A generic class for objects that have text attribute runs.

    .. versionadded:: 0.0.1
    """
    def attribute_runs(self, filter: dict = None) -> List['XAAttributeRun']:
        """Returns a list of attribute runs matching the filter.

        .. seealso:: :func:`elements`

        .. versionadded:: 0.0.1
        """
        return self.elements("attributeRuns", filter, XAAttributeRun)

    def attribute_run(self, filter: Union[int, dict]) -> 'XAAttributeRun':
        """Returns the first attribute run that matches the filter.

        .. seealso:: :func:`element_with_properties`

        .. versionadded:: 0.0.1
        """
        return self.element_with_properties("attributeRuns", filter, XAAttributeRun)

    def first_attribute_run(self) -> 'XAAttributeRun':
        """Returns the attribute run at the first index of the attribute runs array.

        .. seealso:: :func:`first_element`

        .. versionadded:: 0.0.1
        """
        return self.first_element("attributeRuns", XAAttributeRun)

    def last_attribute_run(self) -> 'XAAttributeRun':
        """Returns the attribute run at the last (-1) index of the attribute runs array.

        .. seealso:: :func:`last_element`

        .. versionadded:: 0.0.1
        """
        return self.last_element("attributeRuns", XAAttributeRun)


class XAHasAttachments(XAHasElements):
    """A generic class for objects that have attachments.

    .. versionadded:: 0.0.1
    """
    def attachments(self, filter: dict = None) -> List['XAAttachment']:
        """Returns a list of attachments matching the filter.

        .. seealso:: :func:`elements`

        .. versionadded:: 0.0.1
        """
        return self.elements("attachments", filter, XAAttachment)

    def attachment(self, filter: Union[int, dict]) -> 'XAAttachment':
        """Returns the first attachment that matches the filter.

        .. seealso:: :func:`element_with_properties`

        .. versionadded:: 0.0.1
        """
        return self.element_with_properties("attachments", filter, XAAttachment)

    def first_attachment(self) -> 'XAAttachment':
        """Returns the attachment at the first index of the attachments array.

        .. seealso:: :func:`first_element`

        .. versionadded:: 0.0.1
        """
        return self.first_element("attachments", XAAttachment)

    def last_attachment(self) -> 'XAAttachment':
        """Returns the attachment at the last (-1) index of the attachments array.

        .. seealso:: :func:`last_element`

        .. versionadded:: 0.0.1
        """
        return self.last_element("attachments", XAAttachment)


class XATextDocument(XAHasParagraphs, XAHasWords, XAHasCharacters, XAHasAttributeRuns, XAHasAttachments):
    """A class for managing and interacting with text documents.

    .. versionadded:: 0.0.1
    """
    def __init__(self, properties):
        super().__init__(properties)

    ## Text
    def set_text(self, new_text: str) -> 'XATextDocument':
        """Sets the text of the document.

        :param new_text: The new text of the document
        :type new_text: str
        :return: A reference to the document object.
        :rtype: XATextDocument

        .. seealso:: :func:`prepend`, :func:`append`

        .. versionadded:: 0.0.1
        """
        self.set_property("text", new_text)
        return self

    def prepend(self, text: str) -> 'XATextDocument':
        """Inserts the provided text at the beginning of the document.

        :param text: The text to insert.
        :type text: str
        :return: A reference to the document object.
        :rtype: XATextDocument

        .. seealso:: :func:`append`, :func:`set_text`

        .. versionadded:: 0.0.1
        """
        old_text = self.text
        self.set_property("text", text + old_text)
        return self

    def append(self, text: str) -> 'XATextDocument':
        """Appends the provided text to the end of the document.

        :param text: The text to append.
        :type text: str
        :return: A reference to the document object.
        :rtype: XATextDocument

        .. seealso:: :func:`prepend`, :func:`set_text`

        .. versionadded:: 0.0.1
        """
        old_text = self.text
        self.set_property("text", old_text + text)
        return self


class XAText(XAHasParagraphs, XAHasWords, XAHasCharacters, XAHasAttributeRuns, XAHasAttachments):
    """A class for managing and interacting with the text of documents.

    .. versionadded:: 0.0.1
    """
    def __init__(self, properties):
        super().__init__(properties)

    def __str__(self):
        if isinstance(self.xa_elem, str):
            return self.xa_elem
        return str(self.xa_elem.get())

    def __repr__(self):
        if isinstance(self.xa_elem, str):
            return self.xa_elem
        return str(self.xa_elem.get())


class XAParagraph(XAText):
    """A class for managing and interacting with paragraphs in text documents.

    .. versionadded:: 0.0.1
    """
    def __init__(self, properties):
        super().__init__(properties)


class XAWord(XAText):
    """A class for managing and interacting with words in text documents.

    .. versionadded:: 0.0.1
    """
    def __init__(self, properties):
        super().__init__(properties)


class XACharacter(XAText):
    """A class for managing and interacting with characters in text documents.

    .. versionadded:: 0.0.1
    """
    def __init__(self, properties):
        super().__init__(properties)


class XAAttributeRun(XAText):
    """A class for managing and interacting with attribute runs in text documents.

    .. versionadded:: 0.0.1
    """
    def __init__(self, properties):
        super().__init__(properties)


class XAAttachment():
    """A class for managing and interacting with attachments in text documents.

    .. versionadded:: 0.0.1
    """
    def __init__(self, properties):
        super().__init__(properties)