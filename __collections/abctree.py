from abc import ABC,abstractmethod
from typing import Iterator,Iterable
from __functools import T2_or

class AbstractTree(ABC):
    '''Abstract base class representing a tree structure'''

    #------------------Position class--------------------------------
    class AbstractPosition(ABC):
        '''An abstraction representing the location of a single element.'''
        @abstractmethod
        def element(self):
            '''return the element of this Position'''
            pass
        @abstractmethod
        def __eq__(self,other):
            '''Return True if other Position represent the same location'''
            pass
        def __ne__(self,other):
            '''Return True if other Position does not represent the same location'''
            return not(self == other)
    #------------------abstract methods----------------------------------
    @abstractmethod
    def __len__(self):
        '''Return the total number of elements in the tree'''
        pass
    
    @abstractmethod
    def root(self):
        '''Return root Position'''
        pass
    
    @abstractmethod
    def parent(self,p):
        '''Return Position's parent'''
        pass
    @abstractmethod
    def children(self,p)->Iterator[AbstractPosition]:
        '''Generate an iteration of elements of tree'''
        pass
    @abstractmethod
    def num_children(self,p):
        '''Return the number of the Position's children'''
        pass
    
    def is_root(self,p):
        '''Return True if Position is root'''
        return self.root == p
    def is_leaf(self,p):
        '''Return True if Position is leaf'''
        return self.num_children(p) == 0
    def is_empty(self):
        '''Return True if the number of elements in the tree is zero'''
        return len(self) == 0
    #-------------Tree's depth and height-----------------------
    def depth(self,p):
        '''Return the depth of the Position'''##Begin() == 0,Out() == self.is_root(p),Update(result,flag) == result + 1,self.parent(p)
        result = 0
        while not self.is_root(p):
            result += 1
            p = self.parent(p)
        return result 
    
    def height(self,p = None):##Begin() == 0,Out() == self.is_leaf(p),Update()_2 == result + 1,self.children(p)
        '''Return the height of the Position
        
        if p = None ,Return the height of the tree'''
        if p is None:
            return self.height(self.root())
        result = 0
        flags_ = [p]
        while not T2_or((self.is_leaf(flag) for flag in flags_)):
            result += 1
            flags = []
            for flag in flags_:
                flags.extend(self.children(flag))
            flags_ = flags
        return result
    
    #--------------树的遍历和查找算法-------------------------------
    def positions(self,way = 1):##
        match way:
            case 1:
                for p in self.preorder():
                    yield p
            case 2:
                for p in self.postorder():
                    yield p
            case _ :
                raise TypeError("方式不存在")
    def __iter__(self):
        for p in self.positions():
            yield p.element()
    def preorder(self):
        if not self.is_empty():
            for p in self._subtree__preorder(self.root()):
                yield p
    def _subtree__preorder(self,p)->Iterator[AbstractPosition]:##Begin() == leaf,Out() == is_None,Update(result,flag) == result.children,flag == flag.children,由于flags == results
        results_ = [p]
        while not T2_or((result is  None for result in results_)):
            results = []
            for result in results_:
                yield result
                results.extend(self.children(result))
            results_ = results

    def postorder(self):
        if not self.is_empty():
            for p in self._subtree__postorder(self.root()):
                yield p
    def _subtree__postorder(self,p)->Iterator[AbstractPosition]:##flag == result,Begin() == p0,Out() == is_p0,Update(result) == p.parent == p-1,#-------暂无重构必要
        for c in self.children(p):
            for other in self._subtree__postorder(c):
                yield other
        yield p
    
class AbstractBinaryTree(AbstractTree):
    '''Abstract base class representing a binary tree structure'''

    #---------------additional abstract method--------------------
    @abstractmethod
    def left(self,p):
        '''Return a Position representing p's left child
        
        Return None if the Position have not a left child'''
        pass

    @abstractmethod
    def right(self,p):
        '''Return a Position representing p's right child
        
        Return None if the Position have not a right child'''
    def sibling(self,p):
        '''Return a Position representing p's sibling(or None if no sibling).'''
        parent = self.parent(p)
        if parent is None:
            return None
        else:
            if p == self.left(parent):
                return self.right(parent)
            else:
                return self.left(parent)
    def children(self, p):
        if self.left(p) is not None:
            yield self.left(p)
        if self.right(p) is not None:
            yield self.right(p)
