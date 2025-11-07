import requests
from player import Player
from player_reader import PlayerReader
from player_stats import PlayerStats
from rich.console import Console
from rich.table import Table
from rich.console import Console

def main():
    url = "https://studies.cs.helsinki.fi/nhlstats/2024-25/players"
    reader = PlayerReader(url)
    stats = PlayerStats(reader)
    from rich.console import Console
    console = Console()

    while True:
        nat = console.input("Nationality [bold red][USA/FIN/CAN/SWE/CZE/RUS/SLO/FRA/GBR/SVK/DEN/NED/AUT/BLR/GER/SUI/NOR/UZB/LAT/AUS][/]")
        players = stats.top_scorers_by_nationality(nat)

        table = Table(title=f"Season 2024-2025 players from {nat}")

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
