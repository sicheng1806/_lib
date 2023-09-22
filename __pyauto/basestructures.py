from pywinauto import mouse,Desktop
from pywinauto.controls import uiawrapper
from pywinauto.findwindows import ElementNotFoundError,ElementAmbiguousError
from pywinauto.win32structures import POINT
from pywinauto import timings
from pywinauto import uia_defines
from pywinauto import win32defines
from pywinauto import uia_defines
import time,re



class BaseActions:
    '''提供一些便捷函数'''
    @staticmethod
    def makeVisible(ctrl:uiawrapper.UIAWrapper,y:int = None):
        '''通过鼠标的滚动使控件变得可见
        '''
        ctrl.set_focus()
        if y is not None:
            def is_over():
                if ctrl.rectangle().top <= y and y <= ctrl.rectangle().bottom:
                    return True
                dist = (y-ctrl.rectangle().mid_point().y)//150+1
                mouse.scroll(ctrl.rectangle().mid_point(),dist)
            try:
                timings.wait_until(1,
                                0.1,
                                is_over)
            except timings.TimeoutError:
                pass
            
                
            

    @staticmethod
    def control_from_point(ctrl:uiawrapper.BaseWrapper,point:POINT|tuple[int,int],depth = 1,title_re:str = None,re_module:str = "fullmatch",
                     control_type:str = None, class_name:str = None, title:str=None,action = False,time_sleep = 0.5):
        '''从指定位置获取控件,只能获取可视控件'''
        zip_children = BaseActions.findChildren(ctrl,depth=depth,title_re=title_re,re_module=re_module,control_type=control_type,class_name=class_name,title=title)
        def __point_belongTo(ctrl,point,time_sleep):
            if action:
                mouse.move(point)
                ctrl.draw_outline()
                time.sleep(time_sleep)
            rect = ctrl.rectangle()
            result = True
            if point[0]<=rect.left or point[0]>=rect.right:
                result = False
            if point[1]<=rect.top or point[1] >= rect.bottom:
                result = False
            return result
        zip_children = [zip_child for zip_child in zip_children if __point_belongTo(zip_child[1],point,time_sleep)]
        return zip_children
    @staticmethod
    def showChildren(ctrl:uiawrapper.BaseWrapper,visible_only = True,time_sleep = 1,action = True,depth = 1,
                    title_re:str = None,re_module:str = "fullmatch",
                    control_type:str = None, class_name:str = None, title:str=None,iface = None):
        '''可视化展示子类，并输入其相关参数'''
        children = BaseActions.findChildren(ctrl,depth,visible_only,title_re,re_module,control_type,class_name,title,iface)
        s = "child:[{0}]; (control_type:[{1}]); class_name:[{2}]; rectangle:[{3}]; is_visible:[{4}]; handle:[{5}];window_text:<{6}>"
        for i in range(len(children)):
            child = children[i][1] 
            print(s.format(children[i][0],child.element_info.control_type,child.class_name(),child.rectangle(),child.is_visible(),child.handle,child.window_text()))
            if action:
                child.draw_outline()
                mouse.move(child.rectangle().mid_point())
                time.sleep(time_sleep)

    @staticmethod
    def findChildren(ctrl:uiawrapper.BaseWrapper ,depth:int  = 1,
                     visible_only = True,title_re:str = None,re_module:str = "fullmatch",
                     control_type:str = None, class_name:str = None, title:str=None
                     ,iface = None)->list[tuple[str,uiawrapper.BaseWrapper]]:
        '''返回符合条件的子构件，返回值中str为位置

        * **re_module** 在title_re 设定后生效，可以为"fullmatch","match","search"
        '''
        def __getChildren(zip_children_:list[tuple[str,uiawrapper.BaseWrapper]])->list[tuple[str,uiawrapper.BaseWrapper]]:
            _zip_children = []
            for zip_child_ in zip_children_:
                zip_children = BaseActions.__zip_children(zip_child_[1])
                zip_children = [(zip_child_[0]+zip_child[0][1:],zip_child[1]) for zip_child in zip_children]
                _zip_children.extend(zip_children)
            return _zip_children
        sum_children = []
        zip_children_ = [('0 ',ctrl)]
        for depth in range(0,depth):
            zip_children_ = __getChildren(zip_children_)
            sum_children.extend(zip_children_)
        #--过滤-------
        if visible_only:
            sum_children = [zip_child for zip_child in sum_children if zip_child[1].is_visible()]
        if title:
            sum_children = [zip_child for zip_child in sum_children if zip_child[1].window_text() == title]
        if control_type:
            sum_children = [zip_child for zip_child in sum_children if zip_child[1].element_info.control_type == control_type]
        if class_name:
            sum_children = [zip_child for zip_child in sum_children if zip_child[1].class_name() == class_name]
        if title_re :
            def match_title(title,title_re,module = "fullmatch"):
                        pattern = re.compile(title_re)
                        match module:
                            case "fullmatch":
                                result = True if re.fullmatch(pattern,title) else False
                            case "match":
                                result = True if re.match(pattern,title) else False
                            case "search": 
                                result = True if re.search(pattern,title) else False
                            case _ :
                                raise TypeError("re_module must be one of 'fullmatch','match','search'")
                        return result 
            sum_children = [zip_child for zip_child in sum_children if match_title(zip_child[1].window_text(),title_re,re_module)]
        if iface:
            sum_children = BaseActions.iface_filter(sum_children,iface)
        return sum_children
    
    @staticmethod
    def findChild(ctrl:uiawrapper.BaseWrapper ,depth:int  = 1,
                     visible_only = True,title_re:str = None,re_module:str = "fullmatch",
                     control_type:str = None,class_name:str = None, title:str=None,
                     iface = None):
        zip_children = BaseActions.findChildren(ctrl,depth,visible_only,title_re,re_module,control_type,class_name,title,iface)
        if not zip_children: raise ElementNotFoundError("Not control match")
        if len(zip_children) > 1: raise ElementAmbiguousError(f"{len(zip_children)} control found")
        return zip_children[0]

    @staticmethod
    def __zip_children(ctrl:uiawrapper.BaseWrapper)->list[tuple[str,uiawrapper.BaseWrapper]]:
        '''放回一个打包好位置和控件的列表'''
        children = ctrl.children()
        pos = ['0'+str(i)+' ' for i in range(0,len(children))]
        return list(zip(pos,children))

    @staticmethod
    def iface_filter(zip_children:list[tuple[str,uiawrapper.UIAWrapper]],iface:str):
        '''iface展示只支持scroll'''
        def is_ok(ctrl:uiawrapper.UIAWrapper,iface):
            match iface:
                case "scroll":
                    try:
                        return ctrl.iface_scroll.CurrentVerticallyScrollable
                    except uia_defines.NoPatternInterfaceError:
                        return False
                case _ :
                    raise ValueError("iface must be one of iface")
        zip_children = [zip_child for zip_child in zip_children if is_ok(zip_child[1],iface)]
        return zip_children

    @staticmethod
    def get_child_by_index(space:"Workspace",index:str)->"Workspace":
        '''index的形式为"0 1 2 3"'''
        lst = index.split()
        lst = [int(i) for i in lst[1:]]
        print(lst)
        child = space
        for i in lst:
            child = child[i]
        return child

class Workspace:
    '''BaseWrapper类的打包，提供了一些来自BaseAction的方法，__getitem__方法
    '''
    #___________________________________________
    def __init__(self,ctrl:uiawrapper.UIAWrapper):
        if not isinstance(ctrl,uiawrapper.BaseWrapper): raise TypeError("ctrl must be BaseWrapper")
        self.ctrl = ctrl
        self.backend = self.ctrl.backend
        self.appdata = self.ctrl.appdata
        #self.can_be_label = self.ctrl.can_be_label
        self.class_name = self.ctrl.class_name()
        self.element_info = self.ctrl.element_info
        self.handle = self.ctrl.handle
        #self.window_text = self.ctrl.window_text()
        self.writable_props = self.ctrl.writable_props
        self.friendly_class_name = self.ctrl.friendly_class_name()
        self.control_id = self.ctrl.control_id()
        self.process_id = self.ctrl.process_id()
    def showChildren(self,ctrl:uiawrapper.BaseWrapper = None,visible_only = True,time_sleep = 1,action = True,depth = 1,title_re:str = None,re_module:str = "fullmatch",
                    control_type:str = None, class_name:str = None, title:str=None,iface = None):
        if ctrl is None: ctrl = self.ctrl
        if isinstance(ctrl,Workspace): ctrl = ctrl.ctrl
        return BaseActions.showChildren(ctrl,visible_only,time_sleep,action,depth,title_re,re_module,control_type,class_name,title,iface)
    def mackVisible(self,ctrl):
        if isinstance(ctrl,Workspace): ctrl = ctrl.ctrl
        return BaseActions.mackVisible(ctrl)
    def findChildren(self,ctrl:uiawrapper.BaseWrapper = None ,depth:int  = 1,visible_only = True,title_re:str = None,re_module:str = "fullmatch",
                     control_type:str = None, class_name:str = None, title:str=None,
                     iface:str = None):
        if ctrl is None: ctrl = self.ctrl
        if isinstance(ctrl,Workspace): ctrl = ctrl.ctrl
        args = (ctrl,depth,visible_only,title_re,re_module,control_type,class_name, title,iface)
        return  [(child[0],Workspace(child[1])) for child in BaseActions.findChildren(*args)]  
    def findChild(self,ctrl:uiawrapper.BaseWrapper = None ,depth:int  = 1,visible_only = True,title_re:str = None,re_module:str = "fullmatch",
                     control_type:str = None, class_name:str = None, title:str=None,iface = None):
        if ctrl is None: ctrl = self.ctrl
        if isinstance(ctrl,Workspace): ctrl = ctrl.ctrl
        args = (ctrl,depth,visible_only,title_re,re_module,control_type, class_name, title,iface)
        zip_child = BaseActions.findChild(*args)
        return (zip_child[0],Workspace(zip_child[1]))
    def __getitem__(self,key)->"Workspace":
        if isinstance(key,slice) or isinstance(key,int):
            return Workspace(self.ctrl.children()[key])
        elif isinstance(key,str):
            return BaseActions.get_child_by_index(self,key)
        else:
            raise TypeError("key must be slice or str")
    
    
    #------------------------------------------
    def is_visible(self):
        return self.ctrl.is_visible()
    def is_enabled(self):
        return self.ctrl.is_enabled()
    def was_maximized(self):
        return self.ctrl.was_maximized()
    def rectangle(self):
        return self.ctrl.rectangle()
    def client_to_screen(self,client_point):
        return self.ctrl.client_to_screen(client_point)
    def is_dialog(self):
        return self.ctrl.is_dialog()
    def parent(self):
        return Workspace(self.ctrl.parent())
    def root(self):
        return self.ctrl.root()
    def top_level_parent(self):
        return Workspace(self.ctrl.top_level_parent())
    def texts(self):
        return self.ctrl.texts()
    def children(self,process=None, class_name=None, title=None, 
                 control_type=None,content_only=None):
        children =  self.ctrl.children(process = process,class_name = class_name,title = title,
                                control_type = control_type,content_only = content_only)
        return [Workspace(child) for child in children]
    def iter_children(self,process=None, class_name=None, title=None, 
                 control_type=None,content_only=None):
        for child in self.ctrl.iter_children(process = process,class_name = class_name,title = title,control_type = control_type,content_only = content_only):
            yield Workspace(child)
    def descendants(self,process=None, class_name=None, title=None, control_type=None,
                        content_only=None):
        descendants =  self.ctrl.descendants(process = process,class_name = class_name,title = title,
                                control_type = control_type,content_only = content_only)
        return [Workspace(descendant) for descendant in descendants]
    def iter_descendants(self,process=None, class_name=None, title=None, control_type=None,
                        content_only=None):
        for child in  self.ctrl.iter_descendants(process = process,class_name = class_name,title = title,
                                control_type = control_type,content_only = content_only):
            yield Workspace(child)
    def __repr__(self):
        ''' Workspace'''
        s = "<__pyauto._autowork.Workspace>:(control_type:[{0}]); class_name:[{1}]; rectangle:[{2}]; is_visible:[{3}]; handle:[{4}];window_text:<{5}>"
        return s.format(self.element_info.control_type,self.class_name,self.rectangle(),self.is_visible(),self.handle,self.window_text())
    def window_text(self):
        return self.ctrl.window_text()
    def control_count(self):
        return self.ctrl.control_count()
    def capture_as_image(self, rect=None):
        return self.ctrl.capture_as_image(rect)
    def get_properties(self):
        return self.ctrl.get_properties()
    def draw_outline(
        self,
        colour='green',
        thickness=2,
        fill=win32defines.BS_NULL,
        rect=None):
        return self.ctrl.draw_outline(colour=colour,thickness=thickness,fill=fill,rect=rect)
    def is_child(self, parent:uiawrapper.BaseWrapper):
        if isinstance(parent,Workspace): parent = parent.ctrl
        return self.ctrl.is_child(parent)
    def __eq__(self, other):
        if isinstance(other,Workspace): other = other.ctrl
        return self.ctrl.__eq__(other)
    def __ne__(self, other):
        if isinstance(other,Workspace): other = other.ctrl
        return self.ctrl.__ne__(other)
    def verify_actionable(self):
        return self.ctrl.verify_actionable()
    def verify_enabled(self):
        return self.ctrl.verify_enabled()
    def verify_visible(self):
        return self.ctrl.verify_visible()
    def wait_for_idle(self):
        return self.ctrl.wait_for_idle()
    def set_focus(self):
        return self.ctrl.set_focus()

