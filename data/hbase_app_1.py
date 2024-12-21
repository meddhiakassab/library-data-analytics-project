import happybase

connexion = happybase.Connection('0.0.0.0', port=9090)

table_evaluations = connexion.table('Ratings')

compteur_evaluations_livres = {}

for cle, donnees in table_evaluations.scan():
    isbn = donnees[b'cf1:ISBN'].decode('utf-8')
    if isbn in compteur_evaluations_livres:
        compteur_evaluations_livres[isbn] += 1
    else:
        compteur_evaluations_livres[isbn] = 1

for isbn, compteur in compteur_evaluations_livres.items():
    print(f'ISBN: {isbn}, Nombre d\'évaluations: {compteur}')

connexion.close()
