# snowy-hill
# Estudio de la derivación de claves con bx (Colina nevada)

## Agradecimientos

Rindo homenaje a varias personas que me han inspirado en la madriguera Bitcoin y en la creación de valor:

- Alberto Mera
- Lunaticoin
- Arkad
- Decentralized
- Alfredo Romeo (Datta Capital)
- https://www.bitcoin-1o1.info/
- Carlos Matinez (interescompuesto)

## Aviso

Esta herramienta tiene objetivos educacionales. Aunque podría ser utilizada para producir o manejar tus frases mnemónicas o tus claves publicas y privadas ello supone un riesgo para tu privacidad y la seguridad de tus fondos.

### Ejemplo de salida:

Muestro un ejemplo sencillo utilizando el parametro ``-j``, que se utiliza justamente para producir ejemplo rápidamente.

~~~ 
snowy-hill$ python3 snowy-hill.py  -j 0
#=====================================
Entropia  : 00000000000000000000000000000000
mnemonico : abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon about
Seed      : 5eb00bbddcf069084889a8ab9155568165f5c453ccb85e70811aaed6f6da5fc19a5ac40b389cd370d086206dec8aa6c43daea6690f20ad3d8d48b2d2ce9e38e4
Esquema   : m/44'/0'/0'/0/0
M. FingerP: 73c5da0a
-    m: xprv9s21ZrQH143K3GJpoapnV8SFfukcVBSfeCficPSGfubmSFDxo1kuHnLisriDvSnRRuL2Qrg5ggqHKNVpxR86QEC8w35uxmGoggxtQTPvfUu
-  44': xprv9ukW2Usuz4v9T49296K5xDezLcFCEaGoLo3YGAJNuFmx1McKebuH2S5C5VhaFsBxuChmARtTHRLKnmLjRSL7vGuyDrCaBh7mfdyefDdp5hh
-   0': xprv9wnZLsHUEcR3UVuysrCTjAu7FWKXN2m5XVrgkEmeptHqi5yNkR8seouPutDWAJQcUPYDzTDgjK7G1h53M4QeA4myt6gUSUgdFhQSYw7XAV4
-   0': xprv9xpXFhFpqdQK3TmytPBqXtGSwS3DLjojFhTGht8gwAAii8py5X6pxeBnQ6ehJiyJ6nDjWGJfZ95WxByFXVkDxHXrqu53WCRGypk2ttuqncb
-    0: xprvA1Lvv1qpvx3f8iuRHfaEG45fyvDc3h7Ur5afz5SyRfkAsZ2765KfFfmg6Q9oEJDgf4UdYHphzzJybLykZfznUMKL2KNUU8pLRQgstN5kmFe

-    0: xprvA2cWYEXRrpaYZmR4Mat3aHw7ARSGFAtb5LQNfSuyQCCGVJXRNWA3zkkHZcBM4voi9TBrb9WaC65HGv5e8gZgfnjzH71WofaXT3haLw8LYqQ
  xpub: xpub6Fbrwk4KhC8qnFVXTcR3wRsqiTGkedcSSZKyTqKaxXjFN6rZv3UJYZ4mQtjNYY3gCa181iCHSBWyWst2PFiXBKgLpFVSdcyLbHyAahin8pd
prv_ec: e284129cc0922579a535bbf4d1a3b25773090d28c909bc0fed73b5e0222cc372
   wif: L4p2b9VAf8k5aUahF1JCJUzZkgNEAqLfq8DDdQiyAprQAKSbu8hf
pub_ec: 03aaeb52dd7494c361049de67cc680e83ebcbbbdbeb13637d92cd845f70308af5e
 p2pkh: 1LqBGSKuX5yYUonjxT5qGfpUsXKYYWeabA
#=====================================
~~~

### Ayuda 

~~~
snowy-hill$ python3 snowy-hill.py -h
usage: snowy-hill.py [-h] [-v] [-f FILE] [-t] [-d] [-e ESQUEMA] [-s SECRETO] [-j] [-p PAYFILE] [-o] [-c] [-cc]
                     entropia

snowy-hill.py : Derivar arbol de claves BTC según el BIP32. El parámetro ENTROPIA puede representar en realidad
varias cosas: 1.- Múltiplo de 32 bits llamado ENTROPY en el BIP39, del que derivar la frase mnemonica, en este caso
debe aparecer el parámetro "-d" 2.- La frase mnemónica, entre parentesis y separada por espacios. OJO: no se
verifica que la frase cumpla BIP39. 3.- La Seed fuente de la generación de billeteras deterministas jerárquicas
descrita en BIP32

positional arguments:
  entropia              Origen de la derivación (Entropia, Mnemonico, Seed, xpriv...)

optional arguments:
  -h, --help            show this help message and exit
  -v, --verbose         Mostrar información de depuración
  -f FILE, --file FILE  Nombre de archivo a procesar. SIN IMPLEMENTAR AUN
  -t, --testnet         Realizar la derivacion en TESTNET
  -d, --derivarmnemonico
                        El valor de entropia deriva el mnemonico
  -e ESQUEMA, --esquema ESQUEMA
                        Esquema de derivación. eje: m/44'/0'/0'/0/0 (Se utiliza m/44'/0'/0'/0/x,y para generar
                        direcciones de pago desde x hasta y)
  -s SECRETO, --secreto SECRETO
                        Contraseña para añadir al mnemonico
  -j, --ejemplo         La cadena <entropia> se expandira (x32) y se utilizara esquema BIP44.
  -p PAYFILE, --payfile PAYFILE
                        Nombre del archivo en el que guardar las direcciones de pago.
  -o, --old             Ejecutar la version antigua.
  -c, --corto           Mostrar salida corta.
  -cc, --mascorto       Mostrar salida mas corta.
~~~

## Introducción

Esta herramienta es similar y en parte inspirada por la de Ian Coleman. El proposito es disponer de la misma funcionalidad de la herramienta de Ian Coleman pero en modo comando que permita un modo más rápido de general resultados enfocados al estudio de la derivación. 

Se puede utilizar para generar tus propias llaves utilizando alguna fuente de entropía, pero no se garantiza la seguridad, especialmente en cuanto a privacidad.

La obtencion de las llaves privadas y publicas a partir de una semilla implica una serie de pasos poco intuitivos. Esta herramienta facilita esta labor y puede ayudar a conocer como se realiza dicha derivacion.

Se utiliza el diccionario Ingles y se recomienda que no se utilice ningún otro diccionario. 

Partiendo de una semilla o una frase o una privkey. generar direcciones de interes.
 
Me parece fundamental que cualquier herramienta cuente con un modo textnet, está también. 


[//]: # (semilla)
[//]: # mnemonico
[//]: # seed
#xpriv (m)
#xpub (M)
#P2PK
#P2PKH
#P2SH
#BENCH

