import os, re, pathlib

files = [f for f in os.listdir(os.getcwd()) if not f.split('.')[-1] == 'py']

comp = {}

# parse objects
for f in files:
    comp[f] = {}
    databases = comp[f]

    lines = open(f, 'r').readlines()
    for line in lines:
        db = re.match("^Database: (.*)", line.strip()) 
        if db:
            dbname = db.groups()[0]
            databases[dbname] = {}
            database = databases[dbname]
        else:
            coll = re.match("^db.getCollection\('(.*)'\)\..*", line.strip())
            if coll:
                coll_name = coll.groups()[0]
                database[coll_name] = []
                collection = database[coll_name]
            else:
                rec = re.match("({.*})", line.strip())
                if rec:
                    record = rec.groups()[0]
                    collection.append(record)

# persist
d_dir = os.getcwd() + '/data'
pathlib.Path(d_dir).mkdir(parents=True, exist_ok=True)
os.chdir(d_dir)
home = os.getcwd()

for file,v in comp.items():
    os.chdir(home)
    f_dir = file + ' data'
    pathlib.Path(f_dir).mkdir(parents=True, exist_ok=True)
    os.chdir(f_dir)
    file_dir = os.getcwd()
    for db,colls in v.items():
        os.chdir(file_dir)
        pathlib.Path(db).mkdir(parents=True, exist_ok=True)
        os.chdir(db)
        for name,vals in colls.items():
            with open(name, 'w') as o:
                for rec in vals:
                    o.write(rec)