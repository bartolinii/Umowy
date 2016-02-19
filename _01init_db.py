# -*- coding: utf-8 -*-

import sqlite3


db_path = 'base.db'
conn = sqlite3.connect(db_path)
c = conn.cursor()

c.execute('''DROP TABLE Umowa''')
c.execute('''DROP TABLE Klient''')


c.execute('''
          CREATE TABLE Klient
          ( id INTEGER PRIMARY KEY,
            imie VARCHAR(20) NOT NULL,
            nazwisko VARCHAR(20) NOT NULL,
            PESEL VARCHAR(11) NOT NULL
          )
          ''')
c.execute('''
          CREATE TABLE UMOWA
          (ID_umowa INTEGER PRIMARY KEY,
            data_zawarcia DATE NOT NULL,
            data_od DATE NOT NULL,
            data_do DATE,
            Cena_TV NUMERIC,
            Cena_INT NUMERIC,
            Cena_TEL NUMERIC,
            id_Klient INTEGER,
           FOREIGN KEY(id_Klient) REFERENCES Klient(id)
		  )
          ''')

c.execute('''INSERT INTO KLIENT VALUES (1, 'Bartosz', 'Kowalski', '74121301261')
''')
c.execute('''INSERT INTO KLIENT VALUES (2, 'Tomasz', 'Wardo', '86071801234')
''')
c.execute('''INSERT INTO KLIENT VALUES (3, 'Alicja', 'Petko', '81093002143')
''')
c.execute('''INSERT INTO KLIENT VALUES (4, 'Michal', 'Agustyn', '65033001538')
''')


c.execute('''INSERT INTO UMOWA VALUES(1,'2015-01-01','2015-02-01','2016-02-01','50','60','40', 1)
''')
c.execute('''INSERT INTO UMOWA VALUES(2,'2015-02-01','2015-04-01','2016-03-31','30','40','50', 1)
''')
c.execute('''INSERT INTO UMOWA VALUES(3,'2015-07-15','2015-08-01','2016-08-31','35','45','60', 2)
''')
c.execute('''INSERT INTO UMOWA VALUES(4,'2015-12-17','2016-01-01','2017-12-31','30','40','20', 3)
''')
c.execute('''INSERT INTO UMOWA VALUES(5,'2015-12-28','2016-02-01','2017-01-31','20','50','49', 4)
''')
conn.commit()
