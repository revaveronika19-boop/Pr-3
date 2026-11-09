"""Метапрограмування та шаблони проектування."""
from functools import wraps
from time import perf_counter
from abc import ABC, abstractmethod
class PluginMeta(type):
    registry = {}
    def __new__(mcls, name, bases, attrs):
        cls = super().__new__(mcls, name, bases, attrs)
        if bases:
            if not all(k in attrs for k in ('plugin_name','version')):
                raise TypeError('Потрібні plugin_name та version')
            mcls.registry[attrs['plugin_name']] = cls
        return cls
class BasePlugin(metaclass=PluginMeta):
    pass
class Upper(BasePlugin):
    plugin_name='upper'; version='1.0'
    def execute(self, s): return s.upper()
class Reverse(BasePlugin):
    plugin_name='reverse'; version='1.0'
    def execute(self, s): return s[::-1]
class Length(BasePlugin):
    plugin_name='length'; version='1.0'
    def execute(self, s): return str(len(s))
class Field:
    def __init__(self, expected): self.expected=expected
    def __set_name__(self, owner, name): self.name='_'+name
    def __get__(self, obj, owner): return self if obj is None else getattr(obj,self.name,None)
    def __set__(self,obj,value):
        if not isinstance(value,self.expected): raise TypeError('Неправильний тип')
        setattr(obj,self.name,value)
class Config:
    title=Field(str)
    def __init__(self,title): self.title=title

def log_calls(fn):
    @wraps(fn)
    def inner(*args,**kwargs):
        start=perf_counter(); result=fn(*args,**kwargs)
        print('Виклик',fn.__name__,'час',round(perf_counter()-start,6))
        return result
    return inner
@log_calls
def calculate(n): return sum(i*i for i in range(n))
class Singleton:
    _instance=None
    def __new__(cls):
        if cls._instance is None: cls._instance=super().__new__(cls)
        return cls._instance
class Factory:
    @staticmethod
    def create(name): return PluginMeta.registry[name]()
class Observable:
    def __init__(self): self.observers=[]
    def subscribe(self,callback): self.observers.append(callback)
    def notify(self,value):
        for callback in self.observers: callback(value)
class Strategy:
    def __init__(self, operation): self.operation=operation
    def apply(self, data): return self.operation(data)
def main():
    print('Реєстр:',list(PluginMeta.registry))
    for name in PluginMeta.registry: print(name,Factory.create(name).execute('Python'))
    print('Дескриптор:',Config('Налаштування').title)
    try: Config(123)
    except TypeError as e: print('Валідація:',e)
    print('Декоратор:',calculate(1000))
    print('Singleton:',Singleton() is Singleton())
    events=Observable(); events.subscribe(lambda x: print('Observer:',x)); events.notify('оновлено')
    print('Strategy:',Strategy(lambda x: sorted(x,reverse=True)).apply([3,1,2]))
if __name__ == '__main__': main()
