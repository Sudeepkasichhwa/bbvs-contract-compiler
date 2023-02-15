import dis


def myfunc(alist):
    return len(alist)


dis.dis(myfunc)