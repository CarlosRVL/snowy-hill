# snowy-hill
Estudio de la derivación de claves con bx (Colina nevada)

Ejemplo de salida:
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


## Introducción

Esta herramienta es similar e inspirada a la de Ian Coleman. El proposito es disponer de la misma funcionalidad de la herramienta de Ian Coleman pero en modo comando que permita un modo más rápido de general resultados enfocados al estudio de la derivación. 

Se puede utilizar para generar tus propias llaves utilizando alguna fuente de entropía, pero no se garantiza la seguridad, especialmente en cuanto a privacidad.
