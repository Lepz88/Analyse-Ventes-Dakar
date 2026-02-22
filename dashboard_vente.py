import pandas as pd
import os
import matplotlib.pyplot as plt

# ==========================================
# 1. LE BACK-OFFICE : IMPORT ET NETTOYAGE
# ==========================================
dossier_projet = os.path.dirname(os.path.abspath(__file__))
chemin_fichier = os.path.join(dossier_projet, 'data', 'ventes_dakar_brutes.csv')

try:
    df = pd.read_csv(chemin_fichier, encoding='latin-1')
except FileNotFoundError:
    print("❌ Erreur : Fichier introuvable.")
    exit()

# Nettoyage
df = df.drop_duplicates()
df['Produit'] = df['Produit'].str.strip().str.lower()
df = df[df['Prix_Unitaire'] > 0]
df = df.dropna(subset=['Prix_Unitaire'])
df['Categorie'] = df['Categorie'].fillna('Inconnu')

# ==========================================
# 2. LA MÉCANIQUE : CALCULS BUSINESS
# ==========================================
df['Total_Vente'] = df['Prix_Unitaire'] * df['Quantite']

# KPI 1 : Classement des produits
top_produit = df.groupby('Produit')['Total_Vente'].sum().sort_values(ascending=False)
produits = top_produit.index
chiffre_affaires = top_produit.values

# KPI 2 : Modes de paiement
stats_paiement = df['Mode_Paiement'].value_counts()

# KPI 3 : Évolution temporelle (Génération de dates factices pour l'exemple)
df['Date'] = pd.date_range(start='2026-02-01', periods=len(df), freq='D')
df = df.sort_values('Date')

# ==========================================
# 3. LE FRONT-OFFICE : DASHBOARD DE DIRECTION
# ==========================================
print("\n--- 📊 GÉNÉRATION DU DASHBOARD ---")

# Création du meuble à 4 casiers (2 lignes, 2 colonnes)
fig, axes = plt.subplots(nrows=2, ncols=2, figsize=(15, 10))

# --- CASIER [0, 0] : Barres (Produits) ---
axes[0, 0].bar(produits, chiffre_affaires, color='#4682B4', edgecolor='white')
axes[0, 0].set_title("Performance par Produit", fontweight='bold')
axes[0, 0].set_ylabel("Chiffre d'Affaires (FCFA)")
axes[0, 0].tick_params(axis='x', rotation=45) # On penche le texte pour la lisibilité

# --- CASIER [0, 1] : Camembert (Paiements) ---
axes[0, 1].pie(stats_paiement.values, labels=stats_paiement.index, autopct='%1.1f%%', startangle=140, colors=['#FF5733', '#33FF57', '#3357FF'])
axes[0, 1].set_title("Répartition des Paiements", fontweight='bold')

# --- CASIER [1, 0] : Courbe (Évolution Temporelle) ---
axes[1, 0].plot(df['Date'], df['Total_Vente'], color='#E74C3C', marker='o', linewidth=2)
axes[1, 0].set_title("Évolution Quotidienne (Février 2026)", fontweight='bold')
axes[1, 0].set_ylabel("Ventes (FCFA)")
axes[1, 0].tick_params(axis='x', rotation=45)

# --- CASIER [1, 1] : Case vide (On éteint la lumière) ---
axes[1, 1].axis('off')

# --- FINITIONS ET SAUVEGARDE ---
fig.suptitle("TABLEAU DE BORD : ANALYSE DES VENTES - DAKAR", fontsize=22, fontweight='bold', color='#2C3E50')
plt.tight_layout() # Évite que les graphiques se rentrent dedans
plt.savefig('dashboard_complet_dakar.png', dpi=300)

print("✅ Dashboard généré et sauvegardé : 'dashboard_complet_dakar.png'")
plt.show() # Le SEUL plt.show() de tout le script !