class NOMEMORY(Exception):
    pass
class DUPLICATE_PID(Exception):
    # rise exception when get_mem is called a 2nd time using same PID
    pass