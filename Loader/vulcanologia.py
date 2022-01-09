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
        point_volcan = IRIS["http://www.w3.org/2003/01/geo/wgs84_pos#Point"]()
        point_volcan.lat = 28.612778
        point_volcan.long = -17.866111
        volcan.location = point_volcan
        volcan.hasVolcanicExplosivityIndex = 3

        airqualityDevice= IRIS["https://saref.etsi.org/core/Device"]('AirQuailitySensorPalma', namespace=self.onto)
        airqualityDevice.location = point_volcan
        volcan.hasDevice.append(airqualityDevice)

        point_sismic_device = IRIS["http://www.w3.org/2003/01/geo/wgs84_pos#Point"]()
        point_sismic_device.lat = 28.5116
        point_sismic_device.long = -17.8759
        sismicDevice = IRIS["https://saref.etsi.org/core/Device"]('SismicSensorPalma', namespace=self.onto)
        sismicDevice.location = point_sismic_device
        volcan.hasDevice.append(sismicDevice)

        affectionRisk = IRIS["https://www.w3id.org/aservo#PopulationRisks"]('LaPalmaRisk', namespace=self.onto)
        affectionRisk.is_a.append(IRIS["https://saref.etsi.org/core/Device"])
        affectionRisk.location = point_sismic_device
        volcan.hasDevice.append(affectionRisk)

    def airQualityLoader (self, csvName):
        airQualityCSV = pd.read_csv(csvName)
        airQualityCSV.fillna({'Time': '', 'SO2': -1}, inplace=True)

        self.onto.AirQuailitySensorPalma.hasProperty.append(self.onto.NO2Level('NO2', namespace= self.onto))
        self.onto.AirQuailitySensorPalma.hasProperty.append(self.onto.O3Level('O3', namespace=self.onto))
        self.onto.AirQuailitySensorPalma.hasProperty.append(self.onto.SO2Level('SO2', namespace=self.onto))
        self.onto.AirQuailitySensorPalma.hasProperty.append(self.onto.HumidityLevel('Humidity', namespace=self.onto))
        self.onto.AirQuailitySensorPalma.hasProperty.append(self.onto.IlluminanceLevel('Illuminance', namespace=self.onto))

        for i, row in enumerate(airQualityCSV.itertuples()):
            print (f' Loading the row number {i}/{len(airQualityCSV)}')
            unamed_measurement = IRIS["https://saref.etsi.org/core/Measurement"]()
            unamed_measurement.hasValue = row.O3
            unamed_measurement.hasTimestamp = row.time
            unamed_measurement.isMeasuredIn = IRIS["https://saref.etsi.org/core/UnitOfMeasure"]('ug/m3', namespace=self.onto)
            unamed_measurement.relatesToProperty = self.onto.O3

            self.onto.AirQuailitySensorPalma.makesMeasurement.append(unamed_measurement)


    def SismicMovements (self, csvName):
        seismicMovements = pd.read_csv(csvName)

        self.onto.SismicSensorPalma.hasProperty.append(self.onto.SeismicActivity('Magnitude', namespace= self.onto))
        self.onto.SismicSensorPalma.hasProperty.append(self.onto.SeismicActivity('IntensMax', namespace=self.onto))

        for i, row in enumerate(seismicMovements.itertuples()):
            unamed_measurement = IRIS["https://saref.etsi.org/core/Measurement"]()
            unamed_measurement.hasValue = row.Magnitud
            unamed_measurement.hasTimestamp = row.DateTime_
            unamed_measurement.isMeasuredIn = IRIS["https://saref.etsi.org/core/UnitOfMeasure"]('MbLg',
                                                                                                namespace=self.onto)

            unamed_measurement_2 = IRIS["https://saref.etsi.org/core/Measurement"]()
            unamed_measurement_2.hasValue = row.IntensMax
            unamed_measurement_2.hasTimestamp = row.DateTime_
            unamed_measurement_2.isMeasuredIn = self.onto.MbLg

            self.onto.SismicSensorPalma.makesMeasurement.append(unamed_measurement)
            self.onto.SismicSensorPalma.makesMeasurement.append(unamed_measurement_2)


    def SO2Level (self, csvName):
        airQualityCSV = pd.read_csv(csvName, sep=';')

        self.onto.AirQuailitySensorPalma.hasProperty.append(self.onto.SO2Level('SO2', namespace=self.onto))

        for i, row in enumerate(airQualityCSV.itertuples()):
            print (f' Loading the row number {i}/{len(airQualityCSV)}')
            unamed_measurement = IRIS["https://saref.etsi.org/core/Measurement"]()
            unamed_measurement.hasValue = row.SO2
            unamed_measurement.hasTimestamp = row.Time
            unamed_measurement.isMeasuredIn = IRIS["https://saref.etsi.org/core/UnitOfMeasure"]('ug/m3', namespace=self.onto)
            unamed_measurement.relatesToProperty = self.onto.SO2

            self.onto.AirQuailitySensorPalma.makesMeasurement.append(unamed_measurement)


    def O3Level (self, csvName):
        airQualityCSV = pd.read_csv(csvName, sep=';')

        self.onto.AirQuailitySensorPalma.hasProperty.append(self.onto.SO2Level('O3', namespace=self.onto))

        for i, row in enumerate(airQualityCSV.itertuples()):
            print(f' Loading the row number {i}/{len(airQualityCSV)}')
            unamed_measurement = IRIS["https://saref.etsi.org/core/Measurement"]()
            unamed_measurement.hasValue = row.O3
            unamed_measurement.hasTimestamp = row.Time
            unamed_measurement.isMeasuredIn = IRIS["https://saref.etsi.org/core/UnitOfMeasure"]('ug/m3',
                                                                                                namespace=self.onto)
            unamed_measurement.relatesToProperty = self.onto.SO2

            self.onto.AirQuailitySensorPalma.makesMeasurement.append(unamed_measurement)


    def Affections (self, csvName):
        affectionsCSV = pd.read_csv(csvName)

        self.onto.LaPalmaRisk.hasProperty.append(self.onto.PhysicalProperty('Residential', namespace=self.onto))
        self.onto.LaPalmaRisk.hasProperty.append(self.onto.PhysicalProperty('Industrial', namespace=self.onto))
        self.onto.LaPalmaRisk.hasProperty.append(self.onto.PhysicalProperty('Agro', namespace=self.onto))
        self.onto.LaPalmaRisk.hasProperty.append(self.onto.PhysicalProperty('Leisure', namespace=self.onto))
        self.onto.LaPalmaRisk.hasProperty.append(self.onto.PhysicalProperty('Other', namespace=self.onto))

        for i, row in enumerate(affectionsCSV.itertuples()):
            print(f' Loading the row number {i}/{len(affectionsCSV)}')
            unamed_measurement_1 = IRIS["https://saref.etsi.org/core/Measurement"]()
            unamed_measurement_1.hasValue = row.Residencial
            unamed_measurement_1.hasTimestamp = row.Fecha
            unamed_measurement_1.isMeasuredIn = IRIS["https://saref.etsi.org/core/UnitOfMeasure"]('unit',
                                                                                                namespace=self.onto)

            unamed_measurement_2 = IRIS["https://saref.etsi.org/core/Measurement"]()
            unamed_measurement_2.hasValue = row.Industrial
            unamed_measurement_2.hasTimestamp = row.Fecha
            unamed_measurement_2.isMeasuredIn = IRIS["https://saref.etsi.org/core/UnitOfMeasure"]('unit',
                                                                                                  namespace=self.onto)

            unamed_measurement_3 = IRIS["https://saref.etsi.org/core/Measurement"]()
            unamed_measurement_3.hasValue = row.Agrario
            unamed_measurement_3.hasTimestamp = row.Fecha
            unamed_measurement_3.isMeasuredIn = IRIS["https://saref.etsi.org/core/UnitOfMeasure"]('unit',
                                                                                                  namespace=self.onto)

            unamed_measurement_4 = IRIS["https://saref.etsi.org/core/Measurement"]()
            unamed_measurement_4.hasValue = row.Ocio
            unamed_measurement_4.hasTimestamp = row.Fecha
            unamed_measurement_4.isMeasuredIn = IRIS["https://saref.etsi.org/core/UnitOfMeasure"]('unit',
                                                                                                  namespace=self.onto)

            unamed_measurement_5 = IRIS["https://saref.etsi.org/core/Measurement"]()
            unamed_measurement_5.hasValue = row.Otros
            unamed_measurement_5.hasTimestamp = row.Fecha
            unamed_measurement_5.isMeasuredIn = IRIS["https://saref.etsi.org/core/UnitOfMeasure"]('unit',
                                                                                                  namespace=self.onto)

            unamed_measurement_1.relatesToProperty = self.onto.Residential
            unamed_measurement_2.relatesToProperty = self.onto.Industrial
            unamed_measurement_3.relatesToProperty = self.onto.Agro
            unamed_measurement_4.relatesToProperty = self.onto.Leisure
            unamed_measurement_5.relatesToProperty = self.onto.Other

            self.onto.LaPalmaRisk.makesMeasurement.append(unamed_measurement_1)
            self.onto.LaPalmaRisk.makesMeasurement.append(unamed_measurement_2)
            self.onto.LaPalmaRisk.makesMeasurement.append(unamed_measurement_3)
            self.onto.LaPalmaRisk.makesMeasurement.append(unamed_measurement_4)
            self.onto.LaPalmaRisk.makesMeasurement.append(unamed_measurement_5)



