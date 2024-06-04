"""
 snowy_hill.py
 Generacion de una cartera (en mainnet y testnet).

 Autor: Grillo
 Fecha de creación: antes de 2020
"""

########################################################################################
#semilla
#mnemonico
#seed
#xpriv (m)
#xpub (M)
#P2PK
#P2PKH
#P2SH
#BENCH
### CONSTANTES # Comentadas porque no las utilizo  finalmente.
#BIP141= "m/0/0"
#BIP84 = "m/84'/0'/0'/0/0"
#BIP49 = "m/49'/0'/0'/0/0"
#BIP44 = "m/44'/0'/0'/0/0"
#BIP44T = "m/44'/1'/0'/0/0"
#BIP32 = "m/0/0"
# Ejemplos manual:
#   Derivacion de publicas
# xpv=tprv8fPDJN9UQqg6pFsQsrVxTwHZmXLvHpfGGcsCA9rtnatUgVtBKxhtFeqiyaYKSWydunKpjhvgJf6PwTwgirwuCbFq8YKgpQiaVJf3JCrNmkR; bx hd-to-public --version 70617039 $xpv| bx hd-public -c test.cfg |bx hd-public -i 1 -c test.cfg           | bx hd-to-ec -c test.cfg|bx ec-to-address -v 111
#   Derivacion general
# E=00000000000000000000000000000000; bx mnemonic-new $E| bx mnemonic-to-seed| bx hd-new --version 70615956| bx hd-private -i 44 -d|\
#      bx hd-private -i 1 -d|bx hd-private -i 0 -d| bx hd-private -i 0 | bx hd-private -i 0|\
#      bx hd-to-ec --config test.cfg| bx ec-to-wif --version 239|bx wif-to-public -c test.cfg |bx ec-to-address --version 111
#    = mkpZhYtJu2r87Js3pDiWJDmPte2NRZ8bJV
# E=00000000000000000000000000000000; bx mnemonic-new $E| bx mnemonic-to-seed| bx hd-new --version 70615956| bx hd-private -i 44 -d|\
#      bx hd-private -i 1 -d|bx hd-private -i 0 -d| bx hd-private -i 0 | bx hd-private -i 0|\
#      bx hd-to-ec --config test.cfg|bx ec-to-public -c test.cfg
########################################################################################

# Importaciones estandar
import os  # para poder ejecutar comandos de shell
import argparse  # Manejo de argumentos en linea de comandos
import sys
from subprocess import Popen, PIPE
# Importaciones de terceros
# Importaciones locales
from src.cartera import cartera
from src.pago import all

VERBOSE=False
DEPURA=False
FICHERO_CONFIGURACION_TESTNET="test.cfg"
FICHERO_CONFIGURACION_MAINNET="bx.cfg"
TESTNET=False
MAINNET=True # es redundante, lo hago para mejor lectura. 


def main():
    """
    Funcion principal
    Tratamiento de la entrada de parametros de ejecución y ejecución secuencial.
    :param argumento1: No hay argumentos
    :type argumento1: NONE
    :return: No devuelve nada
    :rtype: NONE
    """
    global VERBOSE
    # Comprobar que existe el programa bx
    try:
        Popen('bx', stdout=PIPE, stderr=PIPE)
    except OSError:
        msg = "No puedo ejecutar bx, necesario para la derivación.\nLocalizable en https://github.com/libbitcoin/libbitcoin-explorer\n"
        sys.exit(msg)

    parser = argparse.ArgumentParser()
    parser = argparse.ArgumentParser(description='%(prog)s : Derivar arbol de claves BTC según el BIP32. El parámetro ENTROPIA puede representar en realidad varias cosas: 1.- Múltiplo de 32 bits llamado ENTROPY en el BIP39, del que derivar la frase mnemonica, en este caso debe aparecer el parámetro "-d" 2.- La frase mnemónica, entre parentesis y separada por espacios. OJO: no se verifica que la frase cumpla BIP39. 3.- La Seed fuente de la generación de billeteras deterministas jerárquicas descrita en BIP32')
    parser.add_argument("-v", "--verbose", help="Mostrar información de depuración", action="store_true")
    parser.add_argument("-f", "--file", help="Nombre de archivo a procesar. SIN IMPLEMENTAR AUN")
    parser.add_argument("-t", "--testnet", help="Realizar la derivacion en TESTNET", action="store_true")
    parser.add_argument("-d", "--derivarmnemonico", help="El valor de entropia deriva el mnemonico", action="store_true")
    parser.add_argument("-e", "--esquema", help="Esquema de derivación. eje: m/44'/0'/0'/0/0 (Se utiliza m/44'/0'/0'/0/x,y para generar direcciones de pago desde x hasta y)")
    parser.add_argument("-s", "--secreto", help="Contraseña para añadir al mnemonico")
    parser.add_argument("-j", "--ejemplo", help="La cadena <entropia> se expandira (x32) y se utilizara esquema BIP44.", action="store_true")
    parser.add_argument("-p", "--payfile", help="Nombre del archivo en el que guardar las direcciones de pago.")
    parser.add_argument("-o", "--old", help="Ejecutar la version antigua.", action="store_true")
    parser.add_argument("-c", "--corto", help="Mostrar salida corta.", action="store_true")
    parser.add_argument("-cc", "--mascorto", help="Mostrar salida mas corta.", action="store_true")
    parser.add_argument("entropia", help="Origen de la derivación (Entropia, Mnemonico, Seed, xpriv...)")
    args = parser.parse_args()

    # Almacenar el valor <entropia> en variable para separar lo del esquema de argumentos.
    semilla=args.entropia
    entropiaAmnemonico=args.derivarmnemonico

    # Aquí procesamos lo que se tiene que hacer con cada argumento

    if args.ejemplo: # Defino unos valores para usarlos como ejemplo y estudio.
        semilla=semilla*32 # cadena multiplo de 32.
        entropiaAmnemonico=True # El ejemplo debe derivar desde entropia a mnemonico

    if args.secreto:
        secreto=args.secreto
    else:
        secreto=""

    TESTNET=args.testnet
    MAINNET=not args.testnet
    if (TESTNET):  #comprobar que existe fichero de configuracion para testnet.
        if os.path.exists(FICHERO_CONFIGURACION_TESTNET):
            BIP44 = "m/44'/1'/0'/0/0"
        else:
            print ("Error: no existe el fichero de configuracion para testnet.")
            exit(1)
    else:
        if os.path.exists(FICHERO_CONFIGURACION_MAINNET):
            BIP44 = "m/44'/0'/0'/0/0"
        else:
            print ("Error: no existe el fichero de configuracion para mainnet.")
            exit(1)

    if args.esquema:
        # se permite "BIP44.n-m"
        if "." in args.esquema:
            [args.esquema,rangoPagos]=args.esquema.split(".")
            BIP44 = BIP44[:-1] + rangoPagos
        if args.esquema=="BIP44":
            esquema=BIP44
        else:
            print ("Cuidado: introducir un esquema manualmente o distinto a BIP44 puede dar un resultado erroneo")
            esquema = args.esquema
    else: 
        esquema=BIP44

    if args.verbose:
        VERBOSE = True
        print("Semilla: "+semilla)
        print("Esquema: "+esquema)
        print("Secreto: "+secreto)
        print("A mnemonico: "+str(entropiaAmnemonico))

    if args.old:
        arbol=dict()
        arbol={'E':"",'mnemonico':"",'contrasena':"",'seed':"",'esquema':"",'m':'', 'M':'','xpriv':[], 'xpub':[], 'pagos':[]}
        direccion = dict() # Definir variable tipo diccionario
        direccion={'xprv':"", 'xpub':"", 'ec':"", 'wif':"", 'ec_pub':"", 'address_p2pkh':""}
        derivacion(semilla, esquema, secreto, entropiaAmnemonico)
    else:
        print("#=====================================")
        mycartera=cartera(semilla, esquema, secreto, entropiaAmnemonico, TESTNET)
        if args.mascorto:
            mycartera.print_massencilla()
        elif args.corto:
            mycartera.print_sencilla(verbose=VERBOSE)
        else:
	        mycartera.print_consola(verbose=VERBOSE)
        print("#=====================================")
        # Volcado de pagos a fichero
        if args.payfile:
            ficheropagos = args.payfile
            try:
                with open(ficheropagos, 'a') as f:
                    f.write("# %s\n%s" %(mycartera.esquema, mycartera.cadena_pagos()))
            except:
                print("Error al tratar de escribir en fichero (%s)" %(ficheropagos))



def DesdeWif(wif):
    """
    Para estudiar la derivacion que realiza el cliente Bitcoin Colore
    tratando de encontrar un punto de union con otro software de billetera.
    """
    if(len(wif)<1):
        return 0
    direccion = dict()
    direccion["wif"]=wif
    direccion["ec"]=(os.popen("bx wif-to-ec "+ wif).read()).rstrip("\n")
    direccion["ec_pub"]=(os.popen("bx wif-to-public " + direccion["wif"]).read()).rstrip("\n")
    direccion["address_p2pkh"]=(os.popen("bx"+ ec_to_address + direccion["ec_pub"]).read()).rstrip("\n")
    return direccion
    privada_wif  = wif.rstrip("\n")
    publica_ec = (os.popen("bx wif-to-public " + privada_wif).read()).rstrip("\n")
    address_p2pkh = (os.popen("bx"+ ec_to_address + publica_ec).read()).rstrip("\n")
    priv_ec = (os.popen("bx wif-to-ec " + privada_wif).read()).rstrip("\n")
    xpriv_de_wif = (os.popen("bx" + hd_new +  priv_ec).read()).rstrip("\n")


def _Depurame_(ref, datos, finalizar=False):
    """
    Uso:
         #_Depurame_(numero,[dato1, dato2,...])
    """
    cadena = "][".join([str(elemento) for elemento in datos])
    print("* Depuracion ref-%d: [%s]" %(ref, cadena))
    if finalizar:
        print ("=== Fin del programa. Se ha llamado a depuracion con orden de finalizar ===")
        exit(1)

### Llamar a funcion principal.###
if __name__ == "__main__":
    main()
