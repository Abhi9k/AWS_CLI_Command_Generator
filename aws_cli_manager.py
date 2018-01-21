import json
import sys

def get_options_cli(val):
    op_list = []
    for k, v in val.items():
        val_type = infer_option_value_type(v)
        op_list.append(Option(k, v, val_type))
    op_list = [x.get_parsed_option() for x in op_list]
    return reduce(lambda x, y: x + ' ' + y, op_list)

def get_option_value_object(value_type, key, value):
    if value_type == ValueTypes.STRUCT:
        return StructOptionValue(key, value)
    elif value_type == ValueTypes.LIST:
        return ListOptionValue(key, value)
    elif value_type == ValueTypes.I_LIST:
        return IListOptionValue(key, value)
    elif value_type == ValueTypes.I_STRUCT:
        return IStructOptionValue(key, value)
    else:
        return BaseOptionValue(key, value)

def infer_option_value_type(val):
    if type(val) == type({}):
        return ValueTypes.STRUCT
    elif type(val) == type([]):
        return ValueTypes.LIST
    else:
        return ValueTypes.BASE

def generate_aws_cli_command(service_name, command_name, options):
    if type(options) == type('str'):
        options_obj = json.loads(options)
    else:
        options_obj = options

    return "aws {0} {1} {2}".format(service_name, command_name, get_options_cli(options_obj))

class ValueTypes(object):
    STRUCT = 0
    LIST = 1
    I_LIST = 2
    I_STRUCT = 3
    NO_VALUE = 4
    STRING = 5
    INTEGER = 6
    BOOLEAN = 7
    BASE = 8
    NO_VALUE = 9

class Option(object):
    def __init__(self, key, value, value_type):
        self.key = key
        self.option_value = get_option_value_object(value_type, key, value)

    def get_parsed_option(self):
        return "--{0} {1}".format(self.key, str(self.option_value))

class BaseOptionValue(object):
    def __init__(self, key, value=None):
        self.value = value
        self.key = key

    def __str__(self):
        if not self.value:
            return ''
        return str(self.value)

    def __repr__(self):
        return self.__str__()

    def get_sub_type(self, sub_val):
        if type(sub_val) == type({}):
            if type(self.value) == type([]):
                return ValueTypes.STRUCT
            else:
                return ValueTypes.I_STRUCT
        elif type(sub_val) == type([]):
            return ValueTypes.I_LIST
        else:
            return infer_option_value_type(sub_val)

class StructOptionValue(BaseOptionValue):
    def __str__(self):
        values = []
        for key in self.value:
            value = self.value[key]
            option_obj = get_option_value_object(self.get_sub_type(value), key, value)
            values.append("{0}={1}".format(key, str(option_obj)))

        return reduce(lambda x, y: x+','+y, values)

class ListOptionValue(BaseOptionValue):
    def __str__(self):
        values = []
        for item in self.value:
            value = item
            option_obj = get_option_value_object(self.get_sub_type(value), self.key, value)
            values.append(str(option_obj))
        values = ["'{0}'".format(x) for x in values]
        return reduce(lambda x, y: x+' '+y, values)

class IListOptionValue(ListOptionValue):
    def __str__(self):
        values = []
        for item in self.value:
            value = item
            option_obj = get_option_value_object(self.get_sub_type(value), self.key, value)
            values.append(str(option_obj))

        value_str = reduce(lambda x, y: x+','+y, values)
        return "[{1}]".format(self.key, value_str)

    def get_sub_type(self, sub_val):
        if type(sub_val) == type({}):
            return ValueTypes.I_STRUCT
        else:
            return ValueTypes.BASE

class IStructOptionValue(BaseOptionValue):
    def __str__(self):
        values = []
        for key in self.value:
            value = self.value[key]
            option_obj = get_option_value_object(self.get_sub_type(value), key, value)
            values.append("{0}={1}".format(key, str(option_obj)))
        value_str = reduce(lambda x, y: x+','+y, values)
        return "{0}{1}{2}".format('{', value_str, '}')

if __name__ == '__main__':
    if len(sys.argv) < 4:
        print '='*40
        print '='*18 + 'Usage' + '='*17
        print '='*40
        print 'python aws_cli_manager.py <aws service name> <service command name> <valid json string containing options>'
        print 'For example:'
        print 'python aws_cli_manager.py ec2 run-instances \'{"image-id":"some image id","instance-type":"t2.small","dry-run":"","tag-specifications":[{"ResourceType":"instance","Tags":[{"Key":"Name","Value":"myserver"}]}]}\''
    else:
        print generate_aws_cli_command(sys.argv[1], sys.argv[2], json.loads(sys.argv[3].strip()))
