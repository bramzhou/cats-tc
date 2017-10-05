from mats.decorator import test_case, caselog
from mats.actions.blee import comments


mut_device = '${deviceId0}'

@caselog
def pyfun(name):
    print "Hello from pyfun"
    print "Please to meet you,", name

@test_case("SAMPLE_CASE")
def main():
    comments("Hello C-ATS")
    pyfun("joe")


if __name__ == '__main__':
    main()