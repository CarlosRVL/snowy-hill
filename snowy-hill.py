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

class direccion_pago(object):
    """
    Para la version Testnet, asumimos que existe el fichero test.cfg con la configuracion necesaria. 
    ATENCION: No realizo control de esistencia del fichero. 
    """
    indice=0 # Indice que ha generado la xprv. 
    xprv=""
    xpub=""
    ec=""
    wif=""
    ec_pub=""
    address_p2pkh=""
    testnet=""
    #hd_new="hd-new "
    hd_to_public="hd-to-public "
    hd_to_ec="hd-to-ec "
    ec_to_wif="ec-to-wif "
    ec_to_address="ec-to-address "
    #mas:
    wif_to_ec="wif-to-ec "

    def __init__(self, privada, indice, testnet=False):
        self.indice = indice
        self.xprv = privada
        self.testnet = testnet
        if (self.testnet):
            #self.hd_new       ="hd-new --version 70615956 "
            self.hd_to_public    ="hd-to-public --version 70617039 "
            self.hd_to_ec     ="hd-to-ec --config test.cfg "
            self.ec_to_wif    ="ec-to-wif --version 239 " # (-u)
            self.ec_to_address="ec-to-address --version 111 "
            wif_to_ec         = "wif-to-ec --config test.cfg "
        else:
            #self.hd_new       ="hd-new "
            self.hd_to_public    ="hd-to-public "
            self.hd_to_ec     ="hd-to-ec "
            self.ec_to_wif    ="ec-to-wif " # (-u)
            self.ec_to_address="ec-to-address "
            wif_to_ec         = "wif-to-ec "

        self.deriva(self.xprv, "xprv")

    def deriva(self, origen, tipo):
        """
        derivar las direcciones de pago finales a partir de una hd xprv.
            - Clave privada (XPrv) + Matematica de curva eliptica (EC) = Clave publica (XPub)
            - Clave publica + transformaciones = direccion bitcoin
        ec_privada, wif, ec_publica, address (P2PKH)....
        la ec_privada parece no ser demasiado interesante,
        suele ser mas utilizada en formato wif
        Secuencia:
            <xprv>   =  Valor de entrada   ;  <xpub>  =  bx hd-public <xprv>
            <ec>     =  bx hd-to-ec <xprv>
            <wif>    =  bx ec-to-wif <ec>
            <ec_pub> =  bx wif-to-public <wif>
            <address_p2pkh>  = bx ec-to-address <ec_pub>
        """
        secuencia={"xprv":0, "ec":2, "wif":3, "ec_pub":4}
        temp_camino=["", "", "", "", "", ""] # 6 campos: xprv - [xpub] - ec - wif - ec_pub - address_p2pkh

        if tipo == "wif" :
            tipo = "ec"
            origen = (os.popen("bx " + wif-to-ec + origen).read()).rstrip("\n")

        temp_camino[secuencia[tipo]]=origen
        #lde=[lambda :(os.popen("bx " + self.hd_public     + temp_camino[0]).read()).rstrip("\n")]
        #temp_temp = lde[0]()
        lderivacion=[lambda a: (os.popen("bx " + self.hd_to_public     + temp_camino[0]).read()).rstrip("\n"),\
                     lambda a: (os.popen("bx " + self.hd_to_ec      + temp_camino[0]).read()).rstrip("\n"),\
                     lambda a: (os.popen("bx " + self.ec_to_wif     + temp_camino[2]).read()).rstrip("\n"),\
                     lambda a: (os.popen("bx wif-to-public "        + temp_camino[3]).read()).rstrip("\n"),\
                     lambda a: (os.popen("bx " + self.ec_to_address + temp_camino[4]).read()).rstrip("\n"),\
                    ]
        for j in range(secuencia[tipo],len(lderivacion)):
            temp_camino[j+1] = (lderivacion[j])(0)
        self.xprv=temp_camino[0]
        self.xpub=temp_camino[1]
        self.ec=temp_camino[2]
        self.wif=temp_camino[3]
        self.ec_pub=temp_camino[4]
        self.address_p2pkh=temp_camino[5]

    def print_consola(self):
        print("\n-%5s: %s" %(self.indice, self.xprv))
        try:
            print("  xpub: " + self.xpub)
            print("prv_ec: " + self.ec)
            print("   wif: " + self.wif)
            print("pub_ec: " + self.ec_pub)
            print(" p2pkh: " + self.address_p2pkh)
        except:
            _Depurame_(376, ["Error en 'pago.print_consola'"])

    def print_p2pkh(self):
        try:
            print("%s:%s" %(self.indice, self.address_p2pkh))
        except:
            _Depurame_(376, ["Error en 'pago.print_p2pkh'"])

    def cadena_consola(self):
        cadena=("\n-%5s: %s" %(self.indice, self.xprv))
        try:
            cadena+=("\n  xpub: " + self.xpub)
            cadena+=("prv_ec: " + self.ec)
            cadena+=("   wif: " + self.wif)
            cadena+=("pub_ec: " + self.ec_pub)
            cadena+=(" p2pkh: " + self.address_p2pkh)
            return cadena
        except:
            _Depurame_(376, ["Error en 'pago.print_consola'"])

    def cadena_p2pkh(self):
        cadena=""
        try:
            cadena=("pag %3s:%s" %(self.indice, self.address_p2pkh))
            return cadena
        except:
            _Depurame_(376, ["Error en 'pago.cadena_p2pkh'"])

    def cadena_wif(self):
        cadena=""
        try:
            cadena=("wif %3s:%s" %(self.indice, self.wif))
            return cadena
        except:
            _Depurame_(378, ["Error en 'pago.cadena_wif'"])


def derivacion(entropia, esquema="m/44'/0'/0'/0/0", contrasena="", entropiaAmnemonico=False):
    """
    Desarrolla secuencia de derivación desde la <entropia> hasta la <direccion>
    Esta secuencia es:
    semilla, mnemonic, seed, hd, hd, hd, ... (ec, wif, public addres)
    <entropia>   =  "Obtenido desde alguna fuente aleatoria o usuario"
    <mnemonico>  =  bx mnemonic-new  <entropia>
    <seed>       =  bx mnemonic-to-seed <mnemonico> [-p <contrasena>]
    <xprv M>     =  bx hd-new <seed>
    <xprv intermedia> =  bx hd-private -i <N> [--hard] <xprv>  # <N> Numero que toca del esquema (.../0'/...)
    <xprv intermedia> =  <se repite el paso anterior hasta el penultimo elemento del esquema>
    ...
    <xprv fin>   =  bx hd-private -i <n> [--hard] <xprv>  #
    -- En este punto se llama a otra funcion encargada de las direcciones de pago. --
    <xpub>   =  bx hd-public <xprv_fin>
    <ec>     =  bx hd-to-ec <xprv>
    <wif>    =  bx ec-to-wif <ec>
    <ec_pub> =  bx wif-to-public <wif>
    <address_p2pkh>  = bx ec-to-address <ec_pub>
    (E): Valor utilizado como origen aleatorio. Normalizado en Base16, debe tener una logitud divisible entre 32
    frase: mnemonico (BIP39)
    seed: representacion numerica del mnemonico bip39
    Parametros
    ----------
    entropia: string
        puede ser un valor de entropia inicial (E), una frase, o un seed.
    esquema: string
        Esquema de derivacion de claves que se debe utilizar.
    contrasena: string
        Frase secreta que modifica la generacion del seed a partir del mnemonico.
        Al utilizarla incorpora un grado adicional de seguridad (y riesgo de perdida)
    entropiaAmnemonico: boolean
        True: parametro entropia se utiliza como generador del mnemonico.
            La secuencia comenzara con la obtencion de la frase mnemonica
        False: parametro entropia se utiliza como seed.
            la secuencia comenzara con la obtencion de la primera XPrv (m).
            En este el programa desconoce la frase mnemonica.
    Devuelve
    --------
    En principio no devuelve nada porque esta enfocada a mostrar datos en pantalla.
    En el futuro debe: estructura u objeto con la derivacion obtenida. 

    Ver tambien
    -----------
    Direcionesdepago(): derivacion de las claves publicas a partir de XPrv,
         hasta la direccion de cartera.
    """
    hd_new=" hd-new "
    hd_public=" hd-public "
    arbol={'E':"",'mnemonico':"",'contrasena':contrasena,'seed':"",'esquema':esquema,'m':'', 'M':'','xpriv':[], 'xpub':[], 'pagos':[]}
    frase = entropia.split() # puede ser una frase o una semilla, decision a continuacion
    # Casos: E, mnemonico, seed
    if(entropiaAmnemonico): # Si es true se debe generar una frase a partir de la entropia
        arbol["E"]=entropia
        arbol["mnemonico"]=(os.popen("bx mnemonic-new " + entropia).read()).rstrip("\n")
    elif(len(frase)>1): #Si contiene mas de una palabra es un mnemonico
        arbol["mnemonico"]=entropia
    if arbol["mnemonico"]:
        arbol["contrasena"] = contrasena
        contrasena = " -p \"%s\" " %(contrasena)
        arbol["seed"]=(os.popen("bx mnemonic-to-seed " + arbol["mnemonico"] + contrasena).read()).rstrip("\n")
    else:
        arbol["seed"] = entropia
    print("Entropia  : " + arbol["E"])
    print("mnemonico : " + arbol["mnemonico"])
    print("Seed      : " + arbol["seed"])
    print("Esquema   : " + arbol["esquema"])
    deriva = arbol["esquema"].split("/")
    temporal=arbol["seed"]
    for x in deriva[:-1]: #ultima especial
        x.strip() #Eliminar blancos
        # La claves pueden ser duras o ¿blandas?. Las duras (') no permiten deribar de la publica, 
        # las "blandas" permiten una deribar publicas de las publicas (tengo que estudiarlo mejor)
        if "'" in x:
            duro=" --hard "
        else:
            duro=""
	    # La clave identificada como m o M es especial. 
        if x == "m":
            arbol["m"]=(os.popen("bx"+ hd_new + arbol["seed"]).read()).rstrip("\n")
            temporal = arbol["m"]
            print ( " - %4s: %s" %(x,arbol["m"]))
        else:  # Las xpriv o pub de la derivacion que no sean m o M las anadirmos a la lista xpriv[]
            y = x.rstrip("'")  # quito la marca de dureza, ya se ha registrado en variable "duro". 
            # La derivacion itera sobre la xpriv previa, por lo que hay que guardar en temporal
            temporal=(os.popen("bx hd-private -i %s %s %s" %(y, duro, temporal)).read()).rstrip("\n")
            arbol["xpriv"].append(temporal)
            # Almaceno xpub para posterior estudio. No lo utilizo de momento. 
            arbol["xpub"].append((os.popen("bx hd-public -i %s %s %s" %(y, duro, temporal)).read()).rstrip("\n") + " Depura: con i y dureza")
            print ( " - %4s: %s" %(x,arbol["xpriv"][-1]))
    # Procesar ultima: deriva[-1]
    # La Ultima clave se trata aparte porque puedo generar mas de una dirección de pago y para ello utilizo una 
    # notacion diferente y un bucle.
    if "'" in deriva[-1]:
        duro=" --hard "
    else:
        duro=""
    # Si quiero generar varias direcciones de pago lo indico los valores inicial y final: i,j
    y = (deriva[-1].strip("'")).split(",")
    # Bucle para generar las direcciones de pago.
    for i in range(int(y[0]),int(y[-1])+1):  # y[-1] representa el ultimo elemento del array. Range no incluye el ultimo por eso +1
        xprv_fin=(os.popen("bx hd-private -i %d %s %s" %(i, duro, temporal)).read()).rstrip("\n")
        #direccion = dict{"xprv", "xpub", "ec", "wif", "ec_pub", "address"}
        pago=direccionesdepago(xprv_fin)
        arbol["pagos"].append(pago)
        print("\n-%4s...........: %s" %(i, pago["xprv"]))
        print("            xpub: " + pago["xpub"])
        print("      privada_ec: " + pago["ec"])
        print("     privada_wif: " + pago["wif"])
        print("      publica_ec: " + pago["ec_pub"])
        print("   address_p2pkh: " + pago["address_p2pkh"])
    return 1


def direccionesdepago(xprv_fin):
    """
    derivar las direcciones de pago finales a partir de una hd xprv.
     - Clave privada (XPrv) + Matematica de curva eliptica (EC) = Clave publica (XPub)
     - Clave publica + transformaciones = direccion bitcoin
    ec_privada, wif, ec_publica, address (P2PKH)....
    la ec_privada parece no ser demasiado interesante,
    suele ser mas utilizada en formato wif
    Secuencia: 
      <xprv>   =  Valor de entrada   ;  <xpub>  =  bx hd-public <xprv>
      <ec>     =  bx hd-to-ec <xprv>
      <wif>    =  bx ec-to-wif <ec>
      <ec_pub> =  bx wif-to-public <wif>
      <address_p2pkh>  = bx ec-to-address <ec_pub>
    """
    hd_new=" hd-new "
    hd_public=" hd-public "
    hd_to_ec=" hd-to-ec "
    ec_to_wif=" ec-to-wif "
    ec_to_address=" ec-to-address "
    # Limpiar direccion en cada llamada
    direccion={'xprv':"", 'xpub':"", 'ec':"", 'wif':"", 'ec_pub':"", 'address_p2pkh':""}
    direccion["xprv"]=xprv_fin
    direccion["xpub"]=\
        (os.popen("bx" + hd_public + (xprv_fin)).read()).rstrip("\n")
    #print ("\nbx" + hd_public + (xprv_fin))
    direccion["ec"]=\
        (os.popen("bx"+ hd_to_ec + xprv_fin).read()).rstrip("\n")
    direccion["wif"]=\
        (os.popen("bx"+ ec_to_wif + direccion["ec"]).read()).rstrip("\n")
    direccion["ec_pub"]=\
        (os.popen("bx wif-to-public " + direccion["wif"]).read()).rstrip("\n")
    direccion["address_p2pkh"]=(os.popen("bx"+ ec_to_address + direccion["ec_pub"]).read()).rstrip("\n")
    return direccion


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
