# Cahier de Charge — Real Estate Platform MVP

## 1. Objectif

Développer une plateforme simple permettant :

- aux acheteurs de consulter les biens disponibles et contacter rapidement le vendeur via WhatsApp
- au vendeur de gérer ses biens, ses leads et son processus de vente depuis une interface interne

Le MVP doit rester simple, rapide et adapté aux agents immobiliers indépendants, courtiers immobiliers et petits promoteurs.

---

## 2. Cible

La plateforme est destinée à :

- agents immobiliers indépendants
- courtiers immobiliers
- petits promoteurs vendant leurs propres biens

Le produit n’est pas destiné, dans cette première version, aux grandes agences immobilières avec une organisation complexe.

---

## 3. Périmètre du MVP

Le MVP est composé de deux parties :

1. Interface publique pour les acheteurs
2. Interface interne pour le vendeur

---

## 4. Interface publique — Acheteurs

### 4.1 Objectif

Permettre aux visiteurs de découvrir les biens disponibles et contacter le vendeur sans compte client.

### 4.2 Fonctionnalités attendues

#### Page d’accueil

- Présentation simple de la plateforme ou du vendeur
- Mise en avant des biens disponibles
- Boutons d’action vers :
  - la liste des biens
  - WhatsApp

#### Liste des biens

- Affichage des biens disponibles
- Cartes de biens contenant :
  - image principale
  - titre
  - localisation
  - prix
  - type de bien
  - statut si nécessaire

#### Détail d’un bien

Chaque bien doit avoir une page détail contenant :

- images du bien
- titre
- prix
- localisation
- type de bien
- surface
- nombre de pièces si applicable
- description
- informations principales

#### Contact WhatsApp

- Bouton “Contacter via WhatsApp”
- Bouton “Demander une visite”
- Redirection vers WhatsApp avec un message pré-rempli lié au bien sélectionné

---

## 5. Interface interne — Vendeur

### 5.1 Objectif

Permettre au vendeur de gérer ses biens, suivre ses prospects et organiser son processus commercial.

### 5.2 Fonctionnalités attendues

#### Authentification

- Connexion privée pour le vendeur/admin
- Aucun compte client côté public

#### Gestion des biens

Le vendeur peut :

- ajouter un bien
- modifier un bien
- supprimer ou archiver un bien
- gérer les images du bien
- modifier le statut du bien

Statuts des biens :

- disponible
- réservé
- vendu

Informations d’un bien :

- titre
- type
- prix
- localisation
- surface
- nombre de pièces si applicable
- description
- images
- statut

#### Gestion des leads

Le vendeur peut créer et gérer les leads intéressés.

Informations d’un lead :

- nom complet
- numéro de téléphone
- email optionnel
- budget optionnel
- préférences optionnelles
- source optionnelle : WhatsApp, recommandation, contact direct, etc.

Les leads sont uniquement des fiches internes. Ils ne possèdent pas de compte sur la plateforme.

#### Association lead — bien

Le vendeur peut :

- associer un lead à un ou plusieurs biens
- voir les biens qui intéressent un lead
- voir les leads intéressés par un bien

#### Pipeline de vente

Le vendeur peut suivre les opportunités commerciales dans un pipeline simple.

Étapes proposées :

- nouveau lead
- contacté
- intéressé
- visite planifiée
- négociation
- réservé
- vendu
- perdu

Fonctionnalités :

- création d’une opportunité
- association à un lead
- association à un bien principal
- déplacement entre les étapes
- marquage comme vendu ou perdu

#### Interactions et notes

Le vendeur peut enregistrer un historique simple :

- note d’appel
- note WhatsApp/message
- note de visite
- remarque générale

Chaque interaction peut être liée à un lead, une opportunité ou un bien.

#### Dashboard

Le dashboard doit afficher une vue simple sur :

- nombre de biens disponibles
- nombre de biens réservés
- nombre de biens vendus
- nombre de leads actifs
- opportunités par étape
- activités ou interactions récentes si possible

---

## 6. Langues

Le MVP doit supporter :

- français
- arabe

L’ajout de l’espagnol est prévu dans une version ultérieure.

---

## 7. Hors périmètre du MVP

Les éléments suivants ne font pas partie de cette première version :

- comptes clients
- inscription ou connexion des acheteurs
- système de réservation en ligne
- calendrier de visites
- paiement en ligne
- génération de contrats
- gestion locative
- automatisation avancée
- intelligence artificielle
- fonctionnalités multi-agences complexes
- espagnol dans le MVP

---

## 8. Résultat attendu en fin d’itération

À la fin de cette itération, la plateforme doit permettre :

### Côté acheteur

- consulter les biens disponibles
- accéder aux détails d’un bien
- contacter le vendeur via WhatsApp
- demander une visite via WhatsApp

### Côté vendeur

- se connecter à l’interface interne
- gérer les biens et leurs statuts
- gérer les leads
- associer les leads aux biens
- suivre les opportunités dans un pipeline
- ajouter des notes et interactions
- consulter un dashboard simple

Le produit final doit être utilisable, clair, rapide et adapté à un workflow simple basé sur WhatsApp et le suivi manuel des prospects.
