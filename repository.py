# -*- coding: utf-8 -*-

import sqlite3
from datetime import datetime

#
# ĹšcieĹĽka poĹ‚Ä…czenia z bazÄ… danych
#
db_path = 'base.db'

#
# WyjÄ…tek uĹĽywany w repozytorium
#

class RepositoryException(Exception):
    def __init__(self, message, *errors):
        Exception.__init__(self, message)
        self.errors = errors

#
# Model danych
#


class Klient():


    def __init__(self, id, imie, nazwisko, PESEL, umowy=[]):
        self.id = id
        self.imie = imie
        self.nazwisko = nazwisko
        self.PESEL = PESEL
        self.umowy = umowy

    def __repr__(self):
        return "<Klient(id='%s', imie='%s', nazwisko='%s', PESEL='%s', umowy='%s')>" % (
                    self.id, self.imie, self.nazwisko, self.PESEL, str(self.umowy)
                )


class Umowa():

    def __init__(self, ID_umowa, data_zawarcia, data_od, data_do, Cena_TV, Cena_INT, Cena_TEL, id_Klient):
        self.ID_umowa = ID_umowa
        self.data_zawarcia = data_zawarcia
        self.data_od = data_od
        self.data_do = data_do
        self.Cena_TV = Cena_TV
        self.Cena_INT = Cena_INT
        self.Cena_TEL = Cena_TEL
        self.id_Klient = id_Klient

    def __repr__(self):
        return "<Umowa(ID_umowa='%s', data_zawarcia='%s', data_od='%s', data_do='%s',Cena_TV='%s', Cena_INT='%s', Cena_TEL='%s', id_Klient='%s')>" % (
                    self.ID_umowa, self.data_zawarcia, self.data_od, self.data_do, self.Cena_TV, self.Cena_INT, self.Cena_TEL, self.id_Klient
                )

class Repository():
    def __init__(self):
        try:
            self.conn = self.get_connection()
        except Exception as e:
            raise RepositoryException('GET CONNECTION:', *e.args)
        self._complete = False

    # wejĹ›cie do with ... as ...
    def __enter__(self):
        return self

    # wyjĹ›cie z with ... as ...
    def __exit__(self, type_, value, traceback):
        self.close()

    def complete(self):
        self._complete = True

    def get_connection(self):
        return sqlite3.connect(db_path)

    def close(self):
        if self.conn:
            try:
                if self._complete:
                    self.conn.commit()
                else:
                    self.conn.rollback()
            except Exception as e:
                raise RepositoryException(*e.args)
            finally:
                try:
                    self.conn.close()
                except Exception as e:
                    raise RepositoryException(*e.args)

class UmowaRepository(Repository):

    def getByKlientId(self, klientId):
        try:
            c = self.conn.cursor()
            c.execute("SELECT * FROM Umowa WHERE id_Klient=? order by data_zawarcia", (klientId,))
            umowa_items_rows = c.fetchall()
            print(umowa_items_rows)
            items_list = []
            for item_row in umowa_items_rows:
                item = Umowa(ID_umowa=item_row[0], data_zawarcia=item_row[1], data_od=item_row[2], data_do=item_row[3], Cena_TV=item_row[4], Cena_INT=item_row[5], Cena_TEL=item_row[6], id_Klient=item_row[7])
                items_list.append(item)
            return items_list
        except Exception as e:
            raise RepositoryException('Nieudane pobranie umow dla klienta: %s' %(klientId))

    def deleteByKlientId(self, klientId):
        try:
            c = self.conn.cursor()
            c.execute("DELETE FROM Umowa WHERE id_klient=?", (klientId,))
            self.conn.commit()
        except Exception as e:
            raise RepositoryException('Nieudane usuniecie umow dla klienta: %s' %(klientId))

    def update(self, umowa):
        try:
            c = self.conn.cursor()
            c.execute("UPDATE UMOWA SET data_zawarcia=?, data_od=?, data_do=?, Cena_TV=?, Cena_INT=?, Cena_TEL=?, id_Klient=? WHERE ID_umowa=?", (umowa.data_zawarcia, umowa.data_od, umowa.data_do, umowa.Cena_TV, umowa.Cena_INT, umowa.Cena_TEL, umowa.id_Klient, umowa.ID_umowa))
            self.conn.commit()
        except Exception as e:
            raise RepositoryException('Nieudany update umowy: %s' %(umowa))


    def add(self, umowa):
        try:
            c = self.conn.cursor()
            c.execute('INSERT INTO UMOWA(ID_umowa, data_zawarcia, data_od, data_do, Cena_TV, Cena_INT, Cena_TEL, id_Klient) VALUES(?, ?, ?, ?, ?, ?, ?, ?)', (umowa.ID_umowa, umowa.data_zawarcia, umowa.data_od, umowa.data_do, umowa.Cena_TV, umowa.Cena_INT, umowa.Cena_TEL, umowa.id_Klient))
            self.conn.commit()
        except Exception as e:
            raise RepositoryException('Nieudane dodanie umowy: %s' %(umowa.ID_umowa))


class KlientRepository(Repository):

    def add(self, klient):
        try:
            c = self.conn.cursor()
            c.execute('INSERT INTO Klient (id, imie, nazwisko, PESEL) VALUES(?, ?, ?, ?)',
                        (klient.id, klient.imie, klient.nazwisko, klient.PESEL)
                    )
            if klient.umowy:
                for umowa in klient.umowy:
                    try:
                        c.execute('INSERT INTO Umowa(ID_umowa, data_zawarcia, data_od, data_do, Cena_TV, Cena_INT, Cena_TEL, id_Klient) VALUES(?,?,?,?,?,?,?,?)',
                                        (umowa.ID_umowa, umowa.data_zawarcia, umowa.data_od, umowa.data_do, umowa.Cena_TV, umowa.Cena_INT, umowa.Cena_TEL, umowa.id_Klient)
                                )
                        self.conn.commit()
                    except Exception as e:
                        raise RepositoryException('nieudane dodanie umowy: %s, do klienta: %s' %
                                                    (str(umowa), str(klient.id))
                                                )
        except Exception as e:
            raise RepositoryException('Nieudane dodanie Klienta: %s' %(klient.id))

    def getById(self, id):

        try:
            c = self.conn.cursor()
            c.execute("SELECT * FROM Klient WHERE id=?", (id,))
            kli_row = c.fetchone()
            if kli_row == None:
                klient = None
                raise RepositoryException()
            else:
                klient = Klient(id=id,imie=kli_row[1],nazwisko=kli_row[2],PESEL=kli_row[3])
                print(klient)
                umowa_items_rows = UmowaRepository().getByKlientId(id)
                klient.umowy = umowa_items_rows
        except Exception as e:
            raise RepositoryException('W bazie brak Klienta: %s' %(id))
        return klient


    def delete(self, klient):
        try:
            c = self.conn.cursor()
            #UmowaRepository().deleteByKlientId(klient.id)
            c.execute('DELETE FROM Klient WHERE id=?', (klient,))
            c.execute('DELETE FROM Umowa WHERE id_Klient=?', (klient,))
        except Exception as e:
            raise RepositoryException('Blad w usuwaniu klienta %s' %str(klient))

    def update(self, klient):
        c = self.conn.cursor()
        c.execute("UPDATE KLIENT SET imie=?, nazwisko=?, PESEL=? WHERE id=?", (klient.imie, klient.nazwisko, klient.PESEL, klient.id))
        self.conn.commit()

if __name__ == '__main__':

    #Klient

    #ADD
    #with KlientRepository() as klient_repository:
        #add_klient=Klient(id=12, imie='Lucjan', nazwisko='Panek',PESEL='66041503563', umowy=[Umowa(ID_umowa=13, data_zawarcia='2015-01-01', data_od='2015-02-01', data_do='2016-02-01', Cena_TV='50', Cena_INT='60', Cena_TEL='40', id_Klient=14)])
        #klient_repository.add(add_klient)

    #getByID
    #with KlientRepository() as klient_repository:
            #klient_repository.getById(5)
            #klient_repository.complete()

    #DELETE
    #with KlientRepository() as klient_repository:
            #klient_repository.delete(1)
            #klient_repository.complete()
    #KlientRepository().delete(1)
    #KlientRepository().complete()

    # UPDATE
    #with KlientRepository() as klient_repository:
            #klient_repository.update(Klient(id = 4, imie='Lucjan', nazwisko='Panek',PESEL='66041503564', umowy=[]))
            #klient_repository.complete()

    #UMOWA

    #getByKlientId OK
    #with UmowaRepository() as umowa_repository:
            #umowa_repository.getByKlientId(10)
            #umowa_repository.complete()

    # DELETE OK
    #with UmowaRepository() as umowa_repository:
            #umowa_repository.deleteByKlientId(3)
            #umowa_repository.complete()

    # UPDATE OK
    #with UmowaRepository() as umowa_repository:
             #umowaDoUpdatu = Umowa(ID_umowa= 1, data_zawarcia="2015-01-04", data_od="2015-01-04", data_do="2016-01-04", Cena_TV="30", Cena_INT="40", Cena_TEL="50", id_Klient=3)
             #umowa_repository.update(umowaDoUpdatu)
             #umowa_repository.complete()


    # ADD OK
    #with UmowaRepository() as umowa_repository:
            # umowaADD = Umowa(ID_umowa= 9, data_zawarcia="2015-01-04", data_od="2015-01-04", data_do="2016-01-04", Cena_TV="30", Cena_INT="40", Cena_TEL="50", id_Klient=3)
            # umowa_repository.add(umowaADD)
            # umowa_repository.complete()
