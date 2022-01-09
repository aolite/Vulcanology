import unittest
from SPARQLWrapper import SPARQLWrapper, JSON

class OntologyTest(unittest.TestCase):
    def test_get_involved_vulcano(self):
        sparql = SPARQLWrapper(
            "https://api.triplydb.com/datasets/aitorcorchero/Vulcanology/services/Vulcanology/sparql")
        sparql.setQuery("""
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            PREFIX saref:<https://saref.etsi.org/core/>
            SELECT ?feature WHERE {
                ?feature a saref:FeatureOfInterest .
            } LIMIT 10
            """)
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()
        for result in results["results"]["bindings"]:
            print(result["feature"]["value"])

        self.assertEqual(result["feature"]["value"], 'https://www.w3id.org/aservo#VolcanLaPalma')

    def test_get_involved_variables_in_vulcano(self):
        sparql = SPARQLWrapper(
            "https://api.triplydb.com/datasets/aitorcorchero/Vulcanology/services/Vulcanology/sparql")
        sparql.setQuery("""
                   PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
                   PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
                   PREFIX saref:<https://saref.etsi.org/core/>
                   SELECT ?property WHERE {
                     ?feature a saref:FeatureOfInterest .
                     ?feature saref:hasProperty ?property .
                   } LIMIT 10
                   """)
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()
        array = []
        for result in results["results"]["bindings"]:
            print(result["property"]["value"])
            array.append(result["property"]["value"])
        self.assertEqual(array, ['https://www.w3id.org/aservo#NO2',
                                 'https://www.w3id.org/aservo#Humidity',
                                 'https://www.w3id.org/aservo#Illuminance',
                                 'https://www.w3id.org/aservo#O3',
                                 'https://www.w3id.org/aservo#SO2'])  # add assertion here

    def test_get_custom_measurements_in_date(self):
        sparql = SPARQLWrapper(
            "https://api.triplydb.com/datasets/aitorcorchero/Vulcanology/services/Vulcanology/sparql")
        sparql.setQuery("""
                          PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
                          PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
                          PREFIX saref:<https://saref.etsi.org/core/>
                          SELECT ?time ?value ?unit WHERE {
                            ?feature a saref:FeatureOfInterest .
                            ?feature saref:hasMeasurement ?measurement .
                            ?measurement saref:relatesToProperty <https://www.w3id.org/aservo#NO2> .
                            ?measurement saref:hasTimestamp ?time .
                            ?measurement saref:hasValue ?value .
                            ?measumrement saref:isMeasuredIn ?unit .
                          }
                          """)
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()
        counter = 0
        for result in results["results"]["bindings"]:
            print(f'{result["time"]["value"]}, {result["value"]["value"]},{result["unit"]["value"]}')
            counter = counter + 1
        self.assertEqual(counter, 10000)

if __name__ == '__main__':
    unittest.main()
