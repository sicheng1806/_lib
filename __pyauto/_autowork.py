
#-------------------------------------
from typing import Iterable
from __collections import FixedList
from __pyauto.basestructures import Workspace

#---------------------------------

class Work:
    '''一个包含自动化行为的类
    
    example:
    >>> #获取工作区workspace
    >>> pass
    >>> myWork = Work(workspace)
    >>> #设置Actions(行为池)
    >>>    #获取行为
    >>> Action1 = myWork.createAction(can_accept,can_start,action,send_order)#Action类的工厂函数
    >>> myWork.addAction(name = "行为1",Action = Action1)
    >>> ::或者
    >>> Action1 = ...
    >>> Action2 = ...
    >>> Action3 = ...
    >>> Action_dict = dict(zip(["name1","name2","name3"],[Action1,Action2,Action3]))
    >>> myWork.extendAction(Action_dict)
    >>> ::或者
    >>>  _actions = otherWork.getActions()
    >>> myWork.extendAction(_actions)
    >>> #设置行为
    >>> #设置参数池
    >>> initialPool = dict(zip(["name1","name2","name3"],[
        FixedList([kargs1,kargs2,kargs3,kargs4]),
        FixedList([kargs1,kargs2,kargs3,kargs4]),
        FixedList([kargs1,kargs2,kargs3,kargs4]),
        FixedList([kargs1,kargs2,kargs3,kargs4])
        ]))
    >>> argPool1 = myWork.createPool(initialPool)
    >>>  #设置参数的更新方法
    >>> :: 定义update00,update01,update02,update03
    >>> argPool1.setUpdate(pos = ("name1",0),update = update00)
    >>> argPool1.setUpdate(dict(zip([("name1",1),("name1",1),("name1",1)],[update01,update02,update03])))  
    >>> movement1 = myWork.createMove(argPool = argPool1)
    >>>  #开始工作行为
    >>> myWork.startMove(movement1)
    '''

    def __init__(self,workspace = None) -> None:
        if not isinstance(workspace,Workspace):workspace = Workspace(Workspace)
        self.workspace = workspace
        self.actions = {}
    def getWorkspace(self):
        return self.workspace
    def setWorkspace(self,workspace):
        self.workspace = workspace
    def createAction(self,can_accept,can_start,action,send_order):
        return Action(can_accept,can_start,action,send_order)
    def setDefaultAction(self,name,Action):
        return self.actions.setdefault(name,Action)
    def updateAction(self,Action_dict):
        return self.actions.update(Action_dict)
    def createPool(self,initialPool):
        return ArgPool(initialPool,self)
    def createMove(self,argPool):
        return Movement(argPool,self)
    def startMove(self,movement):
        return movement.startMove()

class Action:
    '''一个动作:
    
    提出动作的两种实现模式，第一种是根据位置实现鼠标和键盘输入，

    第二种是根据对象实现键盘输入，第二种对象会自动使自己可视化，然后执行相应操作
    '''
    def __init__(self,action,can_accept = None,can_start = None,send_order = None) -> None:
        action = action
        can_accept = can_accept if can_accept else Action.dft_can_start
        can_start = can_start if can_start else Action.dft_can_start
        send_order = send_order if send_order else Action.dft_send_order
        self.data = dict(zip(["can_accept","can_start","action","send_order"],
                             [can_accept,can_start,action,send_order]
                             ))
    def set_can_accept(self,can_accept):
        self.data["can_accept"] = can_accept
    def set_can_start(self,can_start):
        self.data["can_start"] = can_start
    def set_send_order(self,send_order):
        self.data["send_order"] = send_order
    def __getitem__(self,key):
        if key not in self.data.keys(): raise KeyError("没有key值")
        return self.data[key]            
    def __setitem__(self,key,value):
        if key not in self.data.keys(): raise KeyError("没有key值")
        if not isinstance(value,callable):raise TypeError("value must be callable")
        self.data[key] = value
    @classmethod
    def dft_can_start(cls):
        return True,None
    @classmethod
    def dft_can_accept(cls):
        return True,None
    @classmethod
    def dft_send_order(cls):
        return ["END"],None
    #下面是一系列的baseAction
    
class ArgPool:
    def __init__(self,initialPool:dict,work:Work) -> None:
        '''initialPool = {'name':FixedList(_len = 4)} same like updates'''
        self.pool = initialPool
        self.work = work
        self.updates = {}
        keys = self.pool.keys()
        for key in keys:
            self.updates.setdefault(key,FixedList([ArgPool.dft_update]*4))

    @classmethod
    def dft_update(cls,value):
        return None
    def setUpdate(self,pos:tuple[str,str],update:callable):
        '''pos = ("name1","action")'''
        #合法pos
        if not isinstance(update,callable):raise TypeError("update must be callable")
        key = pos[0]
        if key not in self.updates:
            raise ValueError("key not exist")
        match pos[1]:
            case "can_accept":
                self.updates[key][0] = update
            case "can_start":
                self.updates[key][1] = update
            case "action":
                self.updates[key][2] = update
            case "send_order":
                self.updates[key][3] = update
            case _ :
                raise ValueError("pos[1] must be valid")
    
    def setUpdates(self,name:str,update_value:FixedList[callable]):
        if not isinstance(update_value,Iterable): raise TypeError("update_value must be Iterable")
        if len(update_value) != 4: raise TypeError("len wrong")
        for item in update_value:
            if not isinstance(item,callable):TypeError("update_value")
        if not isinstance(name,str) :raise TypeError("name must be str")
        if name not in self.pool:
            raise ValueError("key not exist")
        self.updates[name] = update_value

    def update(self,pos,result):
        '''根据result更新参数池,特殊的当value为None时不更新值'''
        value = self.updates[pos[0]][pos[1]](result)
        if value is not None:
            self.pool[pos[0]][pos[1]] = value

class Movement:
    def __init__(self,argPool:ArgPool,work:Work):
        if not isinstance(argPool,ArgPool): argPool = ArgPool(argPool)
        self.argPool = argPool
        self.work = work
    
    def greek(self):
        _order = ["START"]
        while _order:
            _name = "END"
            for name in _order:
                #接受否------------------------------------
                kargs = self.argPool[name][0]
                result = self.work.actions[name]["can_accept"](**kargs)
                self.argPool.update((name,0),result[1])
                #--------------------------------------
                if result[0] :
                    _name = name
                    break
            #等待可以开始----------------------------------------
            kargs = self.argPool[_name][1]
            result = self.work.actions[_name]["can_start"](**kargs)
            self.argPool.update((_name,1),result[1])
            #执行动作----------------------------------
            kargs = self.argPool[_name][2]
            result=self.work.actions[_name]["action"](**kargs)
            self.argPool.update((_name,2),result[1])
            #发送指令------------------------------------------
            kargs = self.argPool[_name][3]
            result = self.work.actions[_name]["send_order"](**kargs)
            self.argPool.update((_name,2),result[1])
            _order = result[0]

    def startMove(self):
        return self.greek()

    def setUpdate(self,pos:tuple[str,str],update:callable):
        return self.argPool.setUpdate(pos,update)
    def setUpdates(self,name:str,update_value:FixedList[callable]):
        return self.argPool.setUpdates(name,update_value)



            



def test_work0():
    workspace = None
    myWork = Work(workspace)
    #设置Actions(行为池)
        #获取行为
    can_accept,can_start,action,send_order = None,None,None,None
    Action1 = myWork.createAction(can_accept,can_start,action,send_order)
    Action2 = myWork.createAction(can_accept,can_start,action,send_order)
    Action3 = myWork.createAction(can_accept,can_start,action,send_order)
    Action_dict = dict(zip(["name1","name2","name3"],[Action1,Action2,Action3]))
    myWork.extendAction(Action_dict)
    #设置行为
        #设置参数池
    kargs1,kargs2,kargs3,kargs4 = None,None,None,None
    initialPool = dict(zip(["name1","name2","name3"],
    [
    FixedList([kargs1,kargs2,kargs3,kargs4]),
    FixedList([kargs1,kargs2,kargs3,kargs4]),
    FixedList([kargs1,kargs2,kargs3,kargs4]),
    FixedList([kargs1,kargs2,kargs3,kargs4])
    ]
    ))
    #设置参数的更新方法
    movement1 = myWork.createMove(argPool = initialPool)
    update00,update01,update02,update03 = None,None,None,None
    movement1.setUpdate(pos = ("name1",0),update = update00)
    movement1.setUpdate(dict(zip([
    ("name1",1),("name1",1),("name1",1)
    ],[
    update01,update02,update03
    ])))  
    #开始工作行为
    myWork.startMove(movement1)

def test_work1():
    workspace = None
    myWork = Work(workspace)
    #设置Actions(行为池)
        #获取行为
    can_accept,can_start,action,send_order = None,None,None,None
    action1 = myWork.createAction(can_accept,can_start,action,send_order)
    myWork.setDefaultAction("name1",action1)
    #
    myWork.actions["name1"]["action"]()

if __name__ == '__main__':
    pass

    