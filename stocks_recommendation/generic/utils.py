import os
import sys
import yaml
import shutil
import pickle
import inspect
import argparse
import datetime
from pathlib import Path

def load_pickle(filepath):
    '''load data from pickle
    
    Arguments:
        filepath {str} -- Pickle file path
    
    Returns:
        contents -- Return contents in whatever format they were strored in pickle
    '''
    data = None
    if os.path.exists(filepath):
        with open(filepath, 'rb') as f:
            data = pickle.load(f)
    return data

def save_to_pickle(data, abs_file_path):
    '''Save the data to pickle in the desired path
    
    Arguments:
        data {python_object} -- Data could be any valid python object
        abs_file_path {str} -- Absolute path of the file
    '''

    if os.path.exists(abs_file_path) and data:
        with open(abs_file_path, 'wb') as handle:
            pickle.dump(data, handle, protocol=pickle.HIGHEST_PROTOCOL)

def age(filepath, days=30):
    '''This function checks if the file is older than N days.
    
    Arguments:
        filepath {str} -- Path of the file
    
    Keyword Arguments:
        days {int} -- Number of days (default: {30})
    
    Returns:
        bool -- Returns True, if file age is > N days
    '''

    today = datetime.datetime.today()
    modified_date = datetime.datetime.fromtimestamp(os.path.getmtime(filepath))
    duration = today - modified_date
    return duration.days > days

def surround_double_quotes(string):
    '''Surrounds the input string with double quotes and returns the modified string

    Arguments:
        string {string} -- String to be modified

    Returns:
        string -- String with double quotes
    '''

    return '"' + str(string) + '"'

def surround_mysql_quotes(string):
    '''Surrounds the input string with `` and returns the modified string
    
    Arguments:
        string {str} -- String to be modified
    
    Returns:
        string -- String with `mysql quotes`
    '''

    return '`' + str(string) + '`'

def print_err_exit(err_msg):
    '''Print the Error Message and Exits the Program

    Arguments:
        err_msg {string} -- Error Message
    '''

    print ("ERROR: " + err_msg)

    sys.exit(1)

def print_warn(warn_msg):
    '''Print the Warning Message and continues the Program execution

    Arguments:
        warn_msg {string} -- Warning Message
    '''
    print ("WARNING: " + warn_msg)

def print_msg(msg):
    '''Print * across the screen width and puts the msg in the center of the screen

    Arguments:
        msg {string} -- message to be print
    '''
    try:
        rows, columns = os.popen('stty size', 'r').read().split()
        print (msg.center(int(columns), '*'))
    except:
        print (msg)

def is_var_type(var, expected_type):
    '''Returns True if the expected variable type and provided variable type matches

    Arguments:
        var {variable} -- Any valid python variable
        expected_type {variable_type} -- Any valid python variable type

    Returns:
        bool -- Returns True, else Exits the Program
    '''

    if not (type(var) == expected_type):
        msg = "Expected:" + str(expected_type) + " " + "Received:" + str(type(var))
        print_err_exit(msg)
    return True

def stripper(elements_list):
    '''Strips unwanted spaces from start and end, in a list of strings

    Arguments:
        elements_list {list} -- List of strings

    Returns:
        list -- Stripped strings list
    '''
    is_var_type(elements_list, list)
    return [ element.strip() for element in elements_list ]

def del_element(element, elements_list, silent_discard=True):
    '''Removes an element from a list

    Arguments:
        element {string} -- Element to be removed
        elements_list {list} -- List of Strings

    Keyword Arguments:
        silent_discard {bool} -- Discard Message (default: {True})
    '''

    is_var_type(elements_list, list)

    try:
        elements_list.remove(element)
    except:
        if not silent_discard:
            msg = "KeyError:" + " " + surround_double_quotes(element) + " " + "not found"
            print_err_exit(msg)

def write_to_yaml(data, filepath, silent_discard=True):
    '''Write the data to YAML file, raises Error Message on demand

    Arguments:
        data {string} -- Data to be written
        filepath {string} -- Path of file

    Keyword Arguments:
        silent_discard {bool} -- Discard Message (default: {True})
    '''

    is_successful = False
    try:
        with open(filepath, 'w') as outfile:
            yaml.dump(data, outfile, default_flow_style=False)
            is_successful = True
    except:
        pass
    if not silent_discard:
        if is_successful:
            print ("Write Data to file: %s is successful" %filepath)
        else:
            msg = "Write Data to file:" + " " + surround_double_quotes(filepath) + " " + "failed"
            print_err_exit(msg)

def del_key(key, dictionary, silent_discard=True):
    '''Deletes Key from a dictionary, and raises Not Found Error Message on demand

    Arguments:
        key {string} -- Key to be deleted
        dictionary {dictonary} -- Dictionary
    '''

    is_var_type(dictionary, dict)

    try:
        del dictionary[key]
    except:
        if not silent_discard:
            msg = "KeyError:" + " " + surround_double_quotes(key) + " " + "not found"
            print_err_exit(msg)

def get_env(env_var_list):
    '''Return dictionary of the env variables Else raises Error Message

    Arguments:
        env_var_list {list} -- List of the variables expected to be present in environment
    '''

    is_var_type(env_var_list, list)

    if (len(env_var_list) <= 0):
        msg = "Empty env_var_list"
        print_err_exit(msg)

    vars_dict = {}
    for var in env_var_list:
        if os.environ.get(var) is None:
            msg = "ENV_VAR:" + " " + surround_double_quotes(var) + " " + "is not defined"
            print_err_exit(msg)
        else:
            vars_dict[var] = os.environ.get(var)
    return vars_dict

def is_file(filepath, silent_discard = True):
    '''Return True if the file exists Else returns False and raises Not Found Error Message

    Arguments:
        filepath {String} -- File Path

    Raises:
        OSError -- Raises OSError exception if file not found

    Returns:
        bool -- True, if file is found Or False, if file is not found
    '''

    try:
        if os.path.isfile(filepath):
            return True
        else:
            raise OSError
    except:
        if not silent_discard:
            print ("%s No such file exists" %filepath)
        return False

def is_dir(dirpath, silent_discard = True):
    '''Return True if the folder exists Else returns False and raises Not Found Error Message

    Arguments:
        dirpath {String} -- Folder Path

    Raises:
        OSError -- Raises OSError exception if folder not found

    Returns:
        bool -- True, if folder is found Or False, if folder is not found
    '''

    try:
        if os.path.isdir(dirpath):
            return True
        else:
            raise OSError
    except:
        if not silent_discard:
            print ("%s No such directory exists" %dirpath)
        return False

def remove(path, silent_discard = True):
    '''Removes any file or folder recursively, if it exists else reports error message based on user demand

    Arguments:
        path {string} -- Accepts folder or file path
    '''
    is_successful = False
    try:
        if is_dir(path):
            shutil.rmtree(path)
            is_successful = True
        else:
            os.remove(path)
            is_successful = True
    except OSError as e:
        pass
    if not silent_discard:
        if is_successful:
            print ("%s Removed successfully" %path)
        else:
            print ("Error: %s" %path, e.strerror)
            sys.exit(1)

def load_yaml(filepath):
    '''Read yaml file data and returns data in a dict format

    Arguments:
        filepath {string} -- Path of the yaml file

    Returns:
        dict -- Return Python dict if the file reading is successful
        None -- If file reading fails
    '''

    if is_file(filepath):
        try:
            with open(filepath) as f:
                data = yaml.safe_load(f)
            return data
        except:
            print ("%s file reading failed" %filepath)
            return None

def mkdir(folderpath, silent_discard = True):
    '''Create the folder structure, raises Error Message on demand

    Arguments:
        folderpath {string} -- Path of the folder structure
    '''
    is_successful = False
    try:
        os.makedirs(folderpath)
        is_successful = True
    except:
        pass

    if not silent_discard:
        if is_successful:
            print ("%s Directory created " %folderpath)
        else:
            print ("%s Unable to create directory " %folderpath)
            sys.exit(1)

def detailed_error():
    exc_type, exc_obj, exc_tb = sys.exc_info()
    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
    print(exc_type, fname, exc_tb.tb_lineno)

class LoadFromFile (argparse.Action):
    '''Allows to read from a yaml file and using argparse to set the attribute values

    Arguments:
        argparse {Namespace} -- It reads the user arguments from the file using argparse library

    Raises:
        CustomError -- Raises Custom error message if file reading fails
    '''

    def __call__ (self, parser, namespace, values, option_string = None):

        # Read user config file
        try:
            with values as f:
                contents = f.read()
            data = yaml.safe_load(contents)

        # Set the arguments after reading from the file. It will stop reading after one correct read
            for k, v in data.items():
                for nk, nv in v.items():
                    setattr(namespace, nk, nv)
                break
        except Exception as e:
            detailed_error()

if __name__ == "__main__":
    pass
