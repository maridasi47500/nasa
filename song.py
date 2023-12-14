# coding=utf-8
import sqlite3
import sys
import re
from model import Model
from lyric import Lyric
from artist import Artist
class Song(Model):
    def __init__(self):
        self.dbLyric=Lyric()
        self.dbArtist=Artist()
        self.con=sqlite3.connect(self.mydb)
        self.con.row_factory = sqlite3.Row
        self.cur=self.con.cursor()
        self.cur.execute("""create table if not exists song(
        id integer primary key autoincrement,
        artist_id text,
            title text,
            file text
                    );""")
        self.con.commit()
        #self.con.close()
    def getall(self):
        self.cur.execute("select * from song")

        row=self.cur.fetchall()
        return row
    def deletebyid(self,myid):

        self.cur.execute("delete from song where id = ?",(myid,))
        job=self.cur.fetchall()
        self.con.commit()
        return None
    def getbyid(self,myid):
        self.cur.execute("select * from song where id = ?",(myid,))
        row=dict(self.cur.fetchone())
        print(row["id"], "row id")
        job=self.cur.fetchall()
        return row
    def create(self,params):
        print("ok")
        myhash={}
        for x in params:
            if 'confirmation' in x:
                continue
            if 'lyric' in x:
                continue
            if 'artist' in x:
                continue
            if 'envoyer' in x:
                continue
            if '[' not in x and x not in ['routeparams']:
                #print("my params",x,params[x])
                try:
                  myhash[x]=str(params[x].decode())
                except:
                  myhash[x]=str(params[x])
        print("M Y H A S H")
        print(myhash,myhash.keys())
        myid=None
        try:
          artistid=self.dbArtist.findorcreate(params["artist"])
          self.cur.execute("insert into song (artist_id,title,file) values (:artist_id,:title,:file)",myhash)
          self.con.commit()
          myid=str(self.cur.lastrowid)
          for ligne in Fichier("./uploads",params["file"]).ligneparligne():
            print(ligne)
            self.dbLyric.create({"song_id":myid,"text":ligne})


        except Exception as e:
          print("my error"+str(e))
        azerty={}
        azerty["song_id"]=myid
        azerty["notice"]="votre song a été ajouté"
        return azerty




