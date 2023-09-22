from pywinauto.application import Application
from __pyauto import Work,Workspace,BaseActions
from pywinauto.controls import uiawrapper
import time,re,emoji
from __collections import StrTools
from pywinauto import mouse
from __functools import _timings
from comtypes import COMError



def scrollOver(ctrl:Workspace,direct_each = -8,count = None,retry_time = 0.4,time_out = 10):
    '''count 为None会滚动到ctrl的子类在限定条件下不再增加为止,此时retry_time将失效'''
    pos = ctrl.rectangle().mid_point()
    if count is not None: 
        for i in range(count):
            mouse.scroll(pos,wheel_dist=direct_each)
            time.sleep(retry_time)
        return True
    #args = (ctrl,direct_each,pos)
    def continue_scroll(time_out_):
        def is_increasing():
            '''翻页成功则返回True'''
            count = ctrl.control_count()
            mouse.scroll(pos,direct_each)
            if ctrl.control_count() > count:
                print("翻页成功")
                return True
        try:
            return _timings.wait_until(
                time_out_,
                0,
                is_increasing,
            )
        except _timings.TimeoutError:
            print("翻页失败")
            return False
    _timings.continue_until(
        None,
        retry_time,
        continue_scroll,
        time_out_ = time_out
    )
    
def is_text_match(text,match_text_re,module = "in"):
    '''匹配文字的综合方法'''
    match module:
        case "in":
            return match_text_re in text
        case _:
            raise ValueError("module must be one of in,")
def replace_text_to_clipboard(help_ctrl:uiawrapper.UIAWrapper,text):
    '''rule太复杂了所以不做为参数'''
    help_ctrl.set_focus()
    Pattern = re.compile(r"(?:[0-9.]+💰)|(?:💰[0-9.]+)")
    NUM = re.compile(r"[0-9]+[.]?[0-9]*")
    translation_tab = str.maketrans(dict(zip("() \n",["+9","+9",'',"{ENTER}"])))
    digits_mapping = str.maketrans(dict(zip("0123456789",[f"{{VK_NUMPAD{i}}}" for i in range(10)])))
    m_str_ = re.findall(Pattern,text)
    m_str = [re.sub(NUM,lambda x:str(eval(x.group())+5),str_) for str_ in m_str_]
    for str_,_str in zip(m_str_,m_str):
        text = text.replace(str_,_str)#转换为了含表情包但价格解决的字符串
    text = text.translate(translation_tab)#转换一些必须处理的字符
    emj_lst = emoji.emoji_list(text)
    index_ = [[item["match_start"],item["match_end"]] for item in emj_lst]
    index = []
    for i in index_:
        index.extend(i)
    output_lst = StrTools.split_index(text,index)
    for i in range(len(emj_lst)):
        emj_ = emj_lst[i]["emoji"]
        emj = ''
        for j in emj_:
            num_str = str(ord(j)).translate(digits_mapping)
            emj_j = "{VK_MENU down}"+num_str+"{VK_MENU up}"
            emj+= emj_j
        if index[0]:output_lst[2*i+1] = emj
        else: output_lst[2*i] = emj
    help_ctrl.TypeKeys("^a")
    for string in output_lst:
        help_ctrl.TypeKeys(string)
    help_ctrl.TypeKeys("^a^c")

    
    

def foreword_main(app:Application,direct_each = -1,count = None,retry_time = 0,time_out = 10,
                  scope:slice = None,
                  filename = None,mode = "all",
                  i = 0):
    '''step1: scroll :
    * **direct_each,count,retry_time,time_out**
    step2:foreword:
    * **scope**
    other:
    * **mode,filename**，
    mode: 
        * "all" scroll and foreword NOTE:will not use filename to read
        * "scroll" scroll NOTE will write in filename 
        * "forward" foreword,NOTE:filename must exist'''
    match mode:
        case "all" : 
            read_file = None
            write_file = filename
            i = 0
        case "foreword" : 
            count = -1
            if filename is None: raise TypeError("filename must exist to read")
            read_file = filename
            write_file = None
            i = 0
        case "scroll" : 
            if filename is None: raise TypeError("filename must exist to write")
            write_file = filename
            read_file = None
            direct_each = -10000
            retry_time = 0
            time_out = 30
            count = None
            i = 0
        case "continue":
            count = -1
            if filename is None: raise TypeError("filename must exist to read")
            read_file = filename
            write_file = None
        case _:
            raise TypeError("mode not exist")
    __scope = slice(0,scope.stop)
    space = Workspace(app.Dialog.wrapper_object())[20][3][4][0][0][0][0][0]
    button_flush = Workspace(app.Dialog.wrapper_object())[20][3][2]

    space_side = Workspace(Application().connect(title_re = ".*Notepad").window(title_re = ".*Notepad").wrapper_object())[4][0]

    #_________________________________________________________
    if count != -1:#是否去scroll
        scrollOver(space,direct_each,count,retry_time=retry_time,time_out=time_out)
        mouse.scroll(space.rectangle().mid_point(),1000000)
    if not read_file:
        buttons = space.findChildren(control_type = "Button",title = "转发",visible_only=False)
        button_indexes = [button[0] for button in buttons]
        if write_file:
            with open(write_file,'w') as f:
                f.write(str(button_indexes))
    else:
        with open(read_file,"r") as f:
            button_indexes = eval(f.read())
    if scope is not None:
        button_indexes = button_indexes[__scope]
        button_indexes_in = button_indexes[scope]
    if mode == "all":#刷新一下
        button_flush.ctrl.click_input()
        time.sleep(1)
        button_flush.ctrl.click_input()
        time.sleep(4)
        space = Workspace(app.Dialog.wrapper_object())[20][3][4][0][0][0][0][0]
    print("buttons准备完毕")
    #_________________________________________________________
    if mode != "scroll":
        def __foreword(button_indexes,button_indexes_in,mode,i = 0):
            y = space.rectangle().mid_point().y
            #flag_1 = True
            flag_2 = False
            num = 0
            if mode == "continue": 
                num = scope.start
                button_indexes = button_indexes[num:]
            for i0_ in button_indexes:
                try:
                    i0 = int(i0_[2:])
                    #移动button并点击
                    if flag_2:
                        _timings.wait_until(
                                10,0.5,
                                lambda :space.control_count() > 100
                            )
                        flag_2 = False
                    button = space[i0+i]
                    while not (button.element_info.control_type == "Button" and button.window_text() == "转发"):
                        i+=1
                        button = space[i0+i]
                    assert button.element_info.control_type == "Button"
                    if i0_ in button_indexes_in:
                        flag_2 = True
                        print(f"buttons[{i0}]转发开始")
                        BaseActions.makeVisible(button,y)#y
                        #button.draw_outline()
                        def is_clicked():
                            button.ctrl.click_input()
                            return space[0].element_info.control_type == "Edit"
                        #wait_util,加载成功
                        _timings.wait_until(
                                10,0.5,
                                is_clicked
                            )
                        if not is_text_match(space[0].ctrl.get_value(),match_text_re= "💰",module = "in"):
                            Workspace(app.Dialog.wrapper_object())[20][3][1].ctrl.click_input()
                        else:
                            text = space[0].ctrl.get_value()
                            replace_text_to_clipboard(space_side.ctrl,text)
                            space.set_focus()
                            space[0].ctrl.type_keys("^a^a^a^v")
                            def is_down_ok():
                                try:
                                    if space.findChild(control_type = "Button",title = "保 存"):
                                        return True
                                except:
                                    return False
                            _timings.wait_until(
                                40,0.5,
                                is_down_ok
                            )
                            button = space.findChild(control_type = "Button",title = "保 存")[1]
                            assert button.element_info.control_type == "Button"
                            button.ctrl.click_input()
                            
                            button.ctrl.click_input()
                    print(f"i0:{i0} i:{i} num:{num}")
                    num+=1
                except _timings.TimeoutError as e:
                    print(f"TimeoutError raised:{e}")
                    return ("TimeoutError",num,i,i0)
                except IndexError as e:
                    print(f"IndexError raise:{e}")
                    return ("IndexError",num,i,i0)
                except :
                    print(f"num:{num},i:{i}")
                    raise
            return True
            #wait_util,加载成功
        return __foreword(button_indexes,button_indexes_in,mode,i)
    return True

def re_start(direct_each = -1,count = None,retry_time = 0,time_out = 10,
                  scope:slice = None,
                  filename = None,mode = "all",
                  i = 0):
    def what_error(app,args):
        e_num_i_i0 = foreword_main(app,*args)
        if e_num_i_i0 is True:return True
        i0 = e_num_i_i0[-1]
        scope = args[4]
        scope = slice(e_num_i_i0[1],scope.stop,scope.step)
        i = e_num_i_i0[2]
        args = (direct_each,count ,retry_time ,time_out ,scope,filename,mode,i)
        dlg = Workspace(app.Dialog.wrapper_object())
        match e_num_i_i0[0]:
            case "TimeoutError":
                match dlg[20][3][3].window_text():
                    case "编辑":
                        return "编辑",args,i0
                    case "NiNi加盟专属相册":
                        return "NiNi加盟专属相册",args,i0
                    case _:
                        return "NiNi加盟专属相册",args,i0
            case "IndexError":
                return "must_scroll",args,i0
            case _:
                raise e_num_i_i0[0]
    app = Application(backend='uia').connect(title = "微商相册")
    args = (direct_each,count ,retry_time ,time_out ,scope,filename,mode,i)
    while True:
        match what_error(app,args):
            case ("NiNi加盟专属相册",x,i0):
                Workspace(app.Dialog.wrapper_object())[20][3][2].ctrl.click_input()
                args = x
            case ("编辑",x,i0):
                Workspace(app.Dialog.wrapper_object())[20][3][1].ctrl.click_input()
                args = x
            case("must_scroll",x,i0):
                def index_ok(i0,i):
                    space = Workspace(app.Dialog.wrapper_object())[20][3][4][0][0][0][0][0]
                    if space.control_count()>i0+i:
                        return True
                    mouse.scroll(space.rectangle().mid_point(),-1000)
                    return False
                
                args = x
                _timings.wait_until(
                    None,
                    0,
                    index_ok,
                    i0 = i0,
                    i = x[-1]
                )
                
            case True:
                return True
            case _ :
                raise Exception("not useful,just have funny")
        _timings.wait_until(
                                10,0.5,
                                lambda :Workspace(app.Dialog.wrapper_object())[20][3][4][0][0][0][0][0].control_count() > 100
                            )

if __name__ == '__main__':
    s = slice(636,None)
    re_start(scope=s,filename = "buttons.txt",mode = "continue",i = 853)
    #s = slice(0,None)
    #re_start(scope=s,filename="button(5 25).txt",mode= "scroll")
    #s = slice(300,None)
    #re_start(scope=s,filename="button(5 25).txt",mode="continue",i = 0)