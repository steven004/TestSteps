"""
TestSteps is to implement a bunch of functions about test steps execution.
The purpose is to simplify the assertion and automatically logging the steps,
which are not supported in most of the current python test frames.

All the step functions can be used independently, or be used in test frameworks
like py.test or nose
"""

import logging
import os, re, time
from inspect import currentframe
import operator
from .ymal_testbed import init_testbed

__author__ = 'Steven LI'
__version__ = '0.9.7'

__all__ = ['test_logger', 'ok', 'fail', 'eq', 'ne', 'gt', 'lt', 'le', 'ge', 'match', 'unmatch',
           'has', 'hasnt',
           'setlogger', 'addBiOperator', 'getOpWrapper', 'step', 'steps', 's', 'check', 'checks',
           'addStepOption', 'log_new_func', 'auto_func_detection',
           'ReturnPassSet', 'init_testbed']


def __init_logger():
    global test_logger

    # Default handler to the stand output
    ch = logging.StreamHandler()
    formatter = logging.Formatter('%(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    test_logger.addHandler(ch)

    # Add file handler if TESTSTEP_LOG_DIR environment variable defined
    relative_base_path = os.environ.get('TESTSTEP_LOG_PATH')
    if relative_base_path:
        if os.path.exists(relative_base_path):
            file_name = time.strftime("test_%Y%m%d_%H%M.log")
            log_path = os.path.join(os.path.realpath(relative_base_path), file_name)
            fh = logging.FileHandler(log_path)
            formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
            fh.setFormatter(formatter)
            test_logger.addHandler(fh)
        else:
            test_logger.warning("log directory $s does not exist!" % relative_base_path)


test_logger = logging.getLogger("Test")
test_logger.setLevel(logging.DEBUG)


def setlogger(testlogger):
    global test_logger
    test_logger = testlogger


class TestLog__(object):
    def __init__(self):
        self.case_obj = None
        self.case_no = 0
        self.step_no = 0
        self.step_logger = test_logger
        self.step_msg = ''
        self.case_module = None
        self.case_name = ''
        self.pf = True
        self.cause = None
        self.err_msg = ''

    def current_func(self):
        return self.case_obj

    def new_case(self, co):
        self.case_obj = co
        self.step_no = 0
        self.case_name = co.co_name
        self.file_name = co.co_filename
        self.case_no += 1
        self.__log_case()

    def new_func(self, name, path):
        self.step_no = 0
        self.case_name = name
        self.file_name = path
        self.case_no += 1
        self.__log_case()

    def __log_case(self):
        self.step_logger.info("------------------------------------------------------")
        self.step_logger.info("Func %s in file: %s" % (self.case_name, self.file_name))

    def new_step(self, pf, step_info, err_msg=''):
        self.step_no += 1
        if pf:
            self.step_logger.info("Check-%r: %s -PASS- %s" % (self.step_no, step_info, err_msg))
        else:
            self.step_logger.error("Check-%r: %s -FAIL- %s" % (self.step_no, step_info, err_msg))


_this_file = os.path.normcase(setlogger.__code__.co_filename)
__step_info = TestLog__()
__init_logger()
__auto_func_detection = True


def log_new_func(name=None, path=None):
    if name:
        __step_info.new_func(name, path)
    else:
        co = _invoker().f_code
        __step_info.new_case(co)


def auto_func_detection(auto=True):
    global __auto_func_detection
    __auto_func_detection = auto


def _invoker():
    f = currentframe()
    while hasattr(f, "f_code"):
        co = f.f_code
        filename = os.path.normcase(co.co_filename)

        if filename != _this_file:
            return f
        f = f.f_back
    else:
        raise RuntimeError("no code for the frame, why?")


def _step_closure(func):
    """decorator of closure: execution and logging for step functions

    :param func: the step function
    :return: True, or raise exception if error
    """

    def __step(*args, **kwargs):
        __tracebackhide__ = True

        if __auto_func_detection:
            f = _invoker()
            while '__auto_func_detection__' in f.f_locals and not f.f_locals['__auto_func_detection__']:
                f = f.f_back
            co = f.f_code
            if co != __step_info.case_obj:
                __step_info.new_case(co)

        # Get the step message
        (pf, step_info, err_msg) = func(*args, **kwargs)
        __step_info.new_step(pf, step_info, err_msg)
        if not pf:
            # raise TestStepFail(func.__name__, step_info, err_msg)
            raise TestStepFail(step_info, err_msg)

    return __step


##
ReturnPassSet = {0, None}


def passedOrNot(cond):
    for v in ReturnPassSet:
        if cond is v: return True
    return bool(cond)


@_step_closure
def _ok_(cond, desc, errmsg):
    __tracebackhide__ = True
    return (cond, desc, errmsg)


@_step_closure
def ok(cond, passdesc=None, faildesc=None):
    """ One test step to be logged, pass if cond
    :param cond: could be a string, when there is no desc parameter and just pass the step
    :param passdesc: description of this step to be logged if passed
    :param faildesc: description of this step to be logged if failed
    :return: True when it passed
    """
    if not passdesc:
        if isinstance(cond, bool):
            passdesc = "ok(%r)" % cond
        else:  # cond is a description actually, pass anyway.
            passdesc = cond
            cond = True
    if not faildesc:
        faildesc = passdesc

    if passedOrNot(cond):
        return True, passdesc, ''
    else:
        return False, faildesc, ''


@_step_closure
def fail(desc=''):
    return False, "", "fail(%s)" % desc


def _bi_comp_closure(op):
    @_step_closure
    def bi_comp(o1, o2, passdesc='', faildesc=''):
        if not passdesc:
            passdesc = "%r %s %r" % (o1, op, o2)
        if not faildesc:
            faildesc = "%r %s %r" % (o1, op, o2)

        func = _ExtOperation.operator(op)

        err_msg = "%r %s %r?" % (o1, op, o2)
        if func(o1, o2):
            return True, passdesc, err_msg
        else:
            return False, faildesc, err_msg

    return bi_comp


# # Define all the normal functions
eq, ne, gt, lt, ge, le = (_bi_comp_closure(op) for op in ['==', '!=', '>', '<', '>=', '<='])


class TestStepFail(Exception):
    """ custom exception for error reporting. """


class TestRunTimeError(RuntimeError):
    """ custom exception for error reporting. """


##### This is to extend the bi-objects operators in the test format.
class _ExtOperation():
    _operator_dict = {
        '==': operator.eq,
        '!=': operator.ne,
        '<': operator.lt,
        '>': operator.gt,
        '<=': operator.le,
        '>=': operator.ge
    }

    @classmethod
    def operator(cls, op_string):
        if op_string in cls._operator_dict:
            return cls._operator_dict[op_string]
        else:
            raise RuntimeError("Not supported operator: %s", op_string)

    @classmethod
    def register_op(cls, op, func):
        cls._operator_dict[op] = func


addBiOperator = _ExtOperation.register_op
getOpWrapper = lambda op_string: _bi_comp_closure(op_string)

## To add the =~ and !~ operator
addBiOperator('=~', lambda o1, o2: re.compile(o2).search(o1))
match = getOpWrapper('=~')
addBiOperator('!~', lambda o1, o2: not re.compile(o2).search(o1))
unmatch = getOpWrapper('!~')

## To add =<(has) and !< (hasnt) operator
addBiOperator('=>', lambda o1, o2: o2 in o1)
has = getOpWrapper('=>')
addBiOperator('!>', lambda o1, o2: not o2 in o1)
hasnt = getOpWrapper('!>')


####################################################################################
## The section is for step functions implementation
####################################################################################
def step(code_string, globals=None, locals=None, **kwargs):
    __tracebackhide__ = True
    step_string = code_string.strip()
    if len(step_string) == 0: return
    if step_string[0] == '#': return
    if not globals:
        invoker = _invoker()
        globals = invoker.f_globals
        locals = invoker.f_locals
    curStep = TestStep(step_string, globals, locals, **kwargs)
    curStep.parse()
    curStep.execute()

    # Return a dictionary to the invoker for information
    values = [curStep.expr1_val]
    if curStep.expr2_val != None: values.append(curStep.expr2_val)
    return {'values': values,
            'exception': curStep.exception,
            'info': curStep.err_msg,
            'result': curStep.result}


def steps(code_lines, globals=None, locals=None, batch=False):
    __tracebackhide__ = True
    step_list = code_lines.split('\n')

    together = False
    half = ''
    line_no = 0
    step_no = 0
    failed_steps = []
    step_results = []
    for full_string in step_list:
        line_no += 1
        ss = full_string.strip()
        if len(ss) == 0: continue
        if ss[0] == '#': continue
        if together:
            ss = ' '.join([half, ss])
        if ss[-1] == "\\":
            half = ss
            together = True
            continue
        else:
            step_no += 1
            half = ''
            together = False
            try:
                code_string, options = TestStep.parse_steps(ss)
                step_res = step(code_string, globals, locals, **options)
            except Exception as e:
                if not batch: raise e
                test_logger.debug("    ^^^ %d: %s - FAIL - %r   ^^^" % (line_no, code_string, e))
                failed_steps.append({'line': line_no,
                                     'step': step_no,
                                     'code': code_string,
                                     'exception': e})
                step_res = {'exception': e,
                            'code': code_string,
                            'info': e.args,
                            'result': False}
        step_results.append(step_res)

    if len(failed_steps):
        _ok_(False, 'Overall Batch Result: %d checks failed' % len(failed_steps),
             '1st failed step: (line_%d) %s\nerr_msg: %s' % (line_no, failed_steps[0]['code'],
                                                             step_results[0]['info']))
    return {'result': True, 'step_results': step_results}


class TestStep:
    def __init__(self, code_string, globals, locals, **kwargs):
        self.code_string = code_string
        (self.globals, self.locals) = (globals, locals)
        self.kwargs = kwargs

        self.options = dict((k, [False, None]) for k in TestStepOptions.keys())

        self.op_string = None
        self.err_msg = ''
        self.expr1_str, self.expr2_str = (code_string, None)
        self.expr1_val, self.expr2_val = (None, None)
        self.func = None
        self.pass_str = self.fail_str = code_string
        self.result = False
        self.exception = None
        self.warn_msg = None
        self.debug_msg = None

    @classmethod
    def parse_steps(cls, step_string):
        pattern = re.compile(r'(.*?)\s+(?=(?:-\w(?:\s|$)|--\w{2,}(?:\s|$)))(.*)')
        m = pattern.match(step_string)
        code_string = step_string
        option_d = {}
        if m:
            code_string, option_string = m.group(1, 2)
            short_opt_d = dict((v[0], k) for k, v in TestStepOptions.items())
            ol = re.compile(r'(?<!^)\s+(?=(?:-\w|--\w{2,}))').split(option_string)
            for o in ol:
                param = None
                if o[1] != '-':
                    op = o[1]
                    if not op in short_opt_d: raise Exception("Wrong option %s" % op)
                    opt = short_opt_d[op]
                    param = o[2:].strip()
                else:
                    opt, param = re.compile(r'\s+').split(o[2:], 1)
                    if opt not in TestStepOptions:
                        raise Exception(u"Wrong option {0:s}".format(opt))
                if TestStepOptions[opt][1] == int:
                    option_d[opt] = int(param)
                elif TestStepOptions[opt][1] == bool:
                    if not param:
                        option_d[opt] = True
                    else:
                        option_d[opt] = bool(re.compile(r'Y|y|T|t').match(param))
                else:
                    option_d[opt] = eval(param)

        return code_string, option_d

    def parse(self):
        ## Get op and expr strings if there is an op
        for op in _ExtOperation._operator_dict.keys():
            m = re.compile(r'(.*)\s(%s)\s(.*)' % op).match(self.code_string)
            if m:
                (self.expr1_str, self.op_string, self.expr2_str) = m.group(1, 2, 3)
                break

        # Get options
        for (k, v) in self.kwargs.items():
            if k in self.options.keys():
                self.options[k][0] = True
                self.options[k][1] = v
            else:  # should not happen
                raise RuntimeError('ParameterType Error for option: %s' % k)

    def __exe_string(self):
        ret = self.expr1_val = eval(self.expr1_str, self.globals, self.locals)
        if self.op_string:
            self.expr2_val = eval(self.expr2_str, self.globals, self.locals)
            ret = _ExtOperation.operator(self.op_string)(self.expr1_val, self.expr2_val)
            self.err_msg = "%r %s %r" % (self.expr1_val, self.op_string, self.expr2_val)
            # test_logger.debug('--v-- %s --v--'%(self.err_msg))
        else:
            self.err_msg = "%r" % (self.expr1_val)

        # self.result = bool(ret)
        # return ret
        self.result = passedOrNot(ret)
        return self.result

    def execute(self):
        __tracebackhide__ = True
        self.func = self.__exe_string
        for k in TestStepOptPriority:
            if self.options[k][0]:
                self.func = TestStepOptions[k][2](self, self.options[k][1])(self.func)

        self.result = self.func()
        step_description = self.pass_str if self.result else self.fail_str
        _ok_(self.result, step_description, self.err_msg)
        if self.warn_msg:
            test_logger.warning(self.warn_msg)
        if self.debug_msg:
            test_logger.debug(self.debug_msg)

    @classmethod
    def _repeat(cls, obj, seconds):
        def _repeat_(func):
            def do_it(*args, **kwargs):
                p_f = False
                loop = 0
                debug_info = ''
                end_time = time.time() + seconds
                while (time.time() < end_time):
                    p_f = func(*args, **kwargs)
                    loop += 1
                    debug_info += "%d:<%s>  " % (loop, obj.err_msg)
                    if p_f: break
                    time.sleep(1)
                obj.err_msg += ' - tried %d times in %d seconds' % (loop, seconds)
                obj.result = bool(p_f)
                # obj.debug_msg = "Results(-r %d set) { %s}" % (seconds, debug_info)
                test_logger.debug("   vvv  Results(-r %d set) { %s}  vvv" % (seconds, debug_info))
                return p_f

            return do_it

        return _repeat_

    @classmethod
    def _timeout(cls, obj, seconds):
        def _timeout_(func):
            def do_it(*args, **kwargs):
                import threading

                t = threading.Thread(target=func, args=args, kwargs=kwargs)
                t.setDaemon(True)
                t.start()
                t.join(seconds)
                if t.is_alive():
                    obj.err_msg += "  - Step Timeout (-t %d set)" % seconds
                    # test_logger.debug('--v-- step did not complete in %d seconds(-t option set) --v--'%seconds)
                    obj.result = False
                    return False
                else:
                    return obj.result

            return do_it

        return _timeout_

    @classmethod
    def _skip(cls, obj, tf):
        def _skip_(func):
            def __skip__(*args, **kwargs):
                if tf:
                    obj.err_msg = "  - SKIPPED (-s option set)"
                    obj.result = True
                    # test_logger.debug('--v-- step is not executed (due to -s option set) --v--')
                    return True
                else:
                    return func(*args, **kwargs)

            return __skip__

        return _skip_

    @classmethod
    def _xfail(cls, obj, tf):
        def _xfail_(func):
            def __xfail__(*args, **kwargs):
                if tf:
                    ret = func(*args, **kwargs)
                    obj.result = not ret
                    test_logger.debug('    vvv  reverse the result (due to -x option set)  vvv')
                    obj.err_msg += '   - Original result: %r (-x option set) ' % ret
                    return obj.result
                else:
                    return func(*args, **kwargs)

            return __xfail__

        return _xfail_

    @classmethod
    def _warning(cls, obj, tf):
        def _warn_(func):
            def __warn__(*args, **kwargs):
                if tf:
                    ret = func(*args, **kwargs)
                    if not ret:
                        obj.result = not ret
                        # test_logger.warn('--v-- condition not met (pass due to -w option set) --v--')
                        obj.warn_msg = '  ^^^  condition not met (pass due to -w option set)  ^^^ '
                    return obj.result
                else:
                    return func(*args, **kwargs)

            return __warn__

        return _warn_

    @classmethod
    def _duration(cls, obj, seconds):
        def _duration_(func):
            def do_it(*args, **kwargs):
                end_time = time.time() + seconds
                ret = func(*args, **kwargs)
                zzz = end_time - time.time()
                if zzz > 0: time.sleep(zzz)
                obj.err_msg += '  - sleep %d seconds (-d %d set)' % (zzz, seconds)
                # test_logger.debug('--v-- sleep %d seconds (due to -d option set) --v--'%zzz)
                obj.result = ret
                return ret

            return do_it

        return _duration_


TestStepOptions = {
    # options supported, [fullname, paramType, func]
    'repeat': ['r', int, TestStep._repeat],
    'timeout': ['t', int, TestStep._timeout],
    'duration': ['d', int, TestStep._duration],
    'skip': ['s', bool, TestStep._skip],
    'xfail': ['x', bool, TestStep._xfail],
    'warning': ['w', bool, TestStep._warning]
}

TestStepOptPriority = ['xfail', 'repeat', 'timeout', 'duration', 'warning', 'skip']


def addStepOption(long, short, paraType, func, before=None):
    if before:
        i = TestStepOptPriority.index(before)
        TestStepOptPriority.insert(i, long)
    else:
        TestStepOptPriority.append(long)

    TestStepOptions[long] = [short, paraType, func]


## Add the exception (-e) option
def _exception(obj, exception):
    def _exception_(func):
        def do_it(*args, **kwargs):
            try:
                func(*args, **kwargs)
            except exception as e:
                obj.result = True
                obj.err_msg = ' - exception: %r caught' % exception
                obj.exception = e
            else:
                obj.result = False
                obj.err_msg = ' - exception: %r not caught' % exception
            return obj.result

        return do_it

    return _exception_


addStepOption('exception', 'e', Exception, _exception, 'xfail')


## Add passdesc/faildesc (-p/-f) option
def _pass_desc(obj, pass_str):
    def _pass_desc_(func):
        def do_it(*args, **kwargs):
            obj.pass_str = pass_str
            return func(*args, **kwargs)

        return do_it

    return _pass_desc_


def _fail_desc(obj, fail_str):
    def _fail_desc_(func):
        def do_it(*args, **kwargs):
            obj.fail_str = fail_str
            return func(*args, **kwargs)

        return do_it

    return _fail_desc_


addStepOption('passdesc', 'p', str, _pass_desc, 'xfail')
addStepOption('faildesc', 'f', str, _fail_desc, 'xfail')

check = step
checks = steps
s = steps
