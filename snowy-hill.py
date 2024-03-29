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
import os # para poder ejecutar comandos de shell
import argparse #Manejo de argumentos en linea de comandos
import sys
from subprocess import Popen, PIPE
# Importaciones de terceros
# Importaciones locales


VERBOSE=False
DEPURA=False
FICHERO_CONFIGURACION_TESTNET="test.cfg"
FICHERO_CONFIGURACION_MAINNET="bx.cfg"
TESTNET=False
MAINNET=True # es redundante, lo hago para mejor lectura. 

########################################################################################
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
            mycartera.print_sencilla()
        else:
	        mycartera.print_consola()
        print("#=====================================")
        # Volcado de pagos a fichero
        if args.payfile:
            ficheropagos = args.payfile
            try:
                with open(ficheropagos, 'a') as f:
                    f.write("# %s\n%s" %(mycartera.esquema, mycartera.cadena_pagos()))
            except:
                print("Error al tratar de escribir en fichero (%s)" %(ficheropagos))

########################################################################################

class cartera:
    """Representa un almacen de claves que se derivan de una semilla 

    Realiza la derivacion de una familia de direcciones a raiz de una semilla.
    Se puede iniciar la derivacion a varias alturas.

        Attributes
            semilla (str[]): 
    """

    def __init__(self, entropia="", esquema="", contrasena="", entropiaAmnemonico=False, testnet=False):
        """ Constructor de la clase cartera

        No solo inicializa el objeto, en caso de que el argumente entropia no este
        vacio realiza toda la derivacion llamando a las funciones encargadas de realizarla. 

        Args:
            entropia (str): fuente de aleatoriedad
            esquema (str): esquema de derivacion
            contrasena (str): aplicacion BIP 39
            entropiaAmnemonico (bool): True = obtener frase mnemonica desde parametro entropia
                                       False = el parametro entropia representa la Seed
            testnet (bool): True = modo testnet
        Return:
               None ( ): nada
        """
        self.semilla=['', '', '', '', ''] # E, Mnemon, Seed, m, M
        self.indice_m=3 # posicion de m en semilla[]¿?
        self.esquema=""  #Esquema de derivacion en una sola cadena
        self.esquema_derivacion=[] # ["m","0'",...] # Esquema separado.
        self.esquema_pagos=[] # [ini, fin]
        self.HDxp=[]  # almacena [xpriv, xpub] de un determinado nivel
        self.pagos=[] # [[HD, ,...],[HD, ,...],[HD, ,...],...]
        self.testnet=False
        self.master_finger_print=""
        #self.MasterFingerPrint
        #bx hd-new $PPP| bx hd-to-ec |bx ec-to-public| bx bitcoin160 (primeros 4 Bytes)

        """
        Las siguientes variables almacenan los comandos de bx, con el
        objetivo de modificarlas, principalmente para testnet.
        """
        self.hd_new="hd-new "
        self.hd_public="hd-public "
        self.hd_to_public="hd-to-public "
        #self.hd_to_ec="hd-to-ec "
        #self.ec_to_wif="ec-to-wif "
        #self.ec_to_address="ec-to-address "

        self.testnet=testnet
        if (self.testnet):
            self.hd_new       ="hd-new --version 70615956 "
            self.hd_public    ="hd-public --config " + FICHERO_CONFIGURACION_TESTNET + " "  
            self.hd_to_public ="hd-to-public --version 70617039 "
            self.hd_to_ec     ="hd-to-ec --config test.cfg "
        else:
            # 76066276, 049d7878 to produce a "yprv" prefix. Testnet uses 0x044a5262 "upub" and 0x044a4e28 "uprv."
            self.hd_new       ="hd-new " 
            self.hd_public    ="hd-public "
            self.hd_to_public ="hd-to-public "
            self.hd_to_ec     ="hd-to-ec "

        if (esquema):
            self.esquema = esquema
            self.esquema_derivacion = self.esquema.split("/")
        self.contrasena=contrasena

        if (entropia): # Si se inicializa con un valor de entropia desarrollamos
            self.desplegar_seed(entropia,entropiaAmnemonico) 
            self.desplegar_HD()
            self.calculo_m_finger_p()

    def desplegar_seed(self, entropia, entropiaAmnemonico=False):
        """
        La familia de claves se deriva a partir de la semilla (seed) con un cierto formato.
        Pero se puede iniciar la secuencia antes: E -> mnemonico [+ passw] -> seed
        Esta clase permite derivar desde cualquier posicion. Para ello el parametro
        <entropia> se matiza segun:
        Si <entropiaAmnemonico> es True: representa el valor E
        Sino SI contiene mas de una cadena: se trata de una frase mnemonica
        En otro caso: representa seed
        ... PROPUESTA: SI NO FACILITA <ESQUEMA> SOLO SE DESARROLLA HASTA EL SEED. 
        """

        if(entropiaAmnemonico): # Si es true se debe generar una frase a partir de la entropia
            i=0
        else:
            frase = entropia.split() # puede ser una frase o una semilla, decision a continuacion
            if(len(frase)>1): #Si contiene mas de una palabra es un mnemonico
                i=1
            else: # en otro caso <entropia> contiene el Seed. No contamos con el mnemonico.
                i=2
        self.semilla[i]=entropia # Almacenar entropia en la posicion adecuada.
        parametro_contrasena = " -p \"%s\" " %(self.contrasena)

        # Almaceno las funciones a utilizar en la derivacion.
        lderivacion=[lambda E: (os.popen("bx mnemonic-new " + E).read()).rstrip("\n"),\
                 lambda Mn:(os.popen("bx mnemonic-to-seed " + Mn + parametro_contrasena).read()).rstrip("\n"),\
                lambda S: (os.popen("bx "+ self.hd_new + S).read()).rstrip("\n") ,\
#                lambda Pr:(os.popen("bx hd-private -i %s %s %s " %(indice, duro, Pr)).read()).rstrip("\n"),\
                lambda m:(os.popen("bx " + self.hd_to_public + m).read()).rstrip("\n"),\
                ]

        for j in range(i,len(lderivacion)):
            self.semilla[j+1]=lderivacion[j](self.semilla[j])


    def desplegar_HD(self):
        """
        Organiza el recorrido por la cadena de derivacion para las HD 
        """
        # Y continuamos descendiendo
        ultima_derivacion = len(self.esquema_derivacion)
        n_deriva=0
        for indice in self.esquema_derivacion[:]: # El ultimo se trabaja de manera especial
            n_deriva += 1
            indice=indice.strip() # Limpiar espacio en blanco
            if "'" in indice:
                parametro_dureza=" --hard "
            else:
                parametro_dureza=""
            indice=indice.strip("'") # Limpiar

            # HDxp=[]  # almacena [xpriv, xpub] de un determinado nivel.
            # pagos=[] # [[HD, ,...],[HD, ,...],[HD, ,...],...]
            # La clave identificada como m o M es especial.
            if indice == "m":
                self.HDxp.append(self.semilla[self.indice_m : self.indice_m+2])
                continue
            else:
                pass

            siguienteHD = lambda HDpadre,_indice_ : self.desarrollo_hd(HDpadre, _indice_, parametro_dureza)
            if n_deriva < ultima_derivacion:
                self.HDxp.append(siguienteHD(self.HDxp[-1][0], indice))  #([xprv, xpub])
            else: # Si quiero generar varias direcciones de pago lo indico los valores inicial y final: i,j
                finales_derivacion =  indice.split(",")  #(self.esquema_derivacion[-1].strip("'")).split(",")
                # Los finales los guardo en su sitio.
                for i in range(int(finales_derivacion[0]), int(finales_derivacion[-1])+1):
                    # en el rango se pone +1 al segundo extremo porque range queda por debajo.
                    temp_HDsiguiente = siguienteHD(self.HDxp[-1][0],i)[0]   # , i, self.testnet)
                    temp_pago = direccion_pago(temp_HDsiguiente, i, self.testnet)
                    self.pagos.append(temp_pago)


    def desarrollo_hd(self, origen, indice, parametro_dureza=""):
        """
        Calculo de los XPRV y XPUB
        """
        xprv = (os.popen("bx hd-private -i %s %s %s " %(indice, parametro_dureza, origen)).read()).rstrip("\n")
        xpub = (os.popen("bx  " + self.hd_to_public + xprv).read()).rstrip("\n")
        return [xprv, xpub]

    def calculo_m_finger_p(self):
        """
        Calcula la huella dactilar de la cartera.
        """
        calculo="bx " + self.hd_to_ec +" "+ self.semilla[self.indice_m] + " | bx ec-to-public | bx bitcoin160"
        temp= (os.popen(calculo).read()).rstrip('\n')
        self.master_finger_print=temp[0:8]

    def arbol(self, seed, esquema ):
        """
        PENDIENTE
        (no recuerdo que queria hacer aqui)
        """
        pass

    def pago(self, xprv):
        """
        PENDIENTE
        (no recuerdo que queria hacer aqui)
        """
        pass

    def print_consola(self, pagos=True):
        """
        Visualizar los datos por consola. Formato por defecto
        """

        print("Entropia  : " + self.semilla[0])
        print("mnemonico : " + self.semilla[1])
        print("Seed      : " + self.semilla[2])
        print("Esquema   : " + self.esquema)
        print("M. FingerP: " + self.master_finger_print)

        i=0
        for HD in self.HDxp :
            try :
                nivel = self.esquema_derivacion[i]
                print ("- %4s: %s" %(nivel, HD[0])) #(self.HDxp[i])[0]))
                if VERBOSE:
                    print ("      - %s" %(HD[1])) #(self.HDxp[i])[1]))
            except:
                print("Error. Nos salimos del array HDxp.", sys.exc_info()[0])
            i+=1
        if pagos:
            for p in self.pagos:
                p.print_consola()

    def print_sencilla(self, pagos=True):
        """
        Visualizar los datos por consola. Formato sencillo con menos datos
        """
        print("mnemonico : " + self.semilla[1])
        print("Seed      : " + self.semilla[2])
        print("Esquema   : " + self.esquema)
        print("M. FingerP: " + self.master_finger_print)
        print("")
        i=0
        for HD in self.HDxp :
            try :
                nivel = self.esquema_derivacion[i]
                print ("- %4s: %s" %(nivel, HD[0])) #(self.HDxp[i])[0]))
                if VERBOSE:
                    print ("      - %s" %(HD[1])) #(self.HDxp[i])[1]))
            except:
                print("Error. Nos salimos del array HDxp.", sys.exc_info()[0])
            i+=1
        print("")
        if pagos:
            for p in self.pagos:
                print("%s" %(p.cadena_wif()))
                print("%s" %(p.cadena_p2pkh()))
                print("")

    def print_massencilla(self, pagos=True):
        """
        Visualizar los datos por consola. Formato mas sencillo aun menos datos
        """
        print("mnemonico : " + self.semilla[1])
        print("Seed      : " + self.semilla[2])
        print("Esquema   : " + self.esquema)
        print("M. FingerP: " + self.master_finger_print)
        print("")
        if pagos:
            for p in self.pagos:
                print("%s" %(p.cadena_wif()))
                print("%s" %(p.cadena_p2pkh()))
                print("")

    def cadena_pagos(self, pagos=True):
        cadena=""
        for p in self.pagos:
            cadena+=p.cadena_p2pkh()+"\n"
        return cadena

########################################################################################

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

########################################################################################

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
        else: #Las xpriv o pub de la derivacion que no sean m o M las anadirmos a la lista xpriv[]
            y = x.rstrip("'") # quito la marca de dureza, ya se ha registrado en variable "duro". 
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
    for i in range(int(y[0]),int(y[-1])+1): # y[-1] representa el ultimo elemento del array. Range no incluye el ultimo por eso +1
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

########################################################################################

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

########################################################################################

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

########################################################################################

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


