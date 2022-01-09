from owlready2 import *

from Loader.vulcanologia import VulcanologiaLoader


def load_ontology (file):
    return get_ontology(file).load()

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press ⌘F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    file = './Ontology/aservo.owl'


    print(f' Loading the ontology T-Box file named as: {file}')
    TBox = load_ontology(file)

    print (f'{list(TBox.classes())}')
    print(f'{IRIS["https://saref.etsi.org/core/Device"]}')

    loader = VulcanologiaLoader(TBox)
    loader.perimetroLoader()

    loader.airQualityLoader('./Data/Registros_de_calidad_aire.csv')

    TBox = loader.onto
    TBox.save(file='aservo_output_AirQuality.owl', format='rdfxml')




