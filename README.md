**Blind SQLi**

**BSQLi**
<br>
Um simples script que faz a varredura de vulnerabilidades Blind SQL Injection.

**INSTALAÇÃO**

```git clone https://github.com/k45t0/BlindSQLi/```
<br>
```cd BlindSQLi```
<br>
```pip3 install -r requirements.txt```


**USO**
<br>
Para visualizar as opções disponíveis, execute o script com a flag -h:

**EXEMPLOS**

_Varredura de uma única URL:_<br>
```python3 bsqli.py -u "http://testphp.vulnweb.com/artists.php?artist=2" -s MySQL -L 2```

_Varredura de uma lista de URLs:_<br>
```python3 bsqli.py -l urls.txt -s Postgresql -L 1```

**SERVERS**

* MySQL
* Microsoft SQL Server
* Postgresql
* Oracle
