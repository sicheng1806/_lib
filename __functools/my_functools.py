import operator



#---------------------T2族函数---------------------------
def T2(func:callable)->callable:
    '''实现了使二元函数扩展到多维的工厂函数'''
    def Tong(iterable,Begin):
        a_ = Begin
        for a in iterable:
            a_ = func(a_,a)
        return a_
    return Tong

def T2_or(iterable):
    return T2(operator.__or__)(iterable,0)

def T2_and(iterable):
    return T2(operator.add)(iterable,1)
#----------Fn族递归函数----------------
def Fn(func,n,arg):
    '''Fn族函数,n为迭代次数'''
    result = arg
    for i in range(n):
        result = func(result)
    return result



def __test_T2():
    pass
def __test_Fn():
    def f(x):
        return 2*x
    for i in range(10):
        print(Fn(f,i,1))


if __name__ == '__main__':
    __test_Fn()
    
