# snowy-hill
# Estudio de la derivación de claves con bx

## Agradecimientos

Rindo homenaje a varias personas que me han inspirado en la madriguera Bitcoin y en la creación de valor:

- Alberto Mera
- Lunaticoin
- Arkad
- Decentralized
- Alfredo Romeo (Datta Capital)
- https://www.bitcoin-1o1.info/
- Carlos Matinez (interescompuesto)
- Joan Tubau (Kapital)

## Aviso

Esta herramienta tiene objetivos educacionales. Aunque podría ser utilizada para producir o manejar tus frases mnemónicas o tus claves publicas y privadas ello supone un riesgo para tu privacidad y la seguridad de tus fondos.

## Introducción
Cuando nos enfrentamos a la custodia de Bitcoin nos encontramos con que tenemos que *generar* unas *palabras*, que se suelen identificar como una clave privada, y a partir estas se generan *mágicamente* las direcciones bitcoin. Esta herramienta ayuda a desvelar la mágia. Es similar (e inspirada) a la de *Ian Coleman*, buscando la ejecución y salida en linea de comandos.

Se puede utilizar para generar tus propias llaves utilizando alguna fuente de entropía, pero no se garantiza la seguridad, especialmente en cuanto a privacidad.

Me parece fundamental que cualquier herramienta cuente con un modo __testnet__. El parametro -t permite utilizar el modo testnet. 

De momento no llego más allá de las direcciones Legacy. Queda pendiente la implementación de la derivación Segwit y Taproot. 

### Requisitos
Esta herramienta se ha pensado para ejecutarse en Linux. Requiere python y libbitcoin-explorer (bx) (https://github.com/libbitcoin/libbitcoin-explorer.git)
Se puede descargar un ejecutable ya compilado de (https://github.com/libbitcoin/libbitcoin-explorer/wiki/Download-BX)
Es necesario que la ruta al comando "bx" esté se en el PATH. 


## Qué hace la herramienta. La derivación de llaves
La obtencion de las llaves privadas y publicas a partir de una semilla implica una serie de pasos poco intuitivos. Esta herramienta quiere visualizar esos pasos para facilitar el estudio de como se realiza dicha derivacion. Estamos hablando de lo definido en: 

- BIT0039 [^BIP39-1] Implementación de mnemónico.
  
  BIT39 define el modo en que a partir de un número (múltiplo de 32 bits), al que llama **entropia** inicial, se obtiene una frase **mnemónica** (conocida como <<las 12 o 24 palabras>>). El número de palabras dependerá de la longitud de la entropía inicial. También define la manera en que, a partir del mnemónico, se deriva una **semilla** (**SEED**)

- BIP0032 [^BIP32-1] Generación de wallet determinista.
  
  BIT32 define una forma de generar una wallet jerárquica determinista. Es lo que permite tener miles de direcciones a partir de una sola semilla. 

- El termino **cadena de derivación** se refiere a una cadena, por ejemplo: **m/44'/0'/0'/0/0** , que representa los pasos que se dan para llegar desde la semilla hasta las direcciones de pago.
  

[^BIP39-1]: (https://en.bitcoin.it/wiki/BIP_0039) (https://github.com/bitcoin/bips/blob/master/bip-0039.mediawiki)
[^BIP32-1]: (https://en.bitcoin.it/wiki/BIP_0032) (https://github.com/bitcoin/bips/blob/master/bip-0032.mediawiki)

Se utiliza el diccionario Ingles y se recomienda que no se utilice ningún otro diccionario. 

Los parametro permiten definir el punto de partida, pudiendo partir de la entropia, la semilla, la frase o una privkey, y generará las direcciones de pago de interes. 


[//]: # (semilla)
[//]: # (mnemonico)
[//]: # (seed xpriv m, xpub M, P2PK P2PKH P2SH BENCH )


## Ejemplo de salida y explicación

### Ejemplo sencillo utilizando el parametro ``-j``, que se utiliza justamente para producir ejemplo rápidamente.

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

Lo que estamos viendo es una derivación que parte de un valor *entropy* (el parametro -j X expande un valor hexadecimal X 32 veces y lo pasa como *entropy*, y utiliza el esquema BIP44) 
- Esa **Entropia** es transformada en el **mnemonico** (bx mnemonic-new 00000000000000000000000000000000). 
- Del **mnemonico** se deriva la **Seed** (bx mnemonic-to-seed "abandon abandon...about"). Hasta aquí se ha aplicado el **BIP39**. 

He añadido el calculo del fingerprint. Se calcula partiendo de **m** (bx hd-to-ec \<m\> | bx ec-to-public | bx bitcoin160) y tomando los 8 primeros Bytes.      

Ahora pasamos a aplicar BIP32 y BIP44:

- A esta semilla se la hace pasar por el esquema *m/44'/0'/0'/0/0* (BIP44), camino de derivación que se ha a seguir. Consiste en ir obteniendo claves privadas a partir de la inmediata anterior, *Hieratical Dereministic* (HD). Todas estas son XPRIV
  - Para obtener **m**, master node, se aplica (bx hd-new) a la **Seed**
  - Para obtener **44'** se aplica (bx hd-private -i 44 -d) a **m**; El simbolo **'** aparece en otros lugares como **H** (hard) significa que la XPUB asociada no se puede utilizar para derivar direcciones de pago (Tengo que aclararlo mejor, porque creo que falta algún matiz).
  - **0'** (bx hd-private -i 0 -d)
  - **0'** (bx hd-private -i 0 -d)
  - **0** (bx hd-private -i 0); En esta clave no aparece **'**, significa que su XPUB asociada se puede utilizar para derivar direcciones de pago (pendiente matizar)
  - **0** (bx hd-private -i 0)
  - **xpub** se muestra la publica correspondiente a la última XPRV obtenida (hd-to-public)
- En este punto entra en juego la famosa Curva Eliptica, seguimos derivando en busca de la dirección de pago
  - **prv_ec**. Transforma la ultima **XPRIV** con curva eliptica (bx hd-to-ec ) 
  - **wif** Transformamos la anterior en clave wif (bx ec-to-wif )
  - **pub_ec** Obtenemos la XPUB a partir de la wif (bx wif-to-public) (Tambien se puede obtener desde la EC con ec-to-public)
  - **p2pkh** Obtenemos la address o dirección de pago a partir de la XPUB (bx ec-to-address)

Entre parétesis he puesto el comando que se utiliza en cada paso, y que se puede lanzar en línea de comandos. Si el sufrido lector quisiera probar todo el proceso, partiendo de la entropia para generar la dirección de pago puede lanzar el siguiente comando (Debe contar con el ejecutable bx). 
~~~
bx mnemonic-new 00000000000000000000000000000000| bx mnemonic-to-seed| bx hd-new | bx hd-private -i 44 -d|\
      bx hd-private -i 0 -d|bx hd-private -i 0 -d| bx hd-private -i 0 | bx hd-private -i 0|\
      bx hd-to-ec --config test.cfg|bx ec-to-public 
~~~
Si quisiera experimentar a generar alguno de los pasos intermedios, solo debe eliminar los pasos siguienes. Por ejemplo para generar la *master node* puede lanzar: 
~~~
bx mnemonic-new 00000000000000000000000000000000| bx mnemonic-to-seed| bx hd-new 
~~~


Hay más ejemplos en https://github.com/CarlosRVL/snowy-hill/blob/master/ejemplos.md#ejemplos-de-utilizaci%C3%B3n

## Ayuda 

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

## Otros usos
Cuando se quiere validar una wallet ya sea hard o soft, podemos experimentar con varias frases semilla y comparar las direcciones y la Master Fingerprint que nos devuelve la cartera. Algunas wallets utilizan una implementación propia o esquemas multifirma u otra adaptación que implica que dependes de esa implementación "desviada" del estandar para recuperar tus fondos. Si la wallet y snowy-hill generan las mismas direcciones significa que la wallet utiliza el estardar. 



