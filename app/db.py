from tinydb import TinyDB


db = TinyDB("db.json")
graphs_table = db.table("graphs")
