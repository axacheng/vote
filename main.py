import gviz_api
import jinja2
import json
import logging
import os
import webapp2

from model import vote


jinja_environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))


class DrewChart(webapp2.RequestHandler):
  def get(self, chart_type):
    tqx = self.request.get('tqx')
    if tqx:
      params = {}
      params[tqx.split(':')[0]] = tqx.split(':')[1]
    else:
      params = {'reqId':''}
    req_id = params['reqId']

    ###
    q1_result, q2_result, q3_result = vote.Barcode.QueryChart()

    logging.info('Q1:%s', q1_result)  #{u'1': 2, u'2': 2}
    logging.info('Q2:%s', q2_result)
    logging.info('Q3:%s', q3_result)

    ###
    if chart_type == 'q1':
      chart_schema = {'choice_item':('string', u'item'),
                      'choice_count':('number', u'Count')}
      
      chart_data_template = []
      for choice_item, choice_count in q1_result.items():
        chart_data = {}
        chart_data['choice_item'] = choice_item
        chart_data['choice_count'] = choice_count
        chart_data_template.append(chart_data)

      data_table = gviz_api.DataTable(chart_schema)
      data_table.LoadData(chart_data_template)
      chart_response = data_table.ToJSonResponse(columns_order=('choice_item', 'choice_count'),
                                                 order_by='choice_count', req_id=req_id)
      self.response.headers['Content-Type'] = 'text/json'
      self.response.out.write(chart_response)


    elif chart_type == 'q2':
      chart_schema = {'choice_item':('string', u'item'),
                      'choice_count':('number', u'Count')}
      
      chart_data_template = []
      for choice_item, choice_count in q2_result.items():
        chart_data = {}
        chart_data['choice_item'] = choice_item
        chart_data['choice_count'] = choice_count
        chart_data_template.append(chart_data)

      data_table = gviz_api.DataTable(chart_schema)
      data_table.LoadData(chart_data_template)
      chart_response = data_table.ToJSonResponse(columns_order=('choice_item', 'choice_count'),
                                                 order_by='choice_count', req_id=req_id)
      self.response.headers['Content-Type'] = 'text/json'
      self.response.out.write(chart_response)


    elif chart_type == 'q3':
      chart_schema = {'choice_item':('string', u'item'),
                      'choice_count':('number', u'Count')}
      
      chart_data_template = []
      for choice_item, choice_count in q3_result.items():
        chart_data = {}
        chart_data['choice_item'] = choice_item
        chart_data['choice_count'] = choice_count
        chart_data_template.append(chart_data)

      data_table = gviz_api.DataTable(chart_schema)
      data_table.LoadData(chart_data_template)
      chart_response = data_table.ToJSonResponse(columns_order=('choice_item', 'choice_count'),
                                                 order_by='choice_count', req_id=req_id)
      self.response.headers['Content-Type'] = 'text/json'
      self.response.out.write(chart_response)


class Failed(webapp2.RequestHandler):
  def get(self, name):
    template_dict={'name':name}
    template = jinja_environment.get_template('app/failed.html')
    self.response.out.write(template.render(template_dict))


class MainPage(webapp2.RequestHandler):
  def get(self):
    template_dict={}
    template = jinja_environment.get_template('app/index.html')
    self.response.out.write(template.render(template_dict))


class Ok(webapp2.RequestHandler):
  def get(self, name):
    template_dict={'name':name}

    barcode_entity = vote.Barcode.QueryBarcodeStatus(template_dict)

    if barcode_entity and barcode_entity[0].used is False:
      template = jinja_environment.get_template('app/ok.html')
      self.response.out.write(template.render(template_dict))
    
    else:
      template_dict['errmesg'] = '[403] DO NOT HACK US!'
      template = jinja_environment.get_template('app/failed.html')
      self.response.out.write(template.render(template_dict))    


class Report(webapp2.RequestHandler):
  def get(self):
    template_dict={}
    template = jinja_environment.get_template('app/report.html')
    self.response.out.write(template.render(template_dict))


class QueryBarcodeStatus(webapp2.RequestHandler):
  def get(self, name):
    populate_data = {}
    populate_data['name'] = name
    barcode_entity = vote.Barcode.QueryBarcodeStatus(populate_data)

    if barcode_entity and barcode_entity[0].used is False:
      self.redirect('/ok/' + name)

    elif barcode_entity and barcode_entity[0].used is True:
      self.redirect('/failed/' + name + '/used')

    else:
      self.redirect('/failed/' + name + '/failed')


app = webapp2.WSGIApplication([('/chart/(.*)', DrewChart),
                               ('/failed/(.*)', Failed),
                               ('/', MainPage),
                               ('/ok/(.*)', Ok),
                               ('/report', Report),
                               ('/q/(.*)', QueryBarcodeStatus),
                              ],
                              debug=True)
