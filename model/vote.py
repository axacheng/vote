# -*- coding: utf-8 -*-
import collections
import hashlib
import logging

from google.appengine.ext import ndb

BUILDING=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18]
FLOOR=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
POSITION=[0, 1, 2, 3]
SALT='Q@2kC}4q53q'


class Barcode(ndb.Model):
  building = ndb.StringProperty()
  mtime = ndb.DateTimeProperty(auto_now=True)
  name = ndb.StringProperty()
  status = ndb.StringProperty(default='ok')
  used = ndb.BooleanProperty(default=False)
  owner = ndb.StringProperty()
  q1 = ndb.StringProperty(default='0')
  q2 = ndb.StringProperty(default='0')
  q3 = ndb.StringProperty(default='0')
  q4 = ndb.StringProperty(default='0')
  q5 = ndb.StringProperty(default='0')


  @classmethod
  def InitBarcode(cls):
    if len(cls.query().fetch()) < 1:
      def populate_barcode():
        for i in BUILDING:
          for j in FLOOR:
            for k in POSITION:
              addr = "%s-%s-%s" % (i, j, k)
              name = hashlib.sha1(addr + SALT).hexdigest()
              yield cls(building=str(i), name=name, owner=addr, 
                        parent=ndb.Key(cls, name))

      future = ndb.put_multi_async(list(populate_barcode()))

      # Doing real ndb write for calling future object.
      if future:
        return future[0].get_result()

  @classmethod
  def QueryBarcodeStatus(cls, populate_data):
    name = populate_data.get('name')
    parent = ndb.Key(cls, name)
    return cls.query(ancestor=parent).fetch()


  @classmethod
  def QueryBarcodeOwnerByName(cls, populate_data):
    name = populate_data.get('name')
    parent = ndb.Key(cls, name)
    return cls.query(ancestor=parent).fetch(projection=[cls.owner])


  @classmethod
  def QueryBarcodeAnswerByBuilding(cls, populate_data):
    _building = populate_data.get('building')
    return cls.query(cls.building == _building,
                     cls.used == True).fetch()


  @classmethod
  def QueryChart(cls):
    d = collections.defaultdict(list)
    question_1 = collections.Counter()
    question_2 = collections.Counter()
    question_3 = collections.Counter()

    def fix_result(x):
      logging.info('xxxxxxxxxxxxxxx:%s', x)
      d['q1'].append(x.q1)
      d['q2'].append(x.q2)
      d['q3'].append(x.q3)

    cls.query(cls.used == True).map(fix_result)

    for question, answer in d.items():
      if question == 'q1':
        for ans in answer:
          question_1[ans] += 1

      elif question == 'q2':
        for ans in answer:
          question_2[ans] += 1

      elif question == 'q3':
        for ans in answer:
          question_3[ans] += 1

    return question_1, question_2, question_3


  @classmethod
  def UpdateBarcode(cls, populate_data):
    name = populate_data.get('name')
    status = populate_data.get('status')
    q1 = populate_data.get('q1')
    q2 = populate_data.get('q2')
    q3 = populate_data.get('q3')

    parent = ndb.Key(cls, name)
    barcode_entity = cls.query(ancestor=parent).fetch()

    if barcode_entity and barcode_entity[0].used is True:
      return 'used'

    elif barcode_entity and barcode_entity[0].used is False:
      barcode_entity[0].used = True
      barcode_entity[0].q1 = q1
      barcode_entity[0].q2 = q2
      barcode_entity[0].q3 = q3
      barcode_entity[0].put()
      return 'ok'
    
    else:
      return False
