try:
    from mats.decorator import test_case
    from mats.node import info
except:
    def test_case ():
        def wrapper (func):
            return func
        return wrapper
    import sys
    sys.path.insert(0, "/home/zsu0915/proj/AndroidViewClient/src")
    import com
    def info(msg):
        print msg
from com.dtmilano.android.viewclient import ViewClient

@test_case()
def main ():
    # buf = bytearray(8)
    # a = memoryview(buf)
    # a[0:8] = b'01234567'
    # print buf
    import os, sys
    args = sys.argv
    info("args0=%s" % args)
    while len(args) > 1 and args[1][0] == '-':
        args.pop(1)
    info("args=%s" % args)
    serialno = args[1] if len(args) > 1 else \
        os.environ['ANDROID_SERIAL'] if os.environ.has_key('ANDROID_SERIAL') \
        else '.*'
    info("serialno=%s" % serialno)
    ViewClient(*ViewClient.connectToDeviceOrExit(verbose=True)).traverse(transform=ViewClient.TRAVERSE_CIT)


if __name__ == '__main__':
    main()
