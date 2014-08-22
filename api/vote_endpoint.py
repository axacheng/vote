#!/usr/bin/python

import endpoints
import logging
import webapp2


from model import vote
from protorpc import messages
from protorpc import message_types
from protorpc import remote


class BarcodeMessageRequest(messages.Message):
  name = messages.StringField(1, required=True)
  secret = messages.StringField(2)
  q1 = messages.StringField(3)
  q2 = messages.StringField(4)
  q3 = messages.StringField(5)


class BarcodeMessageResponse(messages.Message):
  errmesg = messages.StringField(1)
  name = messages.StringField(2)
  owner = messages.StringField(3)
  status = messages.StringField(4)
  used = messages.BooleanField(5)


class InitBarcodeMessageRequest(messages.Message):
  pass

  
class InitBarcodeMessageResponse(messages.Message):
  errmesg = messages.StringField(1)
  status = messages.StringField(2)


@endpoints.api(name='vote', version='v1', description='Endpoints API for vote system')
class voteApi(remote.Service):
  @endpoints.method(InitBarcodeMessageRequest,
                    InitBarcodeMessageResponse,
                    name='initialize barcodes',
                    path='init',
                    http_method='GET')
  def InitBarcode(self, request):
    vote.Barcode.InitBarcode()
    return InitBarcodeMessageResponse(status='ok', errmesg='')


  @endpoints.method(BarcodeMessageRequest,
                    BarcodeMessageResponse,
                    name='Update barcodes according to survey answer',
                    path='/u',
                    http_method='POST')
  def UpdateBarcode(self, request):
    populate_data = {}
    populate_data['name'] = request.name
    populate_data['q1'] = request.q1
    populate_data['q2'] = request.q2
    populate_data['q3'] = request.q3
    barcode_entity_result = vote.Barcode.UpdateBarcode(populate_data)
    logging.info(barcode_entity_result)

    if barcode_entity_result == 'used':
      return BarcodeMessageResponse(status='used', errmesg='used')

    elif barcode_entity_result is False:
      return BarcodeMessageResponse(status='failed', errmesg='No such barcode')
    
    elif barcode_entity_result == 'ok':
      return BarcodeMessageResponse(status='ok', errmesg='Voted, all good')



  @endpoints.method(BarcodeMessageRequest,
                    BarcodeMessageResponse,
                    name='Query barcodes owner by name',
                    path='/qo',
                    http_method='POST')
  def QueryBarcodeOwner(self, request):
    if request.secret == 'axa':
      populate_data = {}
      populate_data['name'] = request.name
      barcode_owner = vote.Barcode.QueryBarcodeOwnerByName(populate_data)

      if barcode_owner:
        return BarcodeMessageResponse(owner=barcode_owner[0].owner,
                                      status='ok',
                                      errmesg='')
      else:
        return BarcodeMessageResponse(status='failed', errmesg='Can not found owner...')

  #   populate_data['rpi_id'] = request.rpi_id

  # @endpoints.method(TemperatureMessageRequest, TemperatureMessageResponse,
  #   name='query temperature',
  #   path='queryTemperature',
  #   http_method='GET')
  # def QueryTemperature(self, request):
  #   populate_data = {}
  #   populate_data['rpi_id'] = request.rpi_id
  #   entities = temperature.Temperature.QueryCurrentTemperature(populate_data)
    
  #   if entities:
  #     def message_result():
  #       for entity in entities:
  #         yield TemperatureMessageRequest(ctime=entity.ctime,
  #                                         current_temperature=entity.current_temperature,
  #                                         rpi_id=entity.rpi_id)

  #     return TemperatureMessageResponse(items=list(message_result()),
  #                                       status='ok', ='')
  #   else:
  #     return TemperatureMessageResponse(status='ok', ='Can not find current temperature...')  



app = endpoints.api_server([voteApi])
