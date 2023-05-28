from __collections.abctree import AbstractBinaryTree,AbstractTree
from typing import Iterable,Iterator
import copy
from __functools import T2_or


class LinkedBinaryTree(AbstractBinaryTree):
    '''Linked representation of a binary tree structure
    
    设计思路:对外界来说只有Tree和Position对象，对于一些方法为什么这样设计，以旁注的形式指出
    
    '''
    #------------node------------------------------
    class _Node(object):
        __slots__ = '_element','_parent','_left','_right'
        def __init__(self,element = None,parent = None,left = None,right = None) -> None:
            self._element = element
            self._parent = parent
            self._left = left
            self._right = right
    #-------------Position，node的包装--------------------------
    class Position(AbstractBinaryTree.AbstractPosition):
        '''An representation of Position'''

        def __init__(self,container,node:'LinkedBinaryTree._Node') -> None:
            '''Constructor'''
            self._container = container
            self._node = node
        def __repr__(self) -> str:
            node = self._node
            string = f'<position>:{node._element}'
            return string
        def element(self):
            return self._node._element
        def __eq__(self,other:'LinkedBinaryTree.Position'):
            return type(self) is type(other) and other._node is self._node
    #-------------method for position-------------------------
    def _validate(self,p:'LinkedBinaryTree.Position')->_Node:   #由于传入的p不一定时position类所以方法设置给tree
        '''如果p有效,return其node'''
        if not isinstance(p,self.Position):
            raise TypeError("p must be proper Position type")
        if p._container is not self:
            raise ValueError("p must belong to this container")
        if p._node._parent is p._node:
            raise ValueError("p is not longer valid")#?
        return p._node
    def _make_position(self,node):
        '''Return Position instance for given node(or None if no node)'''
        return self.Position(self,node) if node is not None else None
    #------------------method----------------------------
    def __init__(self) -> None:
        '''Create an empty binary tree'''
        self._root = None
        self._size = 0
    def __len__(self):
        return self._size
    def root(self):
        return self._make_position(self._root)
    def parent(self, p:Position):
        node = self._validate(p)
        return self._make_position(node._parent)
    def left(self,p):
        node = self._validate(p)
        return self._make_position(node._left)
    def right(self, p):
        node = self._validate(p)
        return self._make_position(node._right)
    def num_children(self, p):
        node = self._validate(p)
        count = 0
        if node._left is not None:
            count += 1
        if node._left is not None:
            count += 1
        return count
    #---------------二叉树的非公开更新方法-----------------
    def _add__root(self,e):
        '''Place this element at the empty root(or return Raise ValueError if tree nonempty)'''
        if self._root is not None : raise ValueError('Root exits')
        self._size = 1
        self._root = self._Node(e)
        return self._make_position(self._root)
    def _add__left(self,p,e):
        '''如果p没有left则将e添加为p的left，其他引发值错误'''
        node = self._validate(p)
        if node._left is not None :raise ValueError("p's left exits")
        self._size += 1
        node._left = self._Node(e,node)
        return self._make_position(node._left)
    def _add__right(self,p,e):
        '''如果p没有raise则将e添加为p的left，其他引发值错误'''
        node = self._validate(p)
        if node._right is not None :raise ValueError("p's right exits")
        self._size += 1
        node._right = self._Node(e,node)
        return self._make_position(node._right)
    def _replace(self,p,e):
        '''替换一个已经存在Position的元素，返回原来的元素'''
        node = self._validate(p)
        old = node._element
        node._element = e
        return old 
    def _delete(self,p):
        '''删除所在位置的节点，如果只有一个孩子的话，将所在位置替换
        
        放回所在位置的元素
        引发ValueError如果所在位置无效，或者p有两个孩子的话'''
        node = self._validate(p)
        if self.num_children(p) == 2: raise ValueError(" p has two children")
        child = node._left if node._left else node._right
        if child is not None:
            child._parent = node._parent
        if node is self._root:
            self._root = child
        else:
            parent = node._parent
            if node is parent._left:
                parent._left = child
            else:
                parent._right = child
        self._size -= 1
        node._parent = node #废节点
        return node._element
    def _attach(self,p,t1:'LinkedBinaryTree',t2:'LinkedBinaryTree')->None:
        '''Attach trees t1 and t2 as left and right subtrees of external 
        
        修改日志：当t1与自身相等时，程序对t1的修改会影响到自身'''
        node = self._validate(p)
        if not self.is_leaf(p):raise ValueError("position must be leaf")   
        if not type(self) is type(t1) is type(t2):
            raise TypeError("Tree types must match")
        if t1 is self:
            t1 = copy.deepcopy(t1)
        if t2 is self:
            t2 = copy.deepcopy(t2)
        self._size += len(t1) + len(t2)
        if not t1.is_empty():
            t1._root._parent = node
            node._left = t1._root
            t1._root = None
            t1._size = 0
        if not t1.is_empty():
            t1._root._parent = node
            node._right = t1._root
            t1._root = None
            t1._size = 0
    #------------------查找遍历算法-----------------------
    def breadthfrist(self):
        raise NotImplemented("广度遍历算法有待实现")
    def inorder(self):
        raise NotImplemented("中度遍历算法有待实现")
    
class LinkedTree(AbstractTree):
    '''Linked representation of a binary tree structure
    
    设计思路:对外界来说只有Tree和Position对象，对于一些方法为什么这样设计，以旁注的形式指出
    '''
    #------------node------------------------------
    class _Node(object):
        __slots__ = '_element','_parent','_children'
        def __init__(self,element = None,parent = None,children:Iterable['LinkedTree._Node'] = []) -> None:
            self._element = element
            self._parent = parent
            if isinstance(children,Iterable):
                self._children = list(children)
            else:
                self._children[children,]
    #-------------Position，node的包装--------------------------
    class Position(AbstractTree.AbstractPosition):
        '''An representation of Position'''

        def __init__(self,container,node:'LinkedBinaryTree._Node') -> None:
            '''Constructor'''
            self._container = container
            self._node = node
        def __repr__(self) -> str:
            node = self._node
            string = f'<position>:{node._element}'
            return string
        def element(self):
            return self._node._element
        def __eq__(self,other:'LinkedBinaryTree.Position'):
            return type(self) is type(other) and other._node is self._node
    #-------------method for position-------------------------
    def _validate(self,p:'LinkedBinaryTree.Position')->_Node:   #由于传入的p不一定时position类所以方法设置给tree
        '''如果p有效,return其node'''
        if not isinstance(p,self.Position):
            raise TypeError("p must be proper Position type")
        if p._container is not self:
            raise ValueError("p must belong to this container")
        if p._node._parent is p._node:
            raise ValueError("p is not longer valid")#?
        return p._node
    def _make_position(self,node):
        '''Return Position instance for given node(or None if no node)'''
        return self.Position(self,node) if node is not None else None
    #------------------method----------------------------
    def __init__(self) -> None:
        '''Create an empty binary tree'''
        self._root = None
        self._size = 0
    def __len__(self):
        return self._size
    def root(self):
        return self._make_position(self._root)
    def parent(self, p:Position):
        node = self._validate(p)
        return self._make_position(node._parent)
    def children(self, p):
        node = self._validate(p)
        for child in node._children:
            yield self._make_position(child)
    
    def num_children(self, p):
        node = self._validate(p)
        return len(node._children)
    
    #---------------二叉树的非公开更新方法-----------------
    def _add__root(self,e):
        '''Place this element at the empty root(or return Raise ValueError if tree nonempty)'''
        if self._root is not None : raise ValueError('Root exits')
        self._size = 1
        self._root = self._Node(e)
        return self._make_position(self._root)
    def _add__child(self,p:Position,e):
        "给position添加了一个孩子"
        node = self._validate(p)
        child = self._Node(e)
        self._size += 1
        node._children.append(child)
        child._parent = node 
        return self._make_position(child)
    def _add__children(self,p:Position,iterable):
        '''给position添加许多孩子'''
        node = self._validate(p)
        children = [self._Node(e) for e in iterable]
        self._size += len(children)
        node._children.extend(children)
        for child in children:
            child._parent = node
        return [self._make_position(child) for child in children]
    
    
    def _replace(self,p,e):
        '''替换一个已经存在Position的元素，返回原来的元素'''
        node = self._validate(p)
        old = node._element
        node._element = e
        return old 
    def _delete(self,p):
        '''删除所在位置的节点，如果只有一个孩子的话，将所在位置替换
        
        放回所在位置的position
        '''
        node = self._validate(p)
        node._parent = node
        return self._make_position(node)
    
    def _attach(self,p,trees:Iterable['LinkedTree'])->None:
        '''为所在位置依次添加许多树'''
        node = self._validate(p)
        if  isinstance(trees,type(self)):
            if trees is self: trees = copy.deepcopy(trees)
            self._size += trees._size
            node._children.append(trees._root)
            trees._root._parent = node
            trees._size = 0
            #trees._root = None
        if isinstance(trees,Iterable):
            for tree in trees:
                 if not isinstance(tree,type(self)): raise TypeError("must be similar tree type")
        for tree in trees:
            if tree is self:
                tree = copy.deepcopy(tree)
        self._size += sum([len(tree) for tree in trees])
        children = [tree._root for tree in trees]
        node._children.extend(children)
        for child in children:
            child._parent = node
        #for tree in trees: tree._size = 0
        return self._size
    #-----------查找遍历算法------------------------
    def breadthfirst(self):
        raise NotImplemented("广度优先算法暂不支持")
    def depthOrder(self):
        if not self.is_empty():
            for p in self._subtree__depthOrder(self.root()):
                yield p
    def _subtree__depthOrder(self,p)->Iterator[Position]:##Begin() == leaf,Out() == is_None,Update(result,flag) == result.children,flag == flag.children,由于flags == results
        results_ = [p]
        yield self._make_position(self._Node('\t'))
        while not T2_or((result is  None for result in results_)):
            results = []
            for result in results_:
                yield result
                results.extend(self.children(result))
            yield self._make_position(self._Node('\n'))
            results_ = results

    def _depth_children(self,depth,root:Position = None)->Iterator[Position]:## 
        '''抛出相对position深度为depth的孩子们'''
        if depth < 0: raise ValueError("depth must lagger than or equal to 0")
        children_ = [self.root() if root is None else root]
        for i in range(1,depth+1):
            children = []
            for child in children_:
                children.extend(self.children(child))
            children_ = children
        for child in children_:
            yield child
    #---------------基于遍历算法的方法----------------------
    def __repr__(self) -> str:
        '''基于非递归实现，关系暂时展现不出来'''
        string = ''
        for p in self.depthOrder():
            string += str(p.element())+'\t'
        return string


def __test_LinkedBinaryTree():
    abt = LinkedBinaryTree()

    root = abt._add__root("root")
    p1 = abt._add__left(root,"11")
    p2 = abt._add__right(root,"12")
    abt._attach(p1,abt,abt)
    abt._attach(p2,abt,abt)

    for p in abt.positions(2):
        print(p.element())
    print("end")
def __test_LinkedTree():
    tree = LinkedTree()

    root = tree._add__root("root")
    #print(root)
    ps = tree._add__children(root,(11,12,13,14))
    tree1 = LinkedTree()
    tree1._add__root("root1")
    tree1._add__children(tree1.root(),(21,22,23,24))
    tree._attach(ps[0],tree1)
    #print(p11,p12,p13,p14)
    print(tree._size)
    for i in tree.positions():
        print(i.element())
    
    #print(tree)
def __tested3():
    tree = LinkedTree()
    tree._add__root("root")
    ps = tree._add__children(tree.root(),(11,12,13,14))
    tree1 = LinkedTree()
    tree1._add__root(0)
    p = tree1.root()
    for i in range(1,1001):
        p = tree1._add__child(p,i)
    print(tree.height(ps[0]))
    for p in ps:
        tree._add__children(p,(21,22,23,24))
    print(tree.height(ps[0])) 
    #print(tree.depth())
    print(tree.height())
if __name__ == '__main__':
    __test_LinkedTree()