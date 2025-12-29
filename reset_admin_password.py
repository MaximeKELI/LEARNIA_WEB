#!/usr/bin/env python
"""
Script pour réinitialiser le mot de passe du superuser admin
"""
import os
import sys
import django

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'learnia.settings')
django.setup()

from accounts.models import User

def reset_admin_password():
    """Réinitialise le mot de passe de l'admin"""
    print("=" * 60)
    print("RÉINITIALISATION DU MOT DE PASSE ADMIN")
    print("=" * 60)
    print()
    
    # Trouver ou créer l'utilisateur admin
    admin, created = User.objects.get_or_create(
        username='admin',
        defaults={
            'email': 'admin@learnia.tg',
            'is_superuser': True,
            'is_staff': True,
            'is_active': True
        }
    )
    
    if created:
        print("✅ Utilisateur admin créé")
    else:
        print(f"✅ Utilisateur admin trouvé: {admin.username}")
        # S'assurer que l'utilisateur est superuser et staff
        admin.is_superuser = True
        admin.is_staff = True
        admin.is_active = True
        admin.save()
    
    # Définir le nouveau mot de passe
    new_password = 'admin123'
    admin.set_password(new_password)
    admin.save()
    
    print()
    print("=" * 60)
    print("✅ MOT DE PASSE RÉINITIALISÉ AVEC SUCCÈS !")
    print("=" * 60)
    print(f"Nom d'utilisateur: {admin.username}")
    print(f"Email: {admin.email}")
    print(f"Nouveau mot de passe: {new_password}")
    print()
    print("Vous pouvez maintenant vous connecter à :")
    print("http://127.0.0.1:8000/admin/")
    print("=" * 60)
    print()
    print("⚠️  Changez ce mot de passe après la première connexion !")

if __name__ == '__main__':
    reset_admin_password()


