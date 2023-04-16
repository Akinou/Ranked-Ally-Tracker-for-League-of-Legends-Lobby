import requests
import json

# Votre clé API de Riot Games
api_key = 'YOUR_API_KEY_HERE'

# Région du serveur de jeu
region = 'euw1'

# Nom d'utilisateur de l'invocateur
summoner_name = input('Entrez votre nom d\'invocateur : ')

# Récupération de l'ID de l'invocateur
response = requests.get(f'https://{region}.api.riotgames.com/lol/summoner/v4/summoners/by-name/{summoner_name}?api_key={api_key}')
if response.status_code == 200:
    summoner_id = response.json()['id']
else:
    print(f'Erreur {response.status_code}: {response.json()["status"]["message"]}')
    exit()

# Récupération des informations sur la partie en cours
response = requests.get(f'https://{region}.api.riotgames.com/lol/spectator/v4/active-games/by-summoner/{summoner_id}?api_key={api_key}')
if response.status_code == 200:
    current_game_info = response.json()
else:
    print(f'Erreur {response.status_code}: {response.json()["status"]["message"]}')
    exit()

# Affichage des noms des alliés de l'utilisateur et de leurs statistiques
my_team = [participant for participant in current_game_info['participants'] if participant['teamId'] == 100 or participant['teamId'] == 200]
if my_team:
    print('Membres de mon équipe :')
    for participant in my_team:
        summoner_name = participant['summonerName']
        summoner_id = participant['summonerId']

        # Récupération des statistiques en soloq de l'allié
        response = requests.get(f'https://{region}.api.riotgames.com/lol/league/v4/entries/by-summoner/{summoner_id}?api_key={api_key}')
        if response.status_code == 200:
            stats = response.json()
            soloq_stats = [stat for stat in stats if stat['queueType'] == 'RANKED_SOLO_5x5']
            if soloq_stats:
                rank = soloq_stats[0]['tier'] + ' ' + str(soloq_stats[0]['rank']) + ' LP'
                win_ratio = round(soloq_stats[0]['wins'] / soloq_stats[0]['losses'], 2)
                kda = f'{soloq_stats[0]["kills"]}/{soloq_stats[0]["deaths"]}/{soloq_stats[0]["assists"]}'
                print(f'{summoner_name} - Taux de victoire en soloq : {win_ratio}, KDA : {kda}, Rang : {rank}')
            else:
                print(f'{summoner_name} - Statistiques en soloq indisponibles')
        else:
            print(f'Erreur {response.status_code}: {response.json()["status"]["message"]}')
else:
    print('Aucun membre de mon équipe trouvé')
