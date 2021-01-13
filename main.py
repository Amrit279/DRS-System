import capture # Not an in-built or installed module
class DRS:
    """
    Helps the umpire in making his decision if he is not sure whether the batsman is out or
    not out. You can move frames back and forward and then make your decision whether a
    batsman is out or not.
    """
    def __init__(self):
        capture.makeVideo()

if __name__ == "__main__":
    drs = DRS()