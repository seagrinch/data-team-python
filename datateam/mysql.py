#!/usr/bin/env python
# coding=utf-8
# Partially adapted from https://github.com/nestordeharo/mysql-python-class

import MySQLdb, sys

class MysqlPython(object):
  """ Python Class for connecting to the MySQL server """

  __instance   = None
  __host       = None
  __user       = None
  __password   = None
  __database   = None
  __socket     = None
  __session    = None
  __connection = None


  def __new__(cls, *args, **kwargs):
    if not cls.__instance or not cls.__database:
      cls.__instance = super(MysqlPython, cls).__new__(cls,*args,**kwargs)
    return cls.__instance


  def __init__(self, host='localhost', user='root', password='', database='', socket=''):
    self.__host     = host
    self.__user     = user
    self.__password = password
    self.__database = database
    self.__socket   = socket


  def __open(self):
    try:
      cnx = MySQLdb.connect(
        host   = self.__host, 
        user   = self.__user, 
        passwd = self.__password, 
        db     = self.__database, 
        unix_socket = self.__socket,
        local_infile = 1,
        charset='utf8')
      self.__connection = cnx
      self.__session    = cnx.cursor(cursorclass=MySQLdb.cursors.DictCursor) #
    except MySQLdb.Error as e:
      print "Error %d: %s" % (e.args[0],e.args[1])


  def __close(self):
    self.__session.close()
    self.__connection.close()


  def open_connection(self):
    self.__open()

  def close_connection(self):
    self.__close()


  def load_config(self, server):
    import ConfigParser
    config = ConfigParser.ConfigParser()
    config.readfp(open('config.cfg'))
    self.__host     = config.get(server,'hostname')
    self.__user     = config.get(server,'username')
    self.__password = config.get(server,'password')
    self.__database = config.get(server,'database')
    if config.has_option(server,'socket'):
      self.__socket   = config.get(server,'socket')


  def insert(self, table, data):
    values = None
    query = "INSERT INTO %s " % table
    if data:
      keys = data.keys()
      values = tuple(data.values())
      query += "(" + ",".join(["`%s`"] * len(keys)) %  tuple (keys) + ") VALUES (" + ",".join(["%s"]*len(values)) + ")"

#     self.__open()
    self.__session.execute(query, values)
    self.__connection.commit()
#     self.__close()
    return self.__session.lastrowid


  def select(self, table, where=None, *args):
    result = None
    query = 'SELECT '
    if args:
      keys = args
      l = len(keys) - 1
  
      for i, key in enumerate(keys):
        query += "`"+key+"`"
        if i < l:
          query += ","
    else:
      query += '*'

    query += ' FROM %s' % table

    if where:
      query += " WHERE %s" % where

#     self.__open()
    self.__session.execute(query)
    result = [item for item in self.__session.fetchall()]
#     self.__close()

    return result


  def update(self, table, index, data):
    query  = "UPDATE %s SET " % table
    keys   = data.keys()
    values = data.values()
    l = len(keys) - 1
    for i, key in enumerate(keys):
      query += "`"+key+"` = %s"
      if i < l:
        query += ","
    query += " WHERE id=%d" % index

#     self.__open()
    self.__session.execute(query, values)
    self.__connection.commit()
    # Obtain rows affected
    update_rows = self.__session.rowcount
#     self.__close()

    return update_rows


  def update_where(self, table, where=None, *args, **kwargs):
    query  = "UPDATE %s SET " % table
    keys   = kwargs.keys()
    values = tuple(kwargs.values()) + tuple(args)
    l = len(keys) - 1
    for i, key in enumerate(keys):
      query += "`"+key+"` = %s"
      if i < l:
        query += ","
    query += " WHERE %s" % where

#     self.__open()
    self.__session.execute(query, values)
    self.__connection.commit()
    # Obtain rows affected
    update_rows = self.__session.rowcount
#     self.__close()

    return update_rows


  def delete(self, table, index):
    query = "DELETE FROM %s WHERE id=%d" % (table,index)

#     self.__open()
    self.__session.execute(query)
    self.__connection.commit()

    # Obtain rows affected
    delete_rows = self.__session.rowcount
#     self.__close()

    return delete_rows


  def truncate_table(self, table):
    #query = "DELETE FROM %s WHERE 1" % (table)
    query = "TRUNCATE TABLE %s" % (table)

#     self.__open()
    self.__session.execute(query)
    self.__connection.commit()

    # Obtain rows affected
    delete_rows = self.__session.rowcount
#     self.__close()

    return delete_rows


  def sqlquery(self, query):
    self.__session.execute(query)
    self.__connection.commit()
#     rows = self.__connection.rowcount
    return self.__session

