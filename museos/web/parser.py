#!/usr/bin/python3

import xml.etree.ElementTree as ET

def parseXML(file):

    tree = ET.parse(file)
    contenidos = tree.getroot()
    museos = {}
    for contenido in contenidos:
        if contenido.tag == 'contenido':
            for atributos in contenido:
                if atributos.tag == 'atributos':
                    # Nuevo museo
                    museo = {}
                    for atributo in atributos:
                        if len(atributo) >= 1:
                            for subatributo in atributo:
                                if '\n' in subatributo.text:
                                    # Porque se ha detectado un fallo en el XML
                                    museo[subatributo.attrib['nombre']] = subatributo.text.split('\n')[0]
                                else:
                                    museo[subatributo.attrib['nombre']] = subatributo.text
                        else:
                            museo[atributo.attrib['nombre']] = atributo.text
                    museos[museo['ID-ENTIDAD']] = museo;
    return museos
