
# Ejemplos de utilización

## Automatizar ejemplo (-j 1)
~~~
snowy-hill$ python3 snowy-hill.py -j 1
#=====================================
Entropia  : 11111111111111111111111111111111
mnemonico : baby mass dust captain baby mass dust captain baby mass dust casino
Seed      : 5e6463b7d2ec6a4963a389daa226675d8514630512e4ce60ee70b0ed688e35dd8a3398de05cadbc441396ddcb61e9f60ce29cb7b508af3396911df5a73d3c502
Esquema   : m/44'/0'/0'/0/0
M. FingerP: 0be174ee
-    m: xprv9s21ZrQH143K3ftbQoZd4EH3Y4FWJsss3dhWdYAzP3hs2uyhPXLrA8B46zfBv6TfCCbwzcPa5aVuxgkW7nZgdu2n6JUFntFmUDonyHh77bC
-  44': xprv9tzDBqVpBS2gePZYhA3hs9VBWwMewGaTimD1nMCwYt2DvCcSiaJAVapCmiNwWBSE3Z3YyuvUQrdMELK3J9Vg6FL71TeK7G6G6UfQ8WZbh4J
-   0': xprv9w85fhXkWsm9WpbZT1rXtUTvMz54zb9KEZVp8zcYSJaiSJsqydwqb8aU48Gc6BXWm4ko95nXB9PN4iL4MVLdA6PcBRirEZV3j5tcUeUGxkY
-   0': xprv9xudcKKPtnv1TvqyETCgbY3rPxXS8hMm53s5s6Sy5t9eri5wwRFPAu9ZQEC3sJSt3NZhn1WyYjVnFfmcXGLY7neaT7McdEAP1XQ2Dtng4ND
-    0: xprv9zzhATB6LQKhNizpiC38FXGtXz2WCPU8hGdwXTUGu5Ldtaj8YKbiJvFntL4AJgX5MQATcngtFZvi4dG55FLi7cNzweM7DkrLJbQQgGzpsgA

-    0: xprvA3ZSrqwjE2kpWmD9jvhdohZ6gs5GETCg1H9hjbH1ibRGd5UBx6rDwskj1VtVXXuy7ge9osED7kzhrEMd7UNzpXXEEXN4wXQcChWSgcN7mxQ
  xpub: xpub6GYoGMUd4QK7jFHcqxEeAqVqEtukduvXNW5JXygdGvxFVsoLVeAUVg5CrmLpXfvTa7CbD9mh3xS7WxsYmZMNwBgRCUFXaLSZKuAbxhhLTUp
prv_ec: 445d825933b9a9ef4535148c8f4582d2dbc3c24f400c8250fd61228e9629701e
   wif: KyWbzDjpokSqyVtzGTmw6Dw2FTXEy6jP7GEwXmJhXbrvKztGbcee
pub_ec: 027c2288c8d838a4770680f93e1393993a5134cc93d8acc2b3abd4d94b6864a3af
 p2pkh: 1Fq7sd3sGx8SiAXjikdntZCQ65vccYQig5
#=====================================
~~~

## Entropia 11111111111111111111111111111111 y 3 direcciones de pago
~~~
snowy-hill$ python3 snowy-hill.py -d -e "m/44'/0'/0'/0/0,2"  11111111111111111111111111111111
Cuidado: introducir un esquema manualmente o distinto a BIP44 puede dar un resultado erroneo
#=====================================
Entropia  : 11111111111111111111111111111111
mnemonico : baby mass dust captain baby mass dust captain baby mass dust casino
Seed      : 5e6463b7d2ec6a4963a389daa226675d8514630512e4ce60ee70b0ed688e35dd8a3398de05cadbc441396ddcb61e9f60ce29cb7b508af3396911df5a73d3c502
Esquema   : m/44'/0'/0'/0/0,2
M. FingerP: 0be174ee
-    m: xprv9s21ZrQH143K3ftbQoZd4EH3Y4FWJsss3dhWdYAzP3hs2uyhPXLrA8B46zfBv6TfCCbwzcPa5aVuxgkW7nZgdu2n6JUFntFmUDonyHh77bC
-  44': xprv9tzDBqVpBS2gePZYhA3hs9VBWwMewGaTimD1nMCwYt2DvCcSiaJAVapCmiNwWBSE3Z3YyuvUQrdMELK3J9Vg6FL71TeK7G6G6UfQ8WZbh4J
-   0': xprv9w85fhXkWsm9WpbZT1rXtUTvMz54zb9KEZVp8zcYSJaiSJsqydwqb8aU48Gc6BXWm4ko95nXB9PN4iL4MVLdA6PcBRirEZV3j5tcUeUGxkY
-   0': xprv9xudcKKPtnv1TvqyETCgbY3rPxXS8hMm53s5s6Sy5t9eri5wwRFPAu9ZQEC3sJSt3NZhn1WyYjVnFfmcXGLY7neaT7McdEAP1XQ2Dtng4ND
-    0: xprv9zzhATB6LQKhNizpiC38FXGtXz2WCPU8hGdwXTUGu5Ldtaj8YKbiJvFntL4AJgX5MQATcngtFZvi4dG55FLi7cNzweM7DkrLJbQQgGzpsgA

-    0: xprvA3ZSrqwjE2kpWmD9jvhdohZ6gs5GETCg1H9hjbH1ibRGd5UBx6rDwskj1VtVXXuy7ge9osED7kzhrEMd7UNzpXXEEXN4wXQcChWSgcN7mxQ
  xpub: xpub6GYoGMUd4QK7jFHcqxEeAqVqEtukduvXNW5JXygdGvxFVsoLVeAUVg5CrmLpXfvTa7CbD9mh3xS7WxsYmZMNwBgRCUFXaLSZKuAbxhhLTUp
prv_ec: 445d825933b9a9ef4535148c8f4582d2dbc3c24f400c8250fd61228e9629701e
   wif: KyWbzDjpokSqyVtzGTmw6Dw2FTXEy6jP7GEwXmJhXbrvKztGbcee
pub_ec: 027c2288c8d838a4770680f93e1393993a5134cc93d8acc2b3abd4d94b6864a3af
 p2pkh: 1Fq7sd3sGx8SiAXjikdntZCQ65vccYQig5

-    1: xprvA3ZSrqwjE2kpYPHT6oy7QeQLPx2TzXNU79WRcyWiFdymam2LCiLFiaeznfhuTGTcLprZKzRKSjYJGnKfqebBthz4XDZdmXxSB26ZYNFC2aU
  xpub: xpub6GYoGMUd4QK7ksMvCqW7mnM4wyrxPz6KUNS2RMvKoyWkTZMUkFeWGNyUdwjeqNfY6jtryKvhTXfGQ3zNP58PdLTUwp1QaXmvgyCi8Q7XbEW
prv_ec: bcf07bb00aad372c4f5aa98017cf5113e2d7cd96104dc9f3eed17bc3223b1a9f
   wif: L3Yz3eF65uhbVAGAzStxZhqTzR4PBvocZxQxjdNA9oSfHvNmn5Cw
pub_ec: 0340980d1de03cd6d45923cc072f6853ef05e91f0c3ca2e33db68b8039833cdc8d
 p2pkh: 1PdqQuKuDJhiB94ZWD74ddnt2nfbnQbN3U

-    2: xprvA3ZSrqwjE2kpdBLxV49HgNg9opfLYZwKXw4FGHcdECp7WK328gXMpJMKw5UXr5NKzrWmeRK5oBnjcgFDwiYcMYXiBU7MYt6ZktiVpKiRVHF
  xpub: xpub6GYoGMUd4QK7qfRRb5gJ3WctMrVpx2fAu9yr4g2EnYM6P7NAgDqcN6fonMpgjYN86L8ksCzG1Wry6Yc1HYseA5ppHjd7dPM7aFGeVrT5hKv
prv_ec: f40673495ed6dc706ec50086961b58b1e088fc2e0d7fcaccf022b4d717bef965
   wif: L5Q4fU5udLdb1HyYwtsmJD9AtggN72rttmYzW48tJFDCKus76Ztf
pub_ec: 03a178a05cc251f98dab77654977041143801e83e20676e520ec85b8094a299722
 p2pkh: 1LAJ4wpe2BnB1n9pgLqxV8PEg6fqSq1UnX
#=====================================
~~~

## Entropia 11111111111111111111111111111111 y 3 direcciones de pago; añadimos una contraseña. 
Vemos como al añadir una contraseña cambia el resto de la derivación. El mnemonico es el mismo porque la password se utiliza junto con aquel para generar la Seed. 

~~~
snowy-hill$ python3 snowy-hill.py -s unSecreto -d -e "m/44'/0'/0'/0/0,2"  11111111111111111111111111111111
Cuidado: introducir un esquema manualmente o distinto a BIP44 puede dar un resultado erroneo
#=====================================
Entropia  : 11111111111111111111111111111111
mnemonico : baby mass dust captain baby mass dust captain baby mass dust casino
Seed      : 100a12e429100d4350cc24a8068b88be85c17f988fd7bfc9a3bc8c728e58cb55af4b53e1c039bd856fdc51cbfd840e038361aeb40c901494049acb510d354815
Esquema   : m/44'/0'/0'/0/0,2
M. FingerP: 74ea0b38
-    m: xprv9s21ZrQH143K2tRcQNCRoXmypghTkTcEP9SJduvvmjKo8rwr6JScbxJobHiQ5EPrcGww1DVRbcERr1LZzMLb7GnJK42NQ5DkzWDBfN6CMhR
-  44': xprv9ukzFLYHZRD2E4kD6JKGdbPQ65gSj8DYrRYvTEYXkVbTczBA8YXGfh5VUdSKeAhANKhufeaeXedYnEYCBfDbWQFiGizR26d6c2uiuMkSUAE
-   0': xprv9x9TNkFVfZoKMwVoyimxZ6A77tazTRRGDBpcQ5B4gd8ERbZAMEZktDu9YaXNXVFDNtcByyKT4WUJMtMdGgqek8e3W9EDvm5b7hSc8DzZn9M
-   0': xprv9yj6Sd66EhNeSY4aHdY4NRGuvyQpqwd94ozGyk3henZevmEiECjbWfvtZYsDpqPCNPiAgzkH82pZckuzRT2KMXLdKJqgE43KEQv358nkxEz
-    0: xprvA23eNBDRByNi5snpH57R2soWaZcEQFkSRNbdUp3qGTqhvCpb3NLHZQxtVy9PexgNFHKsa34QDiA71BVVHaRCB12wFTJJqpuZ3b1XpCMhi22

-    0: xprvA497RdkjpqzMurv31hfJWfo1hhYBCvyuGSoCPrE7XPjLkRktEKeHR9KYrTABB5viTcv9JjVn45gWmRZT9JfrpAuwHi9BcDWGEZYLsxge1TP
  xpub: xpub6H8Tq9HdfDYf8LzW7jCJsojkFjNfcPhkdfioCEdj5jGKdE62mrxXxwe2hiGWxqKfcTVQRW8GEP1dSgzhehvHyvyMQKYMhD3ouLNsm2jsxLn
prv_ec: e364d88b3557015dde2d71344015525d241cd5eb7aa5b1aadae085220027c579
   wif: L4qjagAYC5dH1C1AVkVzLAbcLPueiYcgj3esn7DptJSovL63Uhga
pub_ec: 02edc82a73d64a512995c66d1056012603e0fb1ebf1f9276ef071e7c633ec11256
 p2pkh: 1DdKEjrbQqkpm6DKARqgLVfUwBMitArmad

-    1: xprvA497RdkjpqzMxx4fUkqz2A4gNEUxA3GaC63jTj1E9upnmd4ukfkFXbV2jR1WzeZja5RFUwEdphJtWN7y8x5SjUGqHf1L46bQ9nc62xa65Fz
  xpub: xpub6H8Tq9HdfDYfBS98anNzPJ1QvGKSZVzRZJyLG7QqiFMmeRQ4JD4W5PoWai63NkVvUS6BHYD9bvW47yXfijdvmUTSq6oMBDC2dtGQfBDQgiU
prv_ec: b3c52a9925fbea1a0de48535dd8b6756c49e471aff75a900e813f7703ee162a0
   wif: L3FAGazQUXjU9hLS5HiDXjGKtitpyC5erz2pZnR1VFqpJCpjRDfA
pub_ec: 03c16c7c3b7666534b82e30e33914771f39a1efbe310d9d9db7836b70b11423b4b
 p2pkh: 14zKWGpt5XY2GFJTSPjKig7PNsW7Uef9oA

-    2: xprvA497RdkjpqzMzox1i7Tw7YmXJ2Rkk2GZWjUUaCtJVQT1CGnFnqyZbNA2Yc6GcV8vLbAHLEp1kYA6dJFTYuJsmXk6n1N1DNSgyAbNDv3bC1z
  xpub: xpub6H8Tq9HdfDYfDJ2Up8zwUgiFr4GF9UzQsxQ5NbHv3jyz557QLPHp9AUWPu9iYcndWAeAaigkfP6joHEcLNMqaQyFbq1Y2Td9ovcFyZTyFM8
prv_ec: 0adfbedd401f12702c6d122d5c9927a3f845005fa8bc44084f43bbdb095e7f07
   wif: KwarAhgxpuwr4YBpxGrqwqNPWmqMRto8mUJHD2w3ykQxvQBNXiWp
pub_ec: 0316153599049de80a94fd283f661fbdbe4e712183695e3532cf3bbe87b26efb87
 p2pkh: 1L6EtPMwpbNQPDjDbvZDPENgA261RnM8pc
#=====================================

~~~

## Ejemplo en testnet (-t)
Comparando con los primeros ejemplos vemos como la Seed en testnet y mainnet es la misma. La fingerprint cambia, muy útil para no confundirnos entre los dos modos. 
~~~
snowy-hill$ python3 snowy-hill.py -t -d -e "m/44'/0'/0'/0/0"  11111111111111111111111111111111
Cuidado: introducir un esquema manualmente o distinto a BIP44 puede dar un resultado erroneo
#=====================================
Entropia  : 11111111111111111111111111111111
mnemonico : baby mass dust captain baby mass dust captain baby mass dust casino
Seed      : 5e6463b7d2ec6a4963a389daa226675d8514630512e4ce60ee70b0ed688e35dd8a3398de05cadbc441396ddcb61e9f60ce29cb7b508af3396911df5a73d3c502
Esquema   : m/44'/0'/0'/0/0
M. FingerP: 0be174ee
-    m: tprv8ZgxMBicQKsPeV885NR8Dsu2rBfiYPusPBcdVxbSs2CLpWinNtgbfsYW2ApqvTqyZe8izi1LEw5iRYJFEzudSxJNcwgZTEypPKZDQx2jQ23
-  44': tprv8bf9yAp9ahrmFCo5MiuD2o7Aq4msAncU4K88emdQ2rWhhoMXhwdv1LBegtYbWYpYQzaKz1YEaDD9hBrnRMqcuJbhY6rcmcpK1aQpaCCtPCH
-   0': tprv8do2T2r5v9bE7dq67ai3485ug7VHE7BKa7Qw1R2zvH5CDucvy1Hb6swuyJSG6Yuq8WHa9BQHLVyAXZsoUhgZy9fCi4w9tvD6eBe2vKseGZN
-   0': tprv8faaPedjJ4k64k5Vu24BmBfqi5weNDPmQbnCjWsRZre8eJq2vnb8geX1KQMhsfqCQp6Un78ji65aiXKMeUgUvqvAykZvHatRvd9SfVztpsL
-    0: tprv8hfdwnVRjg9myYEMNktdRAtsr7SiRuW92pZ4PstjP3q7gBUDXgwTpfdEoWDpK3uPiqhEctJeQvWWXUopCTgevfebUHZQt7aPDh9q7z8mTt3

-    0: tprv8kEPeBG4dJau7aSgQVZ8yMB5zzVUTyEgLq4pc1hUCZukQgDGwUByTd8Avg49XuJHV8AvoxqyH7aWK5uNEgiwdanpmAaNbt8f7oFs8HwpUHd
  xpub: tpubDGvRnbJJmgGa13UUJ9DjNkqCa21QdJRav8fbtXjmcqi9FAU3Zs1Ze7k36oRc4AshN1jVpjHZb4GAD9NAARCcpd8iG4zqFs6nurm1ijDzRvQ
prv_ec: 445d825933b9a9ef4535148c8f4582d2dbc3c24f400c8250fd61228e9629701e
   wif: cPsbT8jgEp978wNFesb4TYS5sgpedYq5BJPQeBmD2iWvak3zx9Fy
pub_ec: 027c2288c8d838a4770680f93e1393993a5134cc93d8acc2b3abd4d94b6864a3af
 p2pkh: mvM5Ag8r5yZhVH1MSKcAiUQix5XKTXPcLk
#=====================================
~~~
