import csv

#Objective 1: Average Goals Per Game (1900-2000)
def calculate_avg_goals_per_game():
    #Store goals per game
    game_goals = {}
    with open('goalscorers.csv', 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            #Get year from date
            year = int(row['date'][:4])
            if 1900 <= year <= 2000:
                #Create unique key for each game, groups info
                game_key = f"{row['date']}_{row['home_team']}_{row['away_team']}"
                game_goals[game_key] = game_goals.get(game_key, 0) + 1
    #Average and output
    if game_goals:
        total_goals = sum(game_goals.values())
        total_games = len(game_goals)
        avg_goals = total_goals / total_games
        print(f"\nAverage Goals Per Game (1900-2000)")
        print(f"Total games: {total_games}")
        print(f"Total goals: {total_goals}")
        print(f"Average goals per game: {avg_goals:.2f}")
    else:
        print("No data found for the specified period.")

#Objective 2: Shootout Wins by Country (Alphabetical Order)
def count_shootout_wins():
    #Store wins by country
    country_wins = {}
    with open('shootouts.csv', 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            #Get winner country
            winner = row['winner']
            if winner:  #Skip empty winners
                country_wins[winner] = country_wins.get(winner, 0) + 1
    #Sort alphabetically and output
    if country_wins:
        #Sort normalise (Å treated as A)
        def normalise_for_sort(country_name):
            return country_name.replace('Å', 'A').replace('å', 'a')
        sorted_countries = sorted(country_wins.items(), key=lambda x: normalise_for_sort(x[0]))
        print(f"\nShootout Wins by Country (Alphabetical Order)")
        print("-" * 40)
        for country, wins in sorted_countries:
            print(f"{country}: {wins}")
    else:
        print("No shootout data found.")

#Objective 3: Create Reliable Key for Joining Data
def create_reliable_key():
    #Function to create game key from date, home_team, away_team
    def make_game_key(date, home_team, away_team):
        return f"{date}_{home_team}_{away_team}"
    #Get user input for game search
    print(f"\nReliable Key Search")
    print("-" * 40)
    date = input("Enter date (YYYY-MM-DD): ").strip()
    home_team = input("Enter home team: ").strip()
    away_team = input("Enter away team: ").strip()
    if not date or not home_team or not away_team:
        print("All fields required!")
        return
    #Create search key
    search_key = make_game_key(date, home_team, away_team)
    print(f"\nSearching for game: {search_key}")
    print("=" * 50)
    #Search goalscorers
    goals_found = []
    with open('goalscorers.csv', 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            game_key = make_game_key(row['date'], row['home_team'], row['away_team'])
            if game_key == search_key:
                goals_found.append(row)
    #Search results
    result_found = None
    with open('results.csv', 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            game_key = make_game_key(row['date'], row['home_team'], row['away_team'])
            if game_key == search_key:
                result_found = row
                break
    #Search shootouts
    shootout_found = None
    with open('shootouts.csv', 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            game_key = make_game_key(row['date'], row['home_team'], row['away_team'])
            if game_key == search_key:
                shootout_found = row
                break
    #Display results
    if result_found:
        print(f"GAME RESULT:")
        print(f"{result_found['home_team']} {result_found['home_score']} - {result_found['away_score']} {result_found['away_team']}")
        print(f"Tournament: {result_found['tournament']}")
    else:
        print("Game result not found")
    if goals_found:
        print(f"\nGOALS ({len(goals_found)} total):")
        for goal in goals_found:
            print(f"{goal['minute']}' {goal['scorer']} ({goal['team']})")
    else:
        print("\nNo goals found")
    if shootout_found:
        print(f"\nSHOOTOUT:")
        print(f"Winner: {shootout_found['winner']}")
    else:
        print("\nNo shootout found")

#Objective 4: Teams That Won Penalty Shootout After 1-1 Draw
def penalty_shootout_after_draw():
    #Function to create game key
    def make_game_key(date, home_team, away_team):
        return f"{date}_{home_team}_{away_team}"
    #Get all 1-1 draws from results
    draw_games = {}
    with open('results.csv', 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['home_score'] == '1' and row['away_score'] == '1':
                game_key = make_game_key(row['date'], row['home_team'], row['away_team'])
                draw_games[game_key] = {
                    'home_team': row['home_team'],
                    'away_team': row['away_team'],
                    'date': row['date']
                }
    #Find shootout winners from 1-1 draws
    shootout_winners = []
    with open('shootouts.csv', 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            game_key = make_game_key(row['date'], row['home_team'], row['away_team'])
            if game_key in draw_games and row['winner']:
                shootout_winners.append({
                    'winner': row['winner'],
                    'date': row['date'],
                    'home_team': row['home_team'],
                    'away_team': row['away_team']
                })
    #Display results
    if shootout_winners:
        print(f"\nTeams That Won Penalty Shootout After 1-1 Draw")
        print("-" * 50)
        for game in shootout_winners:
            print(f"{game['date']}: {game['home_team']} 1-1 {game['away_team']} = {game['winner']} won")
        print(f"\nTotal: {len(shootout_winners)} games")
    else:
        print("No penalty shootouts after 1-1 draws found")

#Objective 5: Top Goal Scorer by Tournament with Percentage
def top_scorer_by_tournament():
    #Function to create game key
    def make_game_key(date, home_team, away_team):
        return f"{date}_{home_team}_{away_team}"
    #Get tournament info from results
    game_tournaments = {}
    with open('results.csv', 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            game_key = make_game_key(row['date'], row['home_team'], row['away_team'])
            game_tournaments[game_key] = row['tournament']
    #Count goals by scorer and tournament
    tournament_goals = {}  #tournament -> {scorer: count, total: count}
    with open('goalscorers.csv', 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            game_key = make_game_key(row['date'], row['home_team'], row['away_team'])
            tournament = game_tournaments.get(game_key, 'Unknown')
            scorer = row['scorer']
            if tournament not in tournament_goals:
                tournament_goals[tournament] = {'scorers': {}, 'total': 0}
            tournament_goals[tournament]['scorers'][scorer] = tournament_goals[tournament]['scorers'].get(scorer, 0) + 1
            tournament_goals[tournament]['total'] += 1
    #Get user input for tournament
    print(f"\nTop Goal Scorer by Tournament")
    print("-" * 40)
    tournament = input("Enter tournament name (or press Enter for all): ").strip()
    if tournament:
        #Show specific tournament
        if tournament in tournament_goals:
            data = tournament_goals[tournament]
            top_scorer = max(data['scorers'].items(), key=lambda x: x[1])
            percentage = (top_scorer[1] / data['total']) * 100
            print(f"\nTournament: {tournament}")
            print(f"Top scorer: {top_scorer[0]}")
            print(f"Goals: {top_scorer[1]} out of {data['total']} total")
            print(f"Percentage: {percentage:.1f}%")
        else:
            print("Tournament not found")
    else:
        #Show top 10 tournaments by total goals
        sorted_tournaments = sorted(tournament_goals.items(), key=lambda x: x[1]['total'], reverse=True)[:10]
        print(f"\nTop 10 Tournaments by Goals (with top scorers)")
        print("-" * 60)
        for tournament, data in sorted_tournaments:
            top_scorer = max(data['scorers'].items(), key=lambda x: x[1])
            percentage = (top_scorer[1] / data['total']) * 100
            print(f"{tournament}: {top_scorer[0]} ({top_scorer[1]}/{data['total']} goals, {percentage:.1f}%)")

#Menu
def main_menu():
    while True:
        print("\n" + "="*50)
        print("Menu")
        print("="*50)
        print("1. Average Goals Per Game (1900-2000)")
        print("2. Shootout Wins by Country")
        print("3. Game Search (Reliable Key)")
        print("4. Penalty Shootouts After 1-1 Draw")
        print("5. Top Goal Scorer by Tournament")
        print("6. Exit")
        print("-"*50)
        choice = input("Select option (1-6): ").strip()
        if choice == '1':
            calculate_avg_goals_per_game()
        elif choice == '2':
            count_shootout_wins()
        elif choice == '3':
            create_reliable_key()
        elif choice == '4':
            penalty_shootout_after_draw()
        elif choice == '5':
            top_scorer_by_tournament()
        elif choice == '6':
            print("Closed")
            break
        else:
            print("Invalid choice. Please select 1-6.")

#Run program
if __name__ == "__main__":
    main_menu()