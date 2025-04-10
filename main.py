# № 1
from sys import stdin

res = {}
for i in stdin.readlines():
    num = int(i[:-1])
    count = 0
    for j in range(2, num):
        if num % j == 0 and j % 2 == 1:
            count += 1
    res[count] = res.get(count, []) + [num]
for i in res:
    res[i].sort()
print(res)



# № 2
import csv
import json

genes = {}
with open('skills.csv', encoding="utf8") as f:
    reader = csv.reader(f, delimiter="-", quotechar='"')
    for i in list(reader)[1:]:
        if i[1] not in genes:
            genes[i[1]] = [[], [], []]
        genes[i[1]][0].append(i[2])
        genes[i[1]][1].append(int(i[3]))
        genes[i[1]][2].append(int(i[4]))
for i in genes:
    genes[i][0].sort()
    genes[i][1] = sum(genes[i][1]) // len(genes[i][1])
    genes[i][2] = max(genes[i][2])

with open('education.jsonl', 'w', encoding="utf-8") as f:
    for gene in genes:
        to_add = {'name': gene, 'skills': genes[gene][0], 'ave_level': genes[gene][1], 'max_age': genes[gene][2]}
        f.write(json.dumps(to_add) + '\n')



# № 3
import requests


def main():
    host = input()
    vessel = input()
    minn = int(input())

    url = f"http://{host}:8080"

    response = requests.get(url)
    response_data = response.json()
    genies = []
    for genie in response_data:
        if genie["vessel"] == vessel and genie["duration"] >= minn * 100:
            genies.append(genie)

    genies.sort(key=lambda x: x["genie"], reverse=True)
    res = {}
    for genie in genies:
        res[genie["genie"]] = res.get(genie["genie"], []) + [genie["afraid"]]
    for genie in res:
        res[genie].sort()
        print(f"{genie}: {' .. '.join(res[genie])}")


if __name__ == "__main__":
    main()



# № 4
import sqlite3


def main():
    name = input()
    dbfile = input()

    con = sqlite3.connect(dbfile)
    cursor = con.cursor()

    cursor.execute("""SELECT rank, state_id FROM Genies WHERE genie = ?""", (name,))

    info = cursor.fetchone()
    genie_rank, genie_state_id = info

    cursor.execute(
        """SELECT Meetings.creature_id, Creatures.creature, Meetings.state_id, Creatures.rank, Creatures.state_id
        FROM Meetings JOIN Creatures ON Meetings.creature_id = Creatures.id
        WHERE Meetings.creature_id IN (SELECT id FROM Creatures WHERE state_id = ?)
        AND Meetings.state_id != ?
        AND Creatures.rank < ?""", (genie_state_id, genie_state_id, genie_rank))
    creatures = sorted(set(creature[1] for creature in cursor.fetchall()), key=lambda x: (-len(x), x))
    for creature in creatures:
        print(creature)


if __name__ == "__main__":
    main()



# № 5
from flask import Flask
import sqlite3
import csv

app = Flask(__name__)


@app.route('/vindict/<name>/')
def main(name):
    with open('you_know.csv', encoding='utf-8') as f:
        con = sqlite3.connect('info.db')
        cursor = con.cursor()
        reader = csv.reader(f, delimiter=";", quotechar='"')
        mags = list(reader)[1:]
        for mag in mags:
            if mag[1] == name:
                level = mag[3]
                break
        params = cursor.execute("""
            SELECT id, power 
            FROM Education 
            WHERE power > (SELECT power FROM Education WHERE id = ?)
        """, (level, )).fetchall()
        mags = list(filter(lambda x: int(x[3]) in [p[0] for p in params], mags))
        power_dict = {p[0]: p[1] for p in params}
        mags.sort(key=lambda x: (-int(x[4]), -power_dict.get(int(x[3]), float('-inf')), x[1]))
        return [mag[1] for mag in mags]


if __name__ == "__main__":
    app.run(host='127.0.0.1', port=8080)
