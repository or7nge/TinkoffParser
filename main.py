from bs4 import BeautifulSoup
from tabulate import tabulate
from math import sqrt
import webbrowser
import requests

LIMIT = 30

table = requests.get("https://algocode.ru/standings_data/ap_2022").json()

for user in table["users"]:
    if user["name"] == "Громыко Андрей":
        my_id = str(user["id"])
        print(my_id)
        break


class Problem:
    def __init__(self, contest, title, price):
        if len(contest) <= 30:
            self.contest = contest
        else:
            self.contest = contest[:30] + "."
        if len(title) <= 40:
            self.title = title
        else:
            self.title = title[:40] + "."
        self.price = price
        self.solved = 0


problems = []
mark = 0
total_solved = 0
for contest in table["contests"]:
    i_solved = 0
    for problem in contest["problems"]:
        problems.append(
            Problem(
                contest["title"],
                problem["short"] + "." + problem["long"],
                1 / len(contest["problems"]),
            )
        )
        if contest["users"][my_id][problem["index"]]["verdict"] == "OK":
            total_solved += 1
            i_solved += 1
            continue
        for user in contest["users"].values():
            if user[problem["index"]]["verdict"] == "OK":
                problems[-1].solved += 1
    mark += i_solved / len(contest["problems"])
mark = 10 * sqrt(mark / len(table["contests"])) * 0.55 * 0.7

problems.sort(key=lambda problem: -problem.price * problem.solved)
table = []
for i in problems[:LIMIT]:
    table.append([i.contest, i.title, i.solved, round(i.price, 2)])

infile = tabulate(
    table, headers=["Контест", "Задача", "Решило", "Цена"], tablefmt="github"
)
infile += f"\n\nSOLVED: {total_solved}/{len(problems)}  -  {round(total_solved / len(problems) * 100)}% "
infile += f"\nMARK: {round(mark, 2)}"
with open("result.txt", "w", encoding="utf-8") as f:
    f.write(infile)

webbrowser.open("result.txt")
