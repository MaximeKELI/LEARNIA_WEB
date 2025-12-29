#!/usr/bin/env python
"""
Script pour créer un superutilisateur Django
Usage: python create_superuser.py [username] [email] [password]
      ou python create_superuser.py (mode interactif)
"""
import os
import sys
import django

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'learnia.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

def create_superuser(username=None, email=None, password=None):
    """Crée un superutilisateur"""
    print("=" * 60)
    print("CRÉATION D'UN SUPERUTILISATEUR - LEARNIA")
    print("=" * 60)
    print()
    
    # Mode interactif si aucun argument
    if not username:
        # Vérifier si un superuser existe déjà
        if User.objects.filter(is_superuser=True).exists():
            print("⚠️  Un superutilisateur existe déjà.")
            response = input("Voulez-vous en créer un autre ? (o/n): ")
            if response.lower() != 'o':
                print("Annulé.")
                return
        
        username = input("Nom d'utilisateur: ").strip()
        if not username:
            print("❌ Le nom d'utilisateur ne peut pas être vide.")
            return
        
        email = input("Email (optionnel): ").strip()
        password = input("Mot de passe: ").strip()
        if not password:
            print("❌ Le mot de passe ne peut pas être vide.")
            return
        
        password_confirm = input("Confirmer le mot de passe: ").strip()
        if password != password_confirm:
            print("❌ Les mots de passe ne correspondent pas.")
            return
    else:
        # Mode non-interactif
        if not password:
            print("❌ Le mot de passe est requis en mode non-interactif.")
            print("Usage: python create_superuser.py [username] [email] [password]")
            return
    
    # Vérifier si l'utilisateur existe déjà
    if User.objects.filter(username=username).exists():
        print(f"❌ L'utilisateur '{username}' existe déjà.")
        return
    
    # Créer le superuser
    try:
        user = User.objects.create_superuser(
            username=username,
            email=email if email else '',
            password=password
        )
        print()
        print("=" * 60)
        print("✅ SUPERUTILISATEUR CRÉÉ AVEC SUCCÈS !")
        print("=" * 60)
        print(f"Nom d'utilisateur: {user.username}")
        print(f"Email: {user.email or '(non renseigné)'}")
        print(f"Superuser: {user.is_superuser}")
        print(f"Staff: {user.is_staff}")
        print()
        print("Vous pouvez maintenant vous connecter à l'admin :")
        print("http://127.0.0.1:8000/admin/")
        print("=" * 60)
    except Exception as e:
        print(f"❌ Erreur lors de la création: {str(e)}")
        return

if __name__ == '__main__':
    if len(sys.argv) >= 2:
        # Mode non-interactif avec arguments
        username = sys.argv[1]
        email = sys.argv[2] if len(sys.argv) > 2 else None
        password = sys.argv[3] if len(sys.argv) > 3 else None
        create_superuser(username, email, password)
    else:
        # Mode interactif
        create_superuser()
