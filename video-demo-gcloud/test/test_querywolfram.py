import querywolfram

query_url = 'http://api.wolframalpha.com/v2/query?' +\
    'input=what+is+the+melting+point+of+silver' +\
    '&appid=AH3JX3-L23R5H2793&includepodid=Result'
  
query_xml = '''<?xml version='1.0' encoding='UTF-8'?>
<queryresult success='true'
    error='false'
    xml:space='preserve'
    numpods='1'
    datatypes='Element'
    timedout=''
    timedoutpods=''
    timing='1.568'
    parsetiming='0.935'
    parsetimedout='false'
    recalculate=''
    id='MSP9671c9f562818b58igd000052b6eb4a576gcf55'
    host='https://www4b.wolframalpha.com'
    server='31'
    related='https://www4b.wolframalpha.com/api/v1/relatedQueries.jsp?id=MSPa9681c9f562818b58igd00005i87f2005i4a00983670053420704098597'
    version='2.6'
    inputstring='what is the melting point of silver'>
 <pod title='Result'
     scanner='Data'
     id='Result'
     position='100'
     error='false'
     numsubpods='1'
     primary='true'>
  <subpod title=''>
   <microsources>
    <microsource>ElementData</microsource>
   </microsources>
   <datasources>
    <datasource>WebElements</datasource>
   </datasources>
   <img src='https://www4b.wolframalpha.com/Calculate/MSP/MSP9691c9f562818b58igd000012d07a68723fiedd?MSPStoreType=image/gif&amp;s=31'
       alt='961.78 °C (degrees Celsius)'
       title='961.78 °C (degrees Celsius)'
       width='178'
       height='19'
       type='Default'
       themes='1,2,3,4,5,6,7,8,9,10,11,12'
       colorinvertable='true' />
   <plaintext>961.78 °C (degrees Celsius)</plaintext>
  </subpod>
  <expressiontypes count='1'>
   <expressiontype name='Default' />
  </expressiontypes>
 </pod>
 <sources count='1'>
  <source url='https://www4b.wolframalpha.com/sources/ElementDataSourceInformationNotes.html'
      text='Element data' />
 </sources>
</queryresult>
'''

def test_answer_query(requests_mock):
    # Following question and answer will work with Wolfram Alpha
    # tested 17th Aug 2021
    query_text = 'what is the melting point of silver'
    query_answer = '961.78 °C (degrees Celsius)'
    # As we do not wish to call the service when testing the response
    # is mocked.
    requests_mock.get(query_url, text=query_xml)
    response_text = querywolfram.answer_query(query_text)
    assert response_text == query_answer
