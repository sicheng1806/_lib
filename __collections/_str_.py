from collections.abc import Iterable


class StrTools:
    '''字符串的工具类'''
    @staticmethod
    def split_index(string:str,iterable:Iterable[int]) -> list[str]:
        '''按索引分割字符串'''
        def is_valid(iterable:Iterable[int]):
            iterable = list(iterable)
            if iterable[0] != 0:
                iterable.insert(0,0)
            for i in range(1,len(iterable)):
                if not isinstance(iterable[i],int):raise TypeError("note::Iterable[int]")
                if iterable[i-1] > iterable[i]:raise TypeError("note::iterable must increase")
            return iterable
        if not isinstance(string,str):raise TypeError("note::str")
        iterable = is_valid(iterable)
        str_lst = []
        for i in range(len(iterable)):
            if i == len(iterable)-1: 
                str_lst.append(string[iterable[i]:])
                continue
            str_lst.append(string[iterable[i]:iterable[i+1]])
        return str_lst
        












if __name__ == '__main__':
    print(StrTools.split_index("HelloWorldComeToMySchool",[0,5,10,14,16]))