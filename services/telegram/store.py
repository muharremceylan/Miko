import json
import sqlite3
import time
import uuid
from pathlib import Path

SUBJECTS={'turkce':'Türkçe','tarih':'Tarih','vatandaslik':'Vatandaşlık','cografya':'Coğrafya','matematik':'Matematik','belirsiz':'Belirsiz'}
class Store:
    def __init__(self,path):
        Path(path).parent.mkdir(parents=True,exist_ok=True,mode=0o700)
        self.db=sqlite3.connect(path);self.db.row_factory=sqlite3.Row
        self.db.execute('PRAGMA journal_mode=WAL')
        self.db.executescript('''CREATE TABLE IF NOT EXISTS owner(slot INTEGER PRIMARY KEY CHECK(slot=1),user_id INTEGER NOT NULL,subject TEXT NOT NULL);
        CREATE TABLE IF NOT EXISTS jobs(id TEXT PRIMARY KEY,user_id INTEGER NOT NULL,message_id INTEGER NOT NULL,state TEXT NOT NULL,subject TEXT NOT NULL,created REAL NOT NULL,updated REAL NOT NULL,source_sha TEXT,error TEXT,result TEXT,UNIQUE(user_id,message_id));''');self.db.commit()
    def owner(self):
        row=self.db.execute('SELECT user_id FROM owner WHERE slot=1').fetchone();return row[0] if row else None
    def claim(self,user_id):
        with self.db:self.db.execute('INSERT OR IGNORE INTO owner VALUES(1,?,?)',(user_id,'belirsiz'))
        return self.owner()==user_id
    def subject(self,user_id,value=None):
        if self.owner()!=user_id:return None
        if value is not None:
            if value not in SUBJECTS:raise ValueError('invalid-subject')
            with self.db:self.db.execute('UPDATE owner SET subject=? WHERE slot=1',(value,))
        return self.db.execute('SELECT subject FROM owner WHERE slot=1').fetchone()[0]
    def create(self,user_id,message_id):
        if self.owner()!=user_id:raise PermissionError()
        existing=self.db.execute('SELECT * FROM jobs WHERE user_id=? AND message_id=?',(user_id,message_id)).fetchone()
        if existing:return dict(existing),False
        now=time.time();id=uuid.uuid4().hex[:12]
        with self.db:self.db.execute('INSERT INTO jobs VALUES(?,?,?,?,?,?,?,?,?,?)',(id,user_id,message_id,'queued',self.subject(user_id),now,now,None,None,None))
        return self.get(user_id,id),True
    def get(self,user_id,id):
        row=self.db.execute('SELECT * FROM jobs WHERE id=? AND user_id=?',(id,user_id)).fetchone();return dict(row) if row else None
    def update(self,id,state,**values):
        if set(values)-{'source_sha','error','result'}:raise ValueError('invalid-field')
        values={**values,'state':state,'updated':time.time()}
        with self.db:self.db.execute('UPDATE jobs SET '+','.join(k+'=?' for k in values)+' WHERE id=?',(*values.values(),id))
    def recent(self,user_id):return [dict(r) for r in self.db.execute('SELECT * FROM jobs WHERE user_id=? ORDER BY created DESC LIMIT 5',(user_id,))]
    def pending(self):return [dict(r) for r in self.db.execute("SELECT * FROM jobs WHERE state IN ('queued','downloading','processing') ORDER BY created")]
    def expiring(self,days):return [dict(r) for r in self.db.execute("SELECT * FROM jobs WHERE updated<? AND state NOT IN ('queued','downloading','processing','deleted','expired')",(time.time()-days*86400,))]
    def forget(self,id,state='deleted'):
        with self.db:self.db.execute('UPDATE jobs SET state=?,source_sha=NULL,result=NULL,error=NULL,updated=? WHERE id=?',(state,time.time(),id))
