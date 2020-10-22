########################################################################################
# derivadordellaves.py
# Generacion de una cartera (en mainnet y testnet).
# La obtencion de las llaves privadas y publicas a partir de una semilla
#  implica una serie de pasos poco intuitivos. Esta herramienta facilita esta
#  labor y puede ayudar a conocer como se realiza dicha derivacion.
#  - n (12, 24...) palabras (jaxx p.e. pide 12)
#  - Diccionario Ingles. Mas estandar
#
#
# partiendo de una semilla o una frase o una privkey. generar direcciones de interes.
# Utilizar conmutador para testnet
#
#semilla
#mnemonico
#seed
#xpriv (m)
#xpub (M)
#P2PK
#P2PKH
#P2SH
#BENCH
########################################################################################

import os # para poder ejecutar comandos de shell
import argparse #Manejo de argumentos en linea de comandos
import sys
from subprocess import Popen, PIPE


### CONSTANTES # Comentadas porque no las utilizo  finalmente.
#BIP141= "m/0/0"
#BIP84 = "m/84'/0'/0'/0/0"
#BIP49 = "m/49'/0'/0'/0/0"
#BIP44 = "m/44'/0'/0'/0/0"
#BIP44T = "m/44'/1'/0'/0/0"
#BIP32 = "m/0/0"

### Variables globales: 
"""
 Las siguientes variables almacenan los comandos de bx, con el 
 objetivo de modificarlas, principalmente para testnet.
"""
hd_new="hd-new "
hd_public="hd-public "
hd_to_ec="hd-to-ec "
ec_to_wif="ec-to-wif "
ec_to_address="ec-to-address "


### Funciones: ###

########################################################################################
def main():
    'Funcion inicial.'
    global hd_new
    global hd_public
    global hd_to_ec
    global ec_to_wif
    global ec_to_address

    # Comprobar que existe el programa bx
    try:
#        Popen(['bx', '--help'], stdout=PIPE, stderr=PIPE)
        Popen('bx', stdout=PIPE, stderr=PIPE)
    except OSError:
        msg = "No puedo ejecutar bx, necesario para la derivación.\nLocalizable en https://github.com/libbitcoin/libbitcoin-explorer\n"
        sys.exit(msg)


    parser = argparse.ArgumentParser()
    parser = argparse.ArgumentParser(description='%(prog)s : Derivar arbol de claves BTC.')

    #parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter,\
    #    description='%(prog)s : Derivar arbol de claves BTC.\n\
    #     Entropia, uno de los siguientes:\n\
    #        (E)  : Valor utilizado como origen aleatorio, derivara en mnemonico. Normalizado en Base16, debe tener una logitud divisible entre 32.\n\
    #        frase: mnemonico (BIP39), derivara en seed.\n\
    #        seed : representacion numerica del mnemonico bip39, \n\
    #')

    parser.add_argument("-v", "--verbose", help="Mostrar información de depuración", action="store_true")
    parser.add_argument("-f", "--file", help="Nombre de archivo a procesar")
    parser.add_argument("-t", "--testnet", help="Realizar la derivacion en TESTNET", action="store_true")
    parser.add_argument("-d", "--derivarmnemonico", help="El valor de entropia deriva el mnemonico", action="store_true")
    parser.add_argument("-e", "--esquema", help="Esquema de derivación. eje: m/44'/0'/0'/0/0")
    parser.add_argument("-s", "--secreto", help="Contraseña para añadir al mnemonico")
    parser.add_argument("-j", "--ejemplo", help="La cadena <entropia> se expandira (x32) y se utilizara esquema BIP44.", action="store_true")
    parser.add_argument("entropia", help="Origen de la derivación (semilla (E), mnemonico, seed, xpriv...)")
    args = parser.parse_args()

    # Almacenar el valor <entropia> en variable para separar lo del esquema de argumentos.
    semilla=args.entropia
    entropiaAmnemonico=args.derivarmnemonico

    # Aquí procesamos lo que se tiene que hacer con cada argumento

    if args.ejemplo: # Defino unos valores para usarlos como ejemplo y estudio.
        semilla=semilla*32 # cadena multiplo de 32
        entropiaAmnemonico=True # El ejemplo debe derivar desde entropia a mnemonico

    if args.secreto:
        secreto=args.secreto
    else:
        secreto=""

    if (args.testnet):
        hd_new       =" hd-new --version 70615956 "
        hd_public    =" hd-public --config test.cfg "  #no funciona con --version 70617039
        hd_to_ec     =" hd-to-ec --config test.cfg "
        ec_to_wif    =" ec-to-wif --version 239 " # (-u)
        ec_to_address=" ec-to-address --version 111 "
        BIP44 = "m/44'/1'/0'/0/0"
    else:
        hd_new       =" hd-new "
        hd_public    =" hd-public "
        hd_to_ec     =" hd-to-ec "
        ec_to_wif    =" ec-to-wif " # (-u)
        ec_to_address=" ec-to-address "
        BIP44 = "m/44'/0'/0'/0/0"

    if args.esquema:
        esquema = args.esquema
    else: 
        esquema=BIP44

    if args.verbose:
        print(semilla)
        print(esquema)
        print(secreto)
        print(entropiaAmnemonico)



    #direccion = dict{"xprv", "xpub", "ec", "wif", "ec_pub", "address"}
    arbol=dict()
    arbol={'E':"",'mnemonico':"",'contrasena':"",'seed':"",'esquema':"",'m':'', 'M':'','xpriv':[], 'xpub':[], 'pagos':[]}
    direccion = dict() # Definir variable tipo diccionario
    direccion={'xprv':"", 'xpub':"", 'ec':"", 'wif':"", 'ec_pub':"", 'address_p2pkh':""}

    print("=====================================")
#    procesar_parametros()
    derivacion(semilla, esquema, secreto, entropiaAmnemonico)
    print("=====================================")



########################################################################################
class cartera:
    """
    Realiza la derivacion de una familia de direcciones a raiz de una semilla. 
    Se puede iniciar la derivacion a varias alturas. 
    """
    E=''          # Valor utilizado como origen aleatorio
    mnemonico=''  # Frase mnemonica
    contrasena='' # cadena que unida a mnemonico generara la semilla
    seed=''       # Semilla para generar la familia de claves
    esquema=''    # Esquema de derivacion, ejemplo:  m/44'/0'/0'/0/0
    m=''
    M=''
    xpriv=''
    xpub=''
    pagos=[]

    def __init__(self, entropia, esquema="m/44'/0'/0'/0/0", contrasena="", entropiaAmnemonico=False):
        """
        Inicializa el objeto. Si entropia contiene dato se despliega la derivacion.
        """
        if (entropia):
            self.desplegar_seed(entropia, esquema="m/44'/0'/0'/0/0", contrasena="", entropiaAmnemonico=False) 

    def desplegar_seed(self, entropia, esquema="m/44'/0'/0'/0/0", contrasena="", entropiaAmnemonico=False):
        """
        La familia de claves se deriva a partir de la semilla (seed) con un cierto formato.
        Pero se puede iniciar la secuencia antes: E -> mnemonico [+ passw] -> seed
        Esta clase permite derivar desde cualquier posicion. Para ello el parametro
        <entropia> se matiza segun:
        Si <entropiaAmneminico> es True: representa el valor E
        Sino SI contiene mas de una cadena: se trata de una frase mnemonica
        En otro caso: representa seed
        ... PROPUESTA: SI NO FACILITA <ESQUEMA> SOLO SE DESARROLLA HASTA EL SEED. 
        """

        frase = '' # entropia.split() # puede ser una frase o una semilla, decision a continuacion

        if(entropiaAmnemonico): # Si es true se debe generar una frase a partir de la entropia
            self.E=entropia
            self.mnemonico=(os.popen("bx mnemonic-new " + self.E).read()).rstrip("\n")
            frase = self.mnemonico.split()
        else: 
            frase = entropia.split() 
            if(len(frase)>1): #Si contiene mas de una palabra es un mnemonico
                self.mnemonico=entropia
            else: # en otro caso <entropia> contiene el Seed. No contamos con el mnemonico.
                self.seed=entropia

        if(self.mnenomico): #Si mnemonico contiene datos...
            self.contrasena=contrasena
            parametro_contrasena = " -p \"%s\" " %(self.contrasena)
            self.seed=(os.popen("bx mnemonic-to-seed " + self.mnemonico + parametro_contrasena).read()).rstrip("\n")
        # En caso contrario <mnemonico> estará vacio y <seed> contrendra el valor de entropia 
        
        # SIGUIENTES PASOS
        # - RECORRER EL ARBOL DE DERIVACION: NUEVO METODO
        # - GENERAR LAS CORRESPONDIENTES DIRECCIONES DE PAGO. NUEVO METODO. 
        def arbol(self, seed, esquema): 
            pass
        def pago(self, xprv):
            pass
        def print(self):
            pass




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
    global hd_new
    global hd_public
    global hd_to_ec
    global ec_to_wif
    global ec_to_address

    arbol={'E':"",'mnemonico':"",'contrasena':contrasena,'seed':"",'esquema':esquema,'m':'', 'M':'','xpriv':[], 'xpub':[], 'pagos':[]}
    #mnemonico=""
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

    #arbol={'esquema':esquema,'contrasena':contrasena,
    # ... 'E':"",'mnemonico':"",'seed':"",'m':'','M':'','xpriv':[],'xpub':[],'pagos':[]}
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
class direccion_pago(object):
    xprv=""
    xpub=""
    ec=""
    wif=""
    ec_pub=""
    address_p2pkh=""

    def __init__(privada):
        self.xprv = privada

    def deriva(self):
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
        self.xpub         =(os.popen("bx" + hd_public + (self.xprv)).read()).rstrip("\n")
        self.ec           =(os.popen("bx"+ hd_to_ec + self.xprv).read()).rstrip("\n")
        self.wif          =(os.popen("bx"+ ec_to_wif + self.ec).read()).rstrip("\n")
        self.ec_pub       =(os.popen("bx wif-to-public " + self.wif).read()).rstrip("\n")
        self.address_p2pkh=(os.popen("bx"+ ec_to_address + self.ec_pub).read()).rstrip("\n")



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
    global hd_new
    global hd_public
    global hd_to_ec
    global ec_to_wif
    global ec_to_address

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
    #direccion["xprv"]=xprv_fin
    direccion["wif"]=wif
    direccion["ec"]=(os.popen("bx wif-to-ec "+ wif).read()).rstrip("\n")
    #direccion["wif"]=(os.popen("bx"+ ec_to_wif + direccion["ec"]).read()).rstrip("\n")
    direccion["ec_pub"]=(os.popen("bx wif-to-public " + direccion["wif"]).read()).rstrip("\n")
    direccion["address_p2pkh"]=(os.popen("bx"+ ec_to_address + direccion["ec_pub"]).read()).rstrip("\n")
    return direccion

    privada_wif  = wif.rstrip("\n")
    publica_ec = (os.popen("bx wif-to-public " + privada_wif).read()).rstrip("\n")
    address_p2pkh = (os.popen("bx"+ ec_to_address + publica_ec).read()).rstrip("\n")
    priv_ec = (os.popen("bx wif-to-ec " + privada_wif).read()).rstrip("\n")
    xpriv_de_wif = (os.popen("bx" + hd_new +  priv_ec).read()).rstrip("\n")


########################################################################################
### Llamar a funcion principal.###
main()
