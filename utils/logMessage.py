import sys, linecache

class logMessage:
    def printException(self):
        exc_type, exc_obj, tb = sys.exc_info()
        f = tb.tb_frame
        lineNo = tb.tb_lineno
        fileName = f.f_code.co_filename
        linecache.checkcache(fileName)
        line = linecache.getline(fileName, lineNo, f.f_globals)
        return 'File "{}", {}, in {} {}: {}'.format(fileName, lineNo, line.strip(), exc_type.__name__, exc_obj)