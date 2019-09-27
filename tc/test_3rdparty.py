from cats.decorators import test_case, caselog
from cats.actions import comments, delay 
from cats.helpers import get_case_name 
from cats import logger
from time import sleep
import selenium

@test_case()
@caselog
def main ():
    logger.info("start main")
    comments(get_case_name())
    logger.debug("comment action: in case " + get_case_name())
    #sleep(3)
    delay(3000)
    logger.error("test log error")


if __name__ == '__main__':
    main()
