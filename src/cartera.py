class cartera:
    """Representa un almacen de claves que se derivan de una semilla 
    Realiza la derivacion de una familia de direcciones a raiz de una semilla.
    Se puede iniciar la derivacion a varias alturas.
    Attributes
    - semilla (str[]): 
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
