#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""Support functions for Stoner package.

These functions depend only on Stoner.compat which is used to ensure a consostent namespace.

Created on Wed Apr 19 19:47:50 2017

@author: Gavin Burnell
"""
from collections import Iterable,MutableSequence
from .compat import string_types,bytes2str
import re
import inspect

from numpy import log10,floor,abs,logical_and,isnan,round
from cgi import escape as html_escape
from copy import deepcopy

operator={
    "eq":lambda k,v:k==v,
    "ne":lambda k,v:k!=v,
    "contains":lambda k,v: v in k,
    "in":lambda k,v: k in v,
    "icontains":lambda k,v: k.upper() in str(v).upper(),
    "iin":lambda k,v: str(v).upper() in k.upper(),
    "lt":lambda k,v:k<v,
    "le":lambda k,v:k<=v,
    "gt":lambda k,v:k>v,
    "ge":lambda k,v:k>=v,
    "between":lambda k,v: logical_and(min(v)<k,k<max(v)),
    "ibetween":lambda k,v: logical_and(min(v)<=k,k<=max(v)),
    "ilbetween":lambda k,v: logical_and(min(v)<=k,k<max(v)),
    "iubetween":lambda k,v: logical_and(min(v)<k,k<=max(v)),
    "startswith":lambda k,v:str(v).startswith(k),
    "istartswith":lambda k,v:str(v).upper().startswith(k.upper()),
    "endsswith":lambda k,v:str(v).endswith(k),
    "iendsswith":lambda k,v:str(v).upper().endswith(k.upper()),
}

prefs={"text":{
        3: "k",6: "M",9: "G",12: "T",15: "P",18: "E",21: "Z",24: "Y",
        -3: "m", -6: "u", -9: "n", -12: "p", -15: "f", -18: "a", -21: "z", -24: "y"
        },
        "latex":{
        3: "k",6: "M",9: "G",12: "T",15: "P",18: "E",21: "Z",24: "Y",
        -3: "m", -6: r"\mu", -9: "n", -12: "p", -15: "f", -18: "a", -21: "z", -24: "y"
        },
        "html":{
        3: "k",6: "M",9: "G",12: "T",15: "P",18: "E",21: "Z",24: "Y",
        -3: "m", -6: r"&micro;", -9: "n", -12: "p", -15: "f", -18: "a", -21: "z", -24: "y"
        }
    }


def isNone(iterator):
    """Returns True if input is None or an empty iterator, or an iterator of None.

    Args:
        iterator (None or Iterable):

    Returns:
        True if iterator is None, empty or full of None.
    """
    if iterator is None:
        ret=True
    elif isiterable(iterator) and not isinstance(iterator,string_types):
        if len(iterator)==0:
            ret=True
        else:
            for i in iterator:
                if i is not None:
                    ret=False
                    break
            else:
                ret=True
    else:
        ret=False
    return ret

def all_size(iterator,size=None):
    """Check whether each element of *iterator* is the same length/shape.

    Arguments:
        iterator (Iterable): list or other iterable of things with a length or shape

    Keyword Arguments:
        size(int, tuple or None): Required size of each item in iterator.

    Returns:
        True if all objects are the size specified (or the same size if size is None).
    """
    if hasattr(iterator[0],"shape"):
        sizer=lambda x:x.shape
    else:
        sizer=lambda x:len(x)

    if size is None:
        size=sizer(iterator[0])
    ret=False
    for i in iterator:
        if sizer(i)!=size:
            break
    else:
        ret=True
    return ret


def all_type(iterator,typ):
    """Determines if an interable omnly contains a common type.

    Arguments:
        iterator (Iterable): The object to check if it is all iterable
        typ (class): The type to check for.

    Returns:
        True if all elements are of the type typ, or False if not.

    Notes:
        Routine will iterate the *iterator* and break when an element is not of
        the search type *typ*.
    """
    ret=False
    if isiterable(iterator):
        for i in iterator:
            if not isinstance(i,typ):
                break
        else:
            ret=True
    return ret

def isiterable(value):
    """Chack to see if a value is iterable.
    
    Args:
        value (object): Entitiy to check if it is iterable
        
    Returns:
        (bool): True if value is an instance of collections.Iterable.
    """
    return isinstance(value,Iterable)

def isproperty(obj,name):
    """Check whether an attribute of an object or class is a property.
    
    Args:
        obj (instance or class): Thing that has the attribute to check
        name (str): Name of the attrbiute that might be a property
        
    Returns:
        (bool): Whether the name is a property or not.
    """
    if isinstance(obj,object):
        obj=obj.__class__
    elif not issubclass(obj,object):
        raise TypeError("Can only check for property status on attributes of an object or a class not a {}".format(type(obj)))
    return hasattr(obj,name) and isinstance(getattr(obj,name),property)

def istuple(obj,*args,**kargs):
    """Determine if obj is a tuple of a certain signature.
    
    Args:
        obj(object): The object to check
        *args(type): Each of the suceeding arguments are used to determine the expected type of each element.
        
    Keywoprd Arguments:
        strict(bool): Whether the elements of the tuple have to be exactly the type specified or just castable as the type
        
    Returns:
        (bool): True if obj is a matching tuple.
    """
    strict=kargs.pop("strict",True)
    if not isinstance(obj,tuple):
        return False
    if len(args)>0 and len(obj)!=len(args):
        return False
    for t,e in zip(args,obj):
        if strict:
            if not isinstance(e,t):
                bad=True
                break
        else:
            try:
                v=t(e)
            except ValueError:
                bad=True
                break
    else:
        bad=False
    return not bad


def tex_escape(text):
    """
        Escapes spacecial text charcters in a string.

        Parameters:
            text (str): a plain text message

        Returns:
            the message escaped to appear correctly in LaTeX

    From `Stackoverflow <http://stackoverflow.com/questions/16259923/how-can-i-escape-latex-special-characters-inside-django-templates>`

    """
    conv = {
        '&': r'\&',
        '%': r'\%',
        '$': r'\$',
        '#': r'\#',
        '_': r'\_',
        '{': r'\{',
        '}': r'\}',
        '~': r'\textasciitilde{}',
        '^': r'\^{}',
        '\\': r'\textbackslash{}',
        '<': r'\textless',
        '>': r'\textgreater',
    }
    regex = re.compile('|'.join(re.escape(bytes2str(key)) for key in sorted(conv.keys(), key = lambda item: - len(item))))
    return regex.sub(lambda match: conv[match.group()], text)


def format_val(value,**kargs):
    """Format a number as an SI quantity
    
    Args:
        value(float): Value to format

    Keyword Arguments:
        fmt (str): Specify the output format, opyions are:
            *  "text" - plain text output
            * "latex" - latex output
            * "html" - html entities
        escape (bool): Specifies whether to escape the prefix and units for unprintable characters in non text formats )default False)
        mode (string): If "float" (default) the number is formatted as is, if "eng" the value and error is converted
            to the next samllest power of 1000 and the appropriate SI index appended. If mode is "sci" then a scientifc,
            i.e. mantissa and exponent format is used.
        units (string): A suffix providing the units of the value. If si mode is used, then appropriate si prefixes are
            prepended to the units string. In LaTeX mode, the units string is embedded in \\mathrm
        prefix (string): A prefix string that should be included before the value and error string. in LaTeX mode this is
            inside the math-mode markers, but not embedded in \\mathrm.

    Returns:
        (str): The formatted value.
    """
    mode=kargs.pop("mode","float")
    units=kargs.pop("units","")
    prefix=kargs.pop("prefix","")
    latex=kargs.pop("latex",False)
    fmt=kargs.pop("fmt","latex" if latex else "text")
    escape=kargs.pop("escape",False)
    escape_func={"latex":tex_escape,"html":html_escape}.get(mode,lambda x:x)

    if escape:
        prefix=escape_func(prefix)
        units=escape_func(units)

    if mode == "float":  # Standard
        suffix_val = ""
    elif mode == "eng":  #Use SI prefixes
        v_mag = floor(log10(abs(value)) / 3.0) * 3.0
        prefixes = prefs.get(fmt,prefs["text"])
        if v_mag in prefixes:
            if fmt=="latex":
                suffix_val = r"\mathrm{{{{{}}}}}".format(prefixes[v_mag])
            else:
                suffix_val = prefixes[v_mag]
            value /= 10 ** v_mag
        else:  # Implies 10^-3<x<10^3
            suffix_val = ""
    elif mode == "sci":  # Scientific mode - raise to common power of 10
        v_mag = floor(log10(abs(value)))
        if fmt=="latex":
            suffix_val = r"\times 10^{{{{{}}}}}".format(int(v_mag))
        elif fmt=="html":
            suffix_val = "&times; 10<sup>{}</sup> ".format(int(v_mag))
        else:
            suffix_val = "E{} ".format(int(v_mag))
        value /= 10 ** v_mag
    else:  # Bad mode
        raise RuntimeError("Unrecognised mode: {} in format_error".format(mode))

    #Protect {} in units string
    units = units.replace("{", "{{").replace("}", "}}")
    prefix = prefix.replace("{", "{{").replace("}", "}}")
    if fmt=="latex":  # Switch to latex math mode symbols
        val_fmt_str = r"${}{{}}".format(prefix)
        if units != "":
            suffix_fmt = r"\mathrm{{{{{}}}}}".format(units)
        else:
            suffix_fmt = ""
        suffix_fmt += "$"
    elif fmt=="html":  # Switch to latex math mode symbols
        val_fmt_str = r"{}{{}}".format(prefix)
        suffix_fmt = units
    else:  # Plain text
        val_fmt_str = r"{}{{}}".format(prefix)
        suffix_fmt = units
    fmt_str = val_fmt_str + suffix_val + suffix_fmt
    return fmt_str.format(value)
        
def format_error(value, error=None, **kargs):
    """This handles the printing out of the answer with the uncertaintly to 1sf and the
    value to no more sf's than the uncertainty.

    Args:
        value (float): The value to be formated
        error (float): The uncertainty in the value
        fmt (str): Specify the output format, opyions are:
            *  "text" - plain text output
            * "latex" - latex output
            * "html" - html entities
        escape (bool): Specifies whether to escape the prefix and units for unprintable characters in non text formats )default False)
        mode (string): If "float" (default) the number is formatted as is, if "eng" the value and error is converted
            to the next samllest power of 1000 and the appropriate SI index appended. If mode is "sci" then a scientifc,
            i.e. mantissa and exponent format is used.
        units (string): A suffix providing the units of the value. If si mode is used, then appropriate si prefixes are
            prepended to the units string. In LaTeX mode, the units string is embedded in \\mathrm
        prefix (string): A prefix string that should be included before the value and error string. in LaTeX mode this is
            inside the math-mode markers, but not embedded in \\mathrm.

    Returns:
        String containing the formated number with the eorr to one s.f. and value to no more d.p. than the error.
    """
    mode=kargs.get("mode","float")
    units=kargs.get("units","")
    prefix=kargs.get("prefix","")
    latex=kargs.get("latex",False)
    fmt=kargs.get("fmt","latex" if latex else "text")
    escape=kargs.get("escape",False)
    escape_func={"latex":tex_escape,"html":html_escape}.get(mode,lambda x:x)

    if error == 0.0 or isnan(error):  # special case for zero uncertainty
        return format_val(value,**kargs)

    if escape:
        prefix=escape_func(prefix)
        units=escape_func(units)

    #Sort out special fomatting for different modes
    if mode == "float":  # Standard
        suffix_val = ""
    elif mode == "eng":  #Use SI prefixes
        v_mag = floor(log10(abs(value)) / 3.0) * 3.0
        prefixes = prefs.get(fmt,prefs["text"])
        if v_mag in prefixes:
            if fmt=="latex":
                suffix_val = r"\mathrm{{{{{}}}}}".format(prefixes[v_mag])
            else:
                suffix_val = prefixes[v_mag]
            value /= 10 ** v_mag
            error /= 10 ** v_mag
        else:  # Implies 10^-3<x<10^3
            suffix_val = ""
    elif mode == "sci":  # Scientific mode - raise to common power of 10
        v_mag = floor(log10(abs(value)))
        if fmt=="latex":
            suffix_val = r"\times 10^{{{{{}}}}}".format(int(v_mag))
        elif fmt=="html":
            suffix_val = "&times; 10<sup>{}</sup> ".format(int(v_mag))
        else:
            suffix_val = "E{} ".format(int(v_mag))
        value /= 10 ** v_mag
        error /= 10 ** v_mag
    else:  # Bad mode
        raise RuntimeError("Unrecognised mode: {} in format_error".format(mode))

# Now do the rounding of the value based on error to 1 s.f.
    e2 = error
    u_mag = floor(log10(abs(error)))  #work out the scale of the error
    error = round(error / 10 ** u_mag) * 10 ** u_mag  # round the error, but this could round to 0.x0
    u_mag = floor(log10(error))  # so go round the loop again
    error = round(e2 / 10 ** u_mag) * 10 ** u_mag  # and get a new error magnitude
    value = round(value / 10 ** u_mag) * 10 ** u_mag
    u_mag = min(0, u_mag)  # Force integer results to have no dp

    #Protect {} in units string
    units = units.replace("{", "{{").replace("}", "}}")
    prefix = prefix.replace("{", "{{").replace("}", "}}")
    if fmt=="latex":  # Switch to latex math mode symbols
        val_fmt_str = r"${}{{:.{}f}}\pm ".format(prefix, int(abs(u_mag)))
        if units != "":
            suffix_fmt = r"\mathrm{{{{{}}}}}".format(units)
        else:
            suffix_fmt = ""
        suffix_fmt += "$"
    elif fmt=="html":  # Switch to latex math mode symbols
        val_fmt_str = r"{}{{:.{}f}}&plusmin;".format(prefix, int(abs(u_mag)))
        suffix_fmt = units
    else:  # Plain text
        val_fmt_str = r"{}{{:.{}f}}+/-".format(prefix, int(abs(u_mag)))
        suffix_fmt = units
    if u_mag < 0:  # the error is less than 1, so con strain decimal places
        err_fmt_str = r"{:." + str(int(abs(u_mag))) + "f}"
    else:  # We'll be converting it to an integer anyway
        err_fmt_str = r"{}"
    fmt_str = val_fmt_str + err_fmt_str + suffix_val + suffix_fmt
    if error >= 1.0:
        error = int(error)
        value = int(value)
    return fmt_str.format(value, error)

def fix_signature(proxy_func,wrapped_func):
    """Tries to update proxy_func to have a signature that matches the wrapped func."""
    try:
        proxy_func.__wrapped__.__signature__=inspect.signature(wrapped_func)
    except AttributeError: #Non-critical error
        try:
            proxy_func.__signature__= inspect.signature(wrapped_func)
        except AttributeError:
            pass
    return proxy_func            


class _attribute_store(dict):
    
    """A dictionary=like class that provides attributes that work like indices.

    Used to implement the mapping of column types to indices in the setas attriobutes.
    """

    def __init__(self, *args, **kargs):
        """Initialise from a dictionary."""
        if len(args) == 1 and isinstance(args[0], dict):
            self.update(args[0])
        else:
            super(_attribute_store, self).__init__(*args, **kargs)

    def __setattr__(self, name, value):
        """Setting an attribute is equivalent to setting an item."""
        self[name] = value

    def __getattr__(self, name):
        """Getting an attrbute is equivalent to getting an item."""
        try:
            return self[name]
        except KeyError:
            raise AttributeError
            
def quantize(number,quantum):
    """Round a number to the nearest multiple of a quantum.
    
    Args:
        number (float,array): Number(s) to be rounded to the nearest qyuantum
        quantum (float): Quantum to round to
    Returns:
        number rounded to qunatum
    """
    return round(number/quantum)*quantum

class typedList(MutableSequence):
    """Subclass list to make setitem enforce  strict typing of members of the list."""
    
    def __init__(self,*args,**kargs):
        if len(args)==0 or not (isinstance(args[0],type) or (isinstance(args[0],tuple) and all_type(args[0],type))):
            self._type=str # Default list type is a string
        else:
            args=list(args)
            self._type=args.pop(0)
        if len(args)==0:
            self._store=list(*args,**kargs)
        elif len(args)==1 and all_type(args[0],self._type):
            self._store=list(*args,**kargs)
        else:
            if len(args)>1:
                raise SyntaxError("List should be constructed with at most two arguments, a type and an iterable")
            else:
                raise TypeError("List should be initialised with elements that are all of type {}".format(self._type))

    def __add__(self,other):
        if isiterable(other):
            new=deepcopy(self)
            new.extend(other)
            return new
        else:
            return NotImplemented
        
    def __iadd__(self,other):
        if isiterable(other):
            self.extend(other)
            return self
        else:
            return NotImplemented
        
    def __radd__(self,other):
        if isinstance(other,list):
            return other+self._store
        else:
            return NotImplemented
        
    def __eq__(self,other):
        return self._store==other
                        
    def __delitem__(self,index):
        del self._store[index]
        
    def __getitem__(self,index):
        return self._store[index]
    
    def __len__(self):
        return len(self._store)

    def __repr__(self):
        return repr(self._store)

    def __setitem__(self,name,value):
        if isiterable(name) or isinstance(name,slice):
            if not isiterable(value) or not all_type(value,self._type):
                raise TypeError("Elelements of this list should be of type {} and must set the correct number of elements".format(self._type))
        elif not isinstance(value,self._type):
            raise TypeError("Elelements of this list should be of type {}".format(self._type))
        self._store[name]=value
        
    def extend(self,other):
        if not isiterable(other) or  not all_type(other,self._type):
            raise TypeError("Elelements of this list should be of type {}".format(self._type))
        else:
            self._store.extend(other)
            
    def index(self,search,start=0):
        return self._store[start:].index(search)
    
    def insert(self,index,obj):
        if not isinstance(obj,self._type):
            raise TypeError("Elelements of this list should be of type {}".format(self._type))
        else:
            self._store.insert(index,obj)
            
