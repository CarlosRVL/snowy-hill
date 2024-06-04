""" pago.py
Generación de las direcciones de pago
"""

import os  # para poder ejecutar comandos de shell
from src.depura import _depurame_

FICHERO_CONFIGURACION_TESTNET="test.cfg"
FICHERO_CONFIGURACION_MAINNET="bx.cfg"

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
