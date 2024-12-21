import happybase

connexion = happybase.Connection('0.0.0.0', port=9090)

table_evaluations = connexion.table('Ratings')
table_utilisateurs = connexion.table('Users')

somme_ages_par_livre = {}
compteur_evaluateurs_par_livre = {}

print("Début du scan des évaluations...")
for cle, donnees in table_evaluations.scan():
    isbn = donnees.get(b'cf1:ISBN', None)
    if isbn is None:
        print(f"Pas de ISBN trouvé pour la clé {cle}, on passe à la suivante.")
        continue
    
    book_rating = donnees.get(b'cf1:Book-Rating', None)
    if book_rating is None:
        print(f"Pas de Book-Rating trouvé pour la clé {cle}, on passe à la suivante.")
        continue

    isbn = isbn.decode('utf-8')
    book_rating = int(book_rating.decode('utf-8'))

    print(f"Traitement de l'ISBN {isbn} avec note {book_rating}...")

    for cle_utilisateur, donnees_utilisateur in table_utilisateurs.scan():
        user_id = donnees_utilisateur.get(b'cf1:User-ID', None)
        if user_id is None:
            print(f"Pas d'User-ID trouvé pour la clé utilisateur {cle_utilisateur}, on passe.")
            continue  # Passer si l'User-ID est manquant

        age = donnees_utilisateur.get(b'cf1:Age', None)
        if age is not None:
            age = int(age.decode('utf-8'))

            print(f"Utilisateur {user_id.decode('utf-8')} a un âge de {age}.")

            if isbn in somme_ages_par_livre:
                somme_ages_par_livre[isbn] += age
                compteur_evaluateurs_par_livre[isbn] += 1
            else:
                somme_ages_par_livre[isbn] = age
                compteur_evaluateurs_par_livre[isbn] = 1

print("Calcul de l'âge moyen...")
age_moyen_par_livre = {
    isbn: somme_ages_par_livre[isbn] / compteur_evaluateurs_par_livre[isbn]
    for isbn in somme_ages_par_livre
}

print("Résultats:")
for isbn, age_moyen in age_moyen_par_livre.items():
    print(f'ISBN: {isbn}, Âge moyen des utilisateurs: {age_moyen}')

connexion.close()
