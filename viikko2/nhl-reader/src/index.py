import requests
from player import Player
from player_reader import PlayerReader
from player_stats import PlayerStats
from rich.console import Console
from rich.table import Table
from rich.console import Console
from rich.console import Console


def main():
    console = Console()

    valid_seasons = {"2018-19", "2019-20", "2020-21", "2021-22",
                     "2022-23", "2023-24", "2024-25", "2025-26"}

    valid_nationalities = {"USA", "FIN", "CAN", "SWE", "CZE", "RUS",
                           "SLO", "FRA", "GBR", "SVK", "DEN", "NED",
                           "AUT", "BLR", "GER", "SUI", "NOR", "UZB",
                           "LAT", "AUS"}

    while True:
        season = console.input("Season [2018-19/2019-20/2020-21/2021-22/2022-23/2023-24/2024-25/2025-26, quit] ")
        if season == "quit":
            break
        elif season not in valid_seasons:
            console.print("Season not valid!")
            continue

        nat = console.input("Nationality [USA/FIN/CAN/SWE/CZE/RUS/SLO/FRA/GBR/SVK/DEN/NED/AUT/BLR/GER/SUI/NOR/UZB/LAT/AUS]")
        if nat not in valid_nationalities:
            console.print("Nationality not valid!")
            continue

        url = f"https://studies.cs.helsinki.fi/nhlstats/{season}/players"
        reader = PlayerReader(url)
        stats = PlayerStats(reader)
        players = stats.top_scorers_by_nationality(nat)

        table = Table(title=f"Season {season} players from {nat}")

        table.add_column("Name", justify="right", style="cyan", no_wrap=True)
        table.add_column("Team(s)", style="magenta")
        table.add_column("Goals", justify="right", style="green")
        table.add_column("Assists", justify="right", style="green")
        table.add_column("Points", justify="right", style="green")

        for player in players:
            table.add_row(
                player.name,
                player.team,
                str(player.goals),
                str(player.assists),
                str(player.points)
            )

        console = Console()
        console.print(table)

if __name__ == "__main__":
    main()
