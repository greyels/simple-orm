#! /mnt/c/PP/python/simple_orm/venv/bin/python3

from simple_orm import *

class Client(Model):
    name = CharCol()
    age = IntCol()
    status = CharCol()

Client.create_table()

bob = Client(name='Bob', age=13, status='Frozen')
john = Client(name='John', age=56, status='Active')

bob.read()
print('name', bob.name, type(bob.name))
print('age', bob.age, type(bob.age))
print('status', bob.status, type(bob.status))

john.read()
print('name', john.name, type(john.name))
print('age', john.age, type(john.age))
print('status', john.status, type(john.status))

bob.update(name='Bobby', age=21, status='Suspended')

bob.read()
print('name', bob.name, type(bob.name))
print('age', bob.age, type(bob.age))
print('status', bob.status, type(bob.status))

bob.delete()
john.delete()
