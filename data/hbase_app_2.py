import happybase

connexion = happybase.Connection('0.0.0.0', port=9090)

table_evaluations = connexion.table('Ratings')

somme_notes_livres = {}
compteur_notes_livres = {}

for cle, donnees in table_evaluations.scan():
    isbn = donnees[b'cf1:ISBN'].decode('utf-8')
    note = int(donnees[b'cf1:Book-Rating'].decode('utf-8'))
    
    if isbn in somme_notes_livres:
        somme_notes_livres[isbn] += note
        compteur_notes_livres[isbn] += 1
    else:
        somme_notes_livres[isbn] = note
        compteur_notes_livres[isbn] = 1

meilleure_note_moyenne = -1
isbn_meilleur_livre = None

for isbn in somme_notes_livres:
    moyenne = somme_notes_livres[isbn] / compteur_notes_livres[isbn]
    if moyenne > meilleure_note_moyenne:
        meilleure_note_moyenne = moyenne
        isbn_meilleur_livre = isbn

print(f'ISBN avec la meilleure note moyenne: {isbn_meilleur_livre}, Note moyenne: {meilleure_note_moyenne}')

connexion.close()
