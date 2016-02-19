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
        c.execute('''INSERT INTO Klient (id, imie, nazwisko, PESEL) VALUES(1, 'Bartosz', 'Kuksa', '96012301341')''')
        c.execute('''INSERT INTO Umowa (ID_umowa, data_zawarcia, data_od, data_do, Cena_TV, Cena_INT, Cena_TEL, id_klient) VALUES(101, '2015-09-01', '2015-10-01','2016-10-01',30,100,20,1)''')
        c.execute('''INSERT INTO Umowa (ID_umowa, data_zawarcia, data_od, data_do, Cena_TV, Cena_INT, Cena_TEL, id_klient) VALUES(102, '2015-03-01', '2015-04-01','2016-03-31',40,50,30,1)''')
        conn.commit()
        conn.close()

    def testCheckKlientImie(self):
        klient = repository.KlientRepository().getById(1)
        self.assertEqual(klient.imie,"Bartosz", "Powinno byc Bartosz")

    def testCheckKlientUmowy(self):
        klient = repository.KlientRepository().getById(1)
        self.assertEqual(len(klient.umowy),2,"powinno byc 2")

    def testaddUmowy(self):
        with repository.UmowaRepository() as umowa_repository:
            umowaADD = repository.Umowa(ID_umowa= 9, data_zawarcia="2015-01-04", data_od="2015-01-04", data_do="2016-01-04", Cena_TV="30", Cena_INT="40", Cena_TEL="50", id_Klient=1)
            umowa_repository.add(umowaADD)
        klient = repository.KlientRepository().getById(1)
        self.assertEqual(len(klient.umowy),3,"powinno byc 3")

    #def testaddKlient(self):
        #with repository.KlientRepository() as klient_repository:
            #add_klient=repository.Klient(id=12, imie='Lucjan', nazwisko='Panek',PESEL='66041503563', umowy=[repository.Umowa(ID_umowa=13, data_zawarcia='2015-01-01', data_od='2015-02-01', data_do='2016-02-01', Cena_TV='50', Cena_INT='60', Cena_TEL='40', id_Klient=14)])
            #klient_repository.add(add_klient)


    def testUpradeKlient(self):
        conn = sqlite3.connect(db_path)
        c = conn.cursor()
        c.execute('SELECT * FROM Klient Where id=?', (1,))
        klient_przed = c.fetchone()

        with repository.KlientRepository() as klient_repository:
            klient_repository.update(repository.Klient(id = 1, imie='Lucjan', nazwisko='Panek',PESEL='66041503564', umowy=[]))
            klient_repository.complete()

        c.execute('SELECT * FROM Klient Where id=?', (1,))
        klient_po = c.fetchone()
        self.assertNotEqual(klient_przed, klient_po, "brak zmian")

    def testDeleteKlient(self):
        with repository.KlientRepository() as klient_repository:
                klient_repository.delete(1)
                klient_repository.complete()
        conn = sqlite3.connect(db_path)
        c = conn.cursor()
        c.execute('SELECT * FROM Umowa Where id_klient=?', (1,))
        umowa = c.fetchone()
        print(umowa)
        self.assertEqual(umowa, None, "Nie powinno byc umow")
        c.execute('SELECT * FROM Klient Where id=?', (1,))
        klienci = c.fetchone()
        print(klienci)
        self.assertEqual(klienci, None, "Nie powinno byc klienta")


    def testGetByIdInstance(self):
        klient = repository.KlientRepository().getById(1)
        self.assertIsInstance(klient, repository.Klient, "Objekt nie jest klasy Klient")


if __name__ == "__main__":
    unittest.main()
