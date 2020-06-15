import functools, json, os, re, traceback

class Log:
    __indent_level__ = 0

    def __init__(self, file_path:str=None, print_logs:bool=True, append:bool=False, indent_string:str="\t", use_repr:bool=True):
        self.__file_path__ = file_path
        self.__print_logs__ = print_logs
        self.__indent_string__ = indent_string
        self.__stringify__ = repr if use_repr else str
        if file_path:
            base_path = os.sep.join(file_path.split(os.sep)[:-1])
            if base_path and not os.path.exists(base_path):
                os.makedirs(base_path)
            open(file_path, "a" if append else "w")
            self.__log_file__ = open(file_path, "a")


    def __del__(self):
        if self.__file_path__ and not self.__log_file__.closed:
            self.__log_file__.close()


    def log(self, value, as_json:(bool,str)=False, use_repr:bool=None):
        stringify = self.__stringify__ if use_repr is None else (repr if use_repr else str)
        if as_json:
            try:
                value_to_print = json.dumps(value, indent=2, default=repr if as_json == "repr" else str)
            except:
                value_to_print = stringify(value)
        elif isinstance(value, BaseException):
            value_to_print = "".join(["%s\n" % stringify(value)] + traceback.format_tb(value.__traceback__))
        else:
            value_to_print = stringify(value)

        if self.__indent_level__:
            def repl(m):
                return self.__indent_string__ * (self.__indent_level__ + len(m.group(0)))
            value_to_print = re.sub("^\t*", repl, value, flags=re.M)

        if self.__file_path__:
            self.__log_file__.write(f"{value_to_print}\n")

        if self.__print_logs__:
            print(value_to_print)


    def decorate(self, header:(bool,str)=True, log_args:bool=False) -> callable:
        def inner_wrapper(func:callable) -> callable:
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                nonlocal header
                if header != False:
                    if header == True:
                        str_args = f"*{repr(args)}, **{repr(kwargs)}" if log_args else "\u2026"
                        header = f"{func.__name__}({str_args})"
                    self.log(header, use_repr=False)
                indent_level = self.indent()
                try:
                    return func(*args, **kwargs)
                finally:
                    self.set_indent(indent_level)
            return wrapper
        return inner_wrapper


    def indent(self, levels:int=1) -> int:
        return self.set_indent(self.__indent_level__ + levels)


    def unindent(self, levels:int=1) -> int:
        return self.set_indent(self.__indent_level__ - levels)


    def set_indent(self, level:int) -> int:
        old_level = self.__indent_level__
        self.__indent_level__ = max(0, level)
        return old_level


    def get_indent(self) -> int:
        return self.__indent_level__


    def set_indent_string(self, indent_string) -> str:
        old_indent_string = self.__indent_string__
        self.__indent_string__ = indent_string
        return old_indent_string


    def get_indent_string(self) -> str:
        return self.__indent_string__
