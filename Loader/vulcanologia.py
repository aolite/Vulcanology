from owlready2 import *
import pandas as pd
import os

class VulcanologiaLoader:
    def __init__(self, ontology):
        self.onto = ontology


    def perimetroLoader(self, ):
        volcan = IRIS["https://saref.etsi.org/core/FeatureOfInterest"]('VolcanLaPalma', namespace=self.onto)
        print (f'{list(self.onto.classes())}')
        volcan.is_a.append(self.onto.VolcanicEruption)
        volcan.hasName = 'Volcan Cumbre Vieja'
        volcan.area = 11360258.6178296
        volcan.ha = 1136.02586178296
        volcan.perimeter = 55080.9270797893
        volcan.shape_area = 14796038.3266602
        volcan.length = 62828.82241109
        volcan.hasDurationInDays = 85
        volcan.lat = 28.612778
        volcan.lon = -17.866111
        volcan.hasVolcanicExplosivityIndex = 3

    def airQualityLoader (self, csvName):
        #dir_path = os.path.dirname(os.path.realpath(__file__))
        #dir_path = os.path.join(dir_path, "Data", csvName)
        airQualityCSV = pd.read_csv(csvName)
        airQualityCSV.fillna({'Time': '', 'SO2': -1}, inplace=True)

        self.onto.VolcanLaPalma.hasProperty.append(self.onto.NO2Level('NO2', namespace= self.onto))
        self.onto.VolcanLaPalma.hasProperty.append(self.onto.O3Level('O3', namespace=self.onto))
        self.onto.VolcanLaPalma.hasProperty.append(self.onto.SO2Level('SO2', namespace=self.onto))
        self.onto.VolcanLaPalma.hasProperty.append(self.onto.HumidityLevel('Humidity', namespace=self.onto))
        self.onto.VolcanLaPalma.hasProperty.append(self.onto.IlluminanceLevel('Illuminance', namespace=self.onto))

        for i, row in enumerate(airQualityCSV.itertuples()):
            print (f' Loading the row number {i}/{len(airQualityCSV)}')
            unamed_measurement = IRIS["https://saref.etsi.org/core/Measurement"]()
            unamed_measurement.hasValue = row.NO2
            unamed_measurement.hasTimestamp = row.time
            unamed_measurement.isMeasuredIn = IRIS["https://saref.etsi.org/core/UnitOfMeasure"]('ug/m3', namespace=self.onto)
            unamed_measurement.relatesToProperty = self.onto.NO2
            self.onto.VolcanLaPalma.hasMeasurement.append(unamed_measurement)

