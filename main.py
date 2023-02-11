from fastapi import FastAPI, HTTPException
import pymongo
import yaml

with open('../config.yaml', 'r') as file:
    config = yaml.safe_load(file)

uri = config['uri']

client = pymongo.MongoClient(uri)
client.list_database_names()
db = client.DFA

app = FastAPI()

@app.get("/")
async def root():
    return {'message': client.list_database_names().__str__()}

@app.get("/mech/{chassis}")
async def get_a_mech(chassis: str):

    if db['battlemech'].count_documents({'chassis':chassis}) > 0:
        mechs = db['battlemech'].find({'chassis': chassis})
        return [{key:mech[key] for key in mech if key != "_id"}
                for mech in mechs]
    raise HTTPException(status_code=404, detail=f'{chassis} not found')

