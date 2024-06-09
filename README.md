      ___ _ _         _   ___  ___  _    _ 
     | _ ) (_)_ _  __| | / __|/ _ \| |  (_)
     | _ \ | | ' \/ _` | \__ \ (_) | |__| |
     |___/_|_|_||_\__,_| |___/\__\_\____|_|
        Blind SQLi | CODER @wh0l5th3r00t | V2

**BSQLi**
Um simples script que faz a varredura de vulnerabilidades Blind SQL Injection.

**Instalação**

```git clone https://github.com/k45t0/BlindSQLi/\n```
```cd BlindSQLi\n```
```pip3 install -r requirements.txt\n```


**Uso**
Para visualizar as opções disponíveis, execute o script com a flag -h:

**Exemplos**

_Varredura de uma única URL:_
```python3 bsqli.py -u "http://testphp.vulnweb.com/artists.php?artist=2" -s MySQL -L 2```

_Varredura de uma lista de URLs:_
```python3 bsqli.py -l urls.txt -s Postgresql -L 1```
