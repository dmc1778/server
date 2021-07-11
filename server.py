import csv
from flask import Flask, request, jsonify, redirect, render_template
from numpy import printoptions
from neo4j import GraphDatabase


with open('cred.txt') as f1:
    data = csv.reader(f1, delimiter=',')
    for row in data:
        username=row[0]
        pwd = row[1]
        uri = row[2]
print(username, pwd, uri)

q1 = '''
create (n:Employee{Name:$name, ID:$id})
'''
api=Flask(__name__)
driver = GraphDatabase.driver(uri=uri, auth=(username,pwd))
session = driver.session()
@api.route("/create/<string:name>&<int:id>", methods=["GET","POST"])
def create_node(name, id):
    map={"name":name, "id":id}
    try:
        session.run(q1, map)
        return (f"employee node is created with employee name={name} and id={id}")
    except Exception as e:
        return (str(e))
    
@api.route("/display", methods=["GET", "POST"])
def display_node():
    q1 = '''
    MATCH p=()-->() RETURN p
    '''
    results = session.run(q1)
    data = results.data()
    return(jsonify(data))

@api.route("/delete", methods=["POST"])
def delete_all():
    q1 = '''
    MATCH (n) DETACH DELETE n
    '''
    results = session.run(q1)

if __name__ == '__main__':
    api.run(port=5050)

    