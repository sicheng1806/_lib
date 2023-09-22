import operator
import time

class TimeoutError(RuntimeError):
    pass



def continue_until(time_out,
                  retry_time,
                  func,
                  value = True,
                  op = operator.eq,
                  **kwargs
                  ):
    '''如果不符合继续执行的条件(op(func(**kwargs),value))，
    则退出，为了防止死循环，可以设定time_out,为None时不设定超时条件'''
    def can_continue(result,value,op):
        return  op(result,value)
    if time_out is None:
        def flag():
            return True
    else:
        start_time = time.time()
        def flag():
            return (time.time()-start_time)<time_out
    while flag():
        result = func(**kwargs)
        time.sleep(retry_time)
        if not can_continue(result,value,op):
            return True

def wait_until(time_out,
               retry_time,
               func,
               value = True,
               op = operator.eq,
               **kwargs):
    '''反复运行知道满足停止条件(op(func(**kwargs),value)),
    为了防止死循环，可以设定time_out，如果time_out为None，则为堵塞函数'''
    def can_out(result,value,op):
        return op(result,value)
    def flag_1():
            return True
    def flag_2():
            if (time.time() - start_time) >= time_out:
                raise TimeoutError("Time out")
            return True
    if time_out is None:
        flag = flag_1
    else:
        start_time = time.time()
        flag = flag_2
    while flag():
        result = func(**kwargs)
        time.sleep(retry_time)
        if can_out(result,value,op):
            return True