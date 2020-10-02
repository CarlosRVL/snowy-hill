# derivadordellaves.py
# Generacion de una cartera (en mainnet y testnet).
# La obtencion de las llaves privadas y publicas a partir de una semilla
#  implica una serie de pasos poco intuitivos. Esta herramienta facilita esta
#  labor y puede ayudar a conocer como se realiza dicha derivacion.
#  - n (12, 24...) palabras (jaxx p.e. pide 12)
#  - Diccionario Ingles. Mas estandar
#

# partiendo de una semilla o una frase o una privkey. generar direcciones de interes.
# Utilizar conmutador para testnet
"""
semilla
mnemonico
seed
xpriv (m)
xpub (M)
P2PK
P2PKH
P2SH
BENCH
"""

import os # para poder ejecutar comandos de shell
# <cadena> seed o frase mnemonico
# <cadena> derivacion
# <cadena> xpriv
import argparse #Manejo de argumentos en linea de comandos
parser = argparse.ArgumentParser()
parser = argparse.ArgumentParser(description='%(prog)s : Derivar arbol de claves BTC.')

# parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter,\
#     description='%(prog)s : Derivar arbol de claves BTC.\n\
#      Entropia, uno de los siguientes:\n\
#         (E)  : Valor utilizado como origen aleatorio, derivara en mnemonico. Normalizado en Base16, debe tener una logitud divisible entre 32.\n\
#         frase: mnemonico (BIP39), derivara en seed.\n\
#         seed : representacion numerica del mnemonico bip39, \n\
# ')

parser.add_argument("-v", "--verbose", help="Mostrar información de depuración", action="store_true")
parser.add_argument("-f", "--file", help="Nombre de archivo a procesar")
parser.add_argument("-t", "--testnet", help="Realizar la derivacion en TESTNET", action="store_true")
parser.add_argument("-d", "--derivarmnemonico", help="El valor de entropia deriva el mnemonico", action="store_true")
parser.add_argument("-e", "--esquema", help="Esquema de derivación. eje: m/44'/0'/0'/0/0")
parser.add_argument("-s", "--secreto", help="contraseña para añadir al mnemonico")
parser.add_argument("entropia", help="Origen de la derivación (semilla (E), mnemonico, seed, xpriv...)")
args = parser.parse_args()

# Aquí procesamos lo que se tiene que hacer con cada argumento

if args.secreto:
    secreto=args.secreto
else:
    secreto=""

entropiaAmnemonico=args.derivarmnemonico

semilla=args.entropia

if args.verbose:
    print(semilla)
    print(esquema)
    print(secreto)
    print(entropiaAmnemonico)

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
else: #Testnet
    esquema=BIP44

###############################################

BIP141= "m/0/0"
BIP84 = "m/84'/0'/0'/0/0"
BIP49 = "m/49'/0'/0'/0/0"
BIP44 = "m/44'/0'/0'/0/0"
BIP44T = "m/44'/1'/0'/0/0"
BIP32 = "m/0/0"

#direccion = dict{"xprv", "xpub", "ec", "wif", "ec_pub", "address"}
arbol=dict()
arbol={'E':"",'mnemonico':"",'contrasena':"",'seed':"",'esquema':"",'m':'', 'M':'','xpriv':[], 'xpub':[], 'pagos':[]}
direccion = dict() # Definir variable tipo diccionario
direccion={'xprv':"", 'xpub':"", 'ec':"", 'wif':"", 'ec_pub':"", 'address_p2pkh':""}


# semilla, mnemonic, seed, hd, hd, hd, ... (ec, wif, public addres)
def derivacion(entropia, esquema="m/44'/0'/0'/0/0", contrasena="", entropiaAmnemonico=False):
    # Entropia puede ser un valor de entropia inicial (E), una frase, o un seed.
    #     (E): Valor utilizado como origen aleatorio. Normalizado en Base16, debe tener una logitud divisible entre 32
    #     frase: mnemonico (BIP39)
    #     seed: representacion numerica del mnemonico bip39
    # arbol=dict()
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
        arbol["seed"]=(os.popen("bx mnemonic-to-seed " + contrasena + arbol["mnemonico"]).read()).rstrip("\n")
    else:
        arbol["seed"] = entropia

#    print("\n")
    print("mnemonico : " + arbol["mnemonico"])
    print("Seed      : " + arbol["seed"])
    print("Esquema   : " + arbol["esquema"])

#arbol={'esquema':esquema,'contrasena':contrasena,
# ... 'E':"",'mnemonico':"",'seed':"",'m':'','M':'','xpriv':[],'xpub':[],'pagos':[]}
    deriva = arbol["esquema"].split("/")
    temporal=arbol["seed"]
    for x in deriva[:-1]: #ultima especial
        x.strip() #Eliminar blancos
        if "'" in x:
            duro=" --hard "
        else:
            duro=""

        if x == "m":
            #xpriv_m=(os.popen("bx"+ hd_new + seed).read()).rstrip("\n")
            #print ("Depuracion 139: bx"+ hd_new + arbol["seed"]+"\n")
            arbol["m"]=(os.popen("bx"+ hd_new + arbol["seed"]).read()).rstrip("\n")
            temporal = arbol["m"]
            print ( " - %4s: %s" %(x,arbol["m"]))
        else: #Las xpriv o pub de la derivacion que no sean m o M las anadirmos a la lista xpriv[]
            y = x.rstrip("'")
            # La derivacion itera sobre la xpriv anterior, guardada en temporal
            temporal=(os.popen("bx hd-private -i %s %s %s" %(y, duro, temporal)).read()).rstrip("\n")
            arbol["xpriv"].append(temporal)
            #arbol["xpub"].append((os.popen("bx hd-public -i %s %s %s" %(y, duro, temporal)).read()).rstrip("\n"))
            # Modo Depuracion
            arbol["xpub"].append((os.popen("bx hd-public -i %s %s %s" %(y, duro, temporal)).read()).rstrip("\n") + " Depura: con i y dureza")
            print ( " - %4s: %s" %(x,arbol["xpriv"][-1]))
            #print ( "Pb %4s: %s" %(x,arbol["xpub"][-1]))
    #procesar ultima: deriva[-1]
    # si x es en la forma n,m generar familia.
    if "'" in deriva[-1]:
        duro=" --hard "
    else:
        duro=""
    y = (deriva[-1].strip("'")).split(",")
    for i in range(int(y[0]),int(y[-1])+1):
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

# funcion direccionesdepago
# derivar las direcciones de pago finales a partir de una hd xprv.
# ec_privada, wif, ec_publica, address (P2PKH)....
# la ec_privada parece no ser demasiado interesante,
# suele ser mas utilizada en formato wif
def direccionesdepago(xprv_fin):
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


# Funcion DesdeWif
# Para estudiar la derivacion que realiza el cliente Bitcoin Colore
# tratando de encontrar un punto de union con otro software de billetera.
def DesdeWif(wif):
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

###############################################################
### Inicio principal
###############################################################
# Comprobar que existe el programa bx
print("=====================================")
derivacion(semilla, esquema, secreto, entropiaAmnemonico)
print("=====================================")
#DesdeWif(wif_DerivarP2SH)
