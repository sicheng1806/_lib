from collections import UserList
from collections.abc import Iterable
class FixedList(UserList):
    '''A fixed length List class '''

    def __init__(self,initlist = None,_len = None):
        self.data = []
        if initlist is not None and _len is None:
            if type(initlist) == type(self.data):
                self.data[:] = initlist
            elif isinstance(initlist, UserList):
                self.data[:] = initlist.data[:]
            else:
                self.data = list(initlist)
            self.len = self.data.__len__
        elif initlist is not None and _len is not None:
            self.len = _len
            if type(initlist) == type(self.data):
                self.data[:] = initlist[:_len] if len(initlist) >= self.len else initlist
            elif isinstance(initlist, UserList):
                self.data[:] = initlist.data[:_len] if len(initlist) >= self.len else initlist.data
            else:
                self.data[:] = list(initlist)[:_len] if len(initlist) >= self.len else list(initlist)
        else:
            self.len = _len if _len is not None else 0
            for i in range(self.len):
                self.data.append(None)
        
        

    def __setitem__(self,i,item):
        if isinstance(i,slice):
            if i.stop > self.len:raise ValueError("值溢出")
            stop = i.stop
            step = i.step if i.step is not None else 1
            start = i.start if i.start is not None else 0
            if (stop-start) // step != len(item): raise ValueError("不等长")
        return super().__setitem__(i,item)
    def __delitem__(self,i):
        raise NotImplementedError("如果要删除,请直接赋值为None")
    def __add__(self, other: Iterable) :
        raise NotImplementedError()
    def __radd__(self, other: Iterable) :
        raise NotImplementedError()
    def __iadd__(self, other: Iterable):
        raise NotImplementedError()
    def __mul__(self, n: int) :
        raise NotImplementedError()
    def __imul__(self, n: int) :
        raise NotImplementedError()
    def append(self, item) -> None:
        raise NotImplementedError()
    
    def insert(self, i: int, item) -> None:
        raise NotImplementedError()
    def extend(self, other: Iterable) -> None:
        raise NotImplementedError()


if __name__ == '__main__':
    lst = FixedList(_len = 10)
    lst[0] = 1
    lst[1:10] = [i for i in range(1,10)]
    print(lst)