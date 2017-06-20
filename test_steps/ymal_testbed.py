"""
yaml_testbed is a module to set up (initiate) a test bed described in a yaml file.

There are two level of yaml files for a test bed definition: Index file and Object file
    The Index file is to describe an existing test bed, in which there are different components,
    while the object file is to define the objects to be used in a test suite

    e.g. :
    The index file: feature_test_bed_Steven.yaml
        gateway17:  # a gateway machine in the test environment
            mgmtip: 10.74.124.17
            user: root
            password: rootpw

        client18:   # a Linux client in a test environment
            mgmtip: 10.74.124.18
            user: root
            password: rootpw

        cluster-a:  # a storage cluster to be access (using predefined user/account)
            auth_fqdn: auth06.cluster.com
            storage_fqdn: auth06.cluster.com

        cluster-b:  # a storage cluster to be access (using predefined user/account)
            auth_fqdn: auth08.cluster.com
            storage_fqdn: auth08.cluster.com

    The Object file:   basic_write_read_test.yaml
        testbed_conf: feature_test_bed_Steven.yaml    # the index file of the test bed to be used.
        fsg_node:   # the object name
            class: lib.fsgwserver.FsgwServer    # the class name to initiate the object
            name: [gateway17]                   # map to the name in the index file
        nfs_client:
            class: lib.nfsclient.NfsClient
            name: [client18]
        smb_client:
            class: lib.smbclient.SmbClient
            name: [client18]
        cos_cluster:
            class: lib.coscluster.CosCluster
            name: [cluster-a]

In this module, a method is provided to initiate the test bed based on the object yaml file.
    All objects (components under test) are in this module's name space.
"""

import yaml
import os, types, re
import inspect
import importlib


class FileTypeError(TypeError):
    """TestBed file type error exception."""


class MissArguments(ValueError):
    """Missed the arguments in the test bed file"""


def _invoker_file():
    f = inspect.currentframe()
    while hasattr(f, "f_code"):
        co = f.f_code
        filename = os.path.normcase(co.co_filename)

        if filename != os.path.normcase(init_testbed.__code__.co_filename):
            return filename
        f = f.f_back
    else:
        raise RuntimeError("no code for the frame, why?")


def absoluteFilePath(filename, relative_base_file=None):
    if os.path.isabs(filename):
        if os.path.exists(filename):
            return filename
        else:
            raise NameError('{0} does not exist, please double check', filename)


    if relative_base_file:
        relative_base_path = os.path.dirname(relative_base_file)
    else:
        #relative_base_path = os.environ.get('TESTBED_CONFIG_PATH')
        relative_base_path = os.environ.get('TESTSUITE_CONFIG_PATH')

    if not relative_base_path:
        relative_base_path = os.path.dirname(_invoker_file())
    if not filename:
        filename = re.compile('.py$').sub('.yaml', os.path.basename(_invoker_file()))

    filepath = os.path.join(os.path.realpath(relative_base_path), filename)

    if os.path.exists(filepath):
        return filepath

    raise NameError('{0} does not exist, please double check', filepath)


def init_yaml_testbed(filename, tbm):
    with open(filename) as f:
        object_dict = yaml.load(f)

    index_dict = dict()

    # See if the testbed_conf is defined in this object file
    # If yes, load attributes in the files into index_dict
    if 'testbed_conf' in object_dict:
        index_files = object_dict['testbed_conf']
        del object_dict['testbed_conf']
        # The index_file could be a list of a file name.
        # If it is not a list, change it to a list.
        if isinstance(index_files, str):
            index_files = [index_files]

        # load index dictionary
        for index_file in index_files:
            index_file_path = absoluteFilePath(index_file, filename)
            with open(index_file_path) as f:
                index_dict.update(yaml.load(f))

    for tb_object in object_dict.keys():
        attr_dict = object_dict[tb_object]

        class_path = attr_dict['class']
        del attr_dict['class']
        class_name = class_path.split('.')[-1]
        class_file = class_path[:-len(class_name)-1]
        m = importlib.import_module(class_file)
        class_def = getattr(m, class_name)
        # To get arguments and defaults from __init__function if it exists
        try:
            arg_spec = inspect.getargspec(class_def.__init__)
            args = arg_spec.args[1:]    # remove 'self'
            defaults = arg_spec.defaults
            if defaults is None:
                defaults = []
        except AttributeError:
            args = []
            defaults = []

        original_name = attr_dict.get('name')
        if original_name:
            # attr_dict.update(index_dict[original_name])
            attr_dict = dict(list(index_dict[original_name].items()) + list(attr_dict.items()))
            del attr_dict['name']

        arg_value = []
        for i in range(len(args) - len(defaults)):
            if attr_dict.get(args[i]): arg_value.append(attr_dict[args[i]])
            else:
                raise MissArguments('{0} argument missed for class {1}'.format(args[i], class_name))

        for i in range(len(defaults)):
            arg_i = len(args) - len(defaults) + i
            if attr_dict.get(args[arg_i]):
                arg_value.append(attr_dict[args[arg_i]])
            else:
                arg_value.append(defaults[i])

        o = class_def(*arg_value)
        setattr(tbm, tb_object, o)

    return tbm


def init_testbed(filename='', namespace=None):
    filename = absoluteFilePath(filename)
    basename, ext = os.path.splitext(filename)
    tbm = types.ModuleType('test_bed', "Dynamically created test bed module")

    if ext == '.py':
        exec(compile(open(filename, 'rb').read(), filename, 'exec'), tbm.__dict__)
        return tbm
    elif ext == '.yaml':
        return init_yaml_testbed(filename, tbm)
    else:
        raise FileTypeError("{0} is not a valid test bed file type, only .py and .yaml supported".format(filename))

