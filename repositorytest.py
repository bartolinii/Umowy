# -*- coding: utf-8 -*-

import repository
import sqlite3
import unittest

db_path = 'base.db'

class RepositoryTest(unittest.TestCase):

    def setUp(self):
        conn = sqlite3.connect(db_path)
        c = conn.cursor()
        c.execute('DELETE FROM Klient')
        c.execute('DELETE FROM Umowa')
        c.execute('''INSERT INTO Klient (id, imie, nazwisko, PESEL) VALUES(1, 'Jan', 'K', '111111111')''')
        c.execute('''INSERT INTO Umowa (ID_umowa, data_zawarcia, data_od, data_do, Cena_TV, Cena_INT, Cena_TEL, id_klient) VALUES(101, '2016-01-01', '2016-01-02','2016-12-01',152,100,1,1)''')
        c.execute('''INSERT INTO Umowa (ID_umowa, data_zawarcia, data_od, data_do, Cena_TV, Cena_INT, Cena_TEL, id_klient) VALUES(102, '2016-01-01', '2016-01-02','2016-12-01',152,100,1,1)''')
        conn.commit()
        conn.close()

    def testCheckKlient(self):
        klient = repository.KlientRepository().getById(1)
        print(klient)
        self.assertEqual(klient.imie,"Jan", "Powinno byc Jan")
        self.assertEqual(len(klient.Umowa),2,"powinno byc 2")

    def testDeleteKlient(self):
        klient = repository.Klient(id=1,imie='',nazwisko='',PESEL='')
        print(klient)
        repository.KlientRepository().delete(klient)
        conn = sqlite3.connect(db_path)
        c = conn.cursor()
        c.execute('SELECT * FROM Umowa Where id_klient=?', (1,))
        umowa = c.fetchone()
        print(umowa)
        self.assertEqual(umowa, None, "Nie powinno byc umow")
        c.execute('SELECT * FROM Klient Where id=?', (1,))
        klienci = c.fetchone()
        self.assertEqual(klienci, None, "Nie powinno byc klienta")


if __name__ == "__main__":
    unittest.main()
