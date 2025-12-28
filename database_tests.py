"""
Tests unitaires pour la base de données
Tests de contraintes, relations, intégrité référentielle
"""
from django.test import TestCase, TransactionTestCase
from django.contrib.auth import get_user_model
from django.db import IntegrityError, transaction
from accounts.models import Matiere, Chapitre, User
from qcm.models import QCM, Question, Choix
from flashcards.models import Deck, Flashcard
from tutor.models import Conversation, Message

User = get_user_model()


class DatabaseConstraintsTest(TestCase):
    """Tests pour les contraintes de base de données"""
    
    def test_matiere_code_unique(self):
        """Test que le code de matière est unique"""
        Matiere.objects.create(
            nom='Mathématiques',
            code='MATH',
            niveau='college'
        )
        # Tenter de créer une autre matière avec le même code
        with self.assertRaises(IntegrityError):
            Matiere.objects.create(
                nom='Autre Math',
                code='MATH',
                niveau='lycee'
            )
    
    def test_chapitre_unique_together(self):
        """Test la contrainte unique_together sur Chapitre"""
        matiere = Matiere.objects.create(
            nom='Mathématiques',
            code='MATH',
            niveau='college'
        )
        Chapitre.objects.create(
            matiere=matiere,
            titre='Chapitre 1',
            numero=1,
            contenu='Contenu'
        )
        # Ne peut pas créer un autre chapitre avec même matiere et numero
        with self.assertRaises(IntegrityError):
            Chapitre.objects.create(
                matiere=matiere,
                titre='Autre titre',
                numero=1,  # Même numéro
                contenu='Autre contenu'
            )
    
    def test_foreign_key_cascade_delete_matiere(self):
        """Test la suppression en cascade d'une matière"""
        matiere = Matiere.objects.create(
            nom='Mathématiques',
            code='MATH',
            niveau='college'
        )
        chapitre = Chapitre.objects.create(
            matiere=matiere,
            titre='Chapitre 1',
            numero=1,
            contenu='Contenu'
        )
        chapitre_id = chapitre.id
        # Supprimer la matière
        matiere.delete()
        # Le chapitre doit être supprimé aussi (CASCADE)
        self.assertFalse(Chapitre.objects.filter(id=chapitre_id).exists())
    
    def test_foreign_key_set_null(self):
        """Test SET_NULL sur les ForeignKey"""
        user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            email='test@example.com'
        )
        matiere = Matiere.objects.create(
            nom='Mathématiques',
            code='MATH',
            niveau='college'
        )
        chapitre = Chapitre.objects.create(
            matiere=matiere,
            titre='Chapitre 1',
            numero=1,
            contenu='Contenu'
        )
        qcm = QCM.objects.create(
            user=user,
            titre='QCM Test',
            chapitre=chapitre,
            texte_source='Texte'
        )
        chapitre_id = chapitre.id
        # Supprimer le chapitre
        chapitre.delete()
        # Le QCM doit toujours exister mais avec chapitre=None (SET_NULL)
        qcm.refresh_from_db()
        self.assertIsNone(qcm.chapitre)


class DatabaseRelationsTest(TestCase):
    """Tests pour les relations de base de données"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            email='test@example.com'
        )
        self.matiere = Matiere.objects.create(
            nom='Mathématiques',
            code='MATH',
            niveau='college'
        )
    
    def test_matiere_chapitres_relation(self):
        """Test la relation inverse Matiere -> Chapitres"""
        chapitre1 = Chapitre.objects.create(
            matiere=self.matiere,
            titre='Chapitre 1',
            numero=1,
            contenu='Contenu 1'
        )
        chapitre2 = Chapitre.objects.create(
            matiere=self.matiere,
            titre='Chapitre 2',
            numero=2,
            contenu='Contenu 2'
        )
        # Vérifier la relation inverse
        self.assertEqual(self.matiere.chapitres.count(), 2)
        self.assertIn(chapitre1, self.matiere.chapitres.all())
        self.assertIn(chapitre2, self.matiere.chapitres.all())
    
    def test_qcm_questions_relation(self):
        """Test la relation QCM -> Questions"""
        qcm = QCM.objects.create(
            user=self.user,
            titre='QCM Test',
            texte_source='Texte'
        )
        question1 = Question.objects.create(
            qcm=qcm,
            texte='Question 1',
            numero=1
        )
        question2 = Question.objects.create(
            qcm=qcm,
            texte='Question 2',
            numero=2
        )
        # Vérifier la relation
        self.assertEqual(qcm.questions.count(), 2)
        self.assertIn(question1, qcm.questions.all())
        self.assertIn(question2, qcm.questions.all())
    
    def test_question_choix_relation(self):
        """Test la relation Question -> Choix"""
        qcm = QCM.objects.create(
            user=self.user,
            titre='QCM Test',
            texte_source='Texte'
        )
        question = Question.objects.create(
            qcm=qcm,
            texte='Question ?',
            numero=1
        )
        choix1 = Choix.objects.create(
            question=question,
            texte='Choix 1',
            est_correct=True
        )
        choix2 = Choix.objects.create(
            question=question,
            texte='Choix 2',
            est_correct=False
        )
        # Vérifier la relation
        self.assertEqual(question.choix.count(), 2)
        self.assertIn(choix1, question.choix.all())
        self.assertIn(choix2, question.choix.all())
    
    def test_conversation_messages_relation(self):
        """Test la relation Conversation -> Messages"""
        conversation = Conversation.objects.create(
            user=self.user,
            titre='Conversation Test'
        )
        message1 = Message.objects.create(
            conversation=conversation,
            role='user',
            contenu='Message 1'
        )
        message2 = Message.objects.create(
            conversation=conversation,
            role='assistant',
            contenu='Message 2'
        )
        # Vérifier la relation
        self.assertEqual(conversation.messages.count(), 2)
        self.assertIn(message1, conversation.messages.all())
        self.assertIn(message2, conversation.messages.all())
    
    def test_deck_flashcards_relation(self):
        """Test la relation Deck -> Flashcards"""
        deck = Deck.objects.create(
            user=self.user,
            titre='Deck Test'
        )
        flashcard1 = Flashcard.objects.create(
            deck=deck,
            recto='Recto 1',
            verso='Verso 1'
        )
        flashcard2 = Flashcard.objects.create(
            deck=deck,
            recto='Recto 2',
            verso='Verso 2'
        )
        # Vérifier la relation
        self.assertEqual(deck.flashcards.count(), 2)
        self.assertIn(flashcard1, deck.flashcards.all())
        self.assertIn(flashcard2, deck.flashcards.all())


class DatabaseTransactionsTest(TransactionTestCase):
    """Tests pour les transactions de base de données"""
    
    def test_transaction_rollback(self):
        """Test qu'une transaction peut être annulée"""
        matiere = Matiere.objects.create(
            nom='Mathématiques',
            code='MATH',
            niveau='college'
        )
        initial_count = Matiere.objects.count()
        
        try:
            with transaction.atomic():
                Matiere.objects.create(
                    nom='Français',
                    code='FR',
                    niveau='college'
                )
                # Simuler une erreur
                raise IntegrityError("Simulation d'erreur")
        except IntegrityError:
            pass
        
        # Le nombre doit être inchangé (rollback)
        self.assertEqual(Matiere.objects.count(), initial_count)


class DatabaseIndexingTest(TestCase):
    """Tests pour les index de base de données"""
    
    def test_ordering_on_matiere(self):
        """Test l'ordonnancement par défaut sur Matiere"""
        Matiere.objects.create(nom='Français', code='FR', niveau='college')
        Matiere.objects.create(nom='Mathématiques', code='MATH', niveau='college')
        Matiere.objects.create(nom='Anglais', code='ANG', niveau='college')
        
        matieres = list(Matiere.objects.all())
        # Doit être ordonné par nom
        self.assertEqual(matieres[0].nom, 'Anglais')
        self.assertEqual(matieres[1].nom, 'Français')
        self.assertEqual(matieres[2].nom, 'Mathématiques')
    
    def test_ordering_on_chapitre(self):
        """Test l'ordonnancement sur Chapitre"""
        matiere = Matiere.objects.create(
            nom='Mathématiques',
            code='MATH',
            niveau='college'
        )
        Chapitre.objects.create(
            matiere=matiere,
            titre='Chapitre 3',
            numero=3,
            contenu='Contenu'
        )
        Chapitre.objects.create(
            matiere=matiere,
            titre='Chapitre 1',
            numero=1,
            contenu='Contenu'
        )
        Chapitre.objects.create(
            matiere=matiere,
            titre='Chapitre 2',
            numero=2,
            contenu='Contenu'
        )
        
        chapitres = list(Chapitre.objects.filter(matiere=matiere))
        # Doit être ordonné par numero
        self.assertEqual(chapitres[0].numero, 1)
        self.assertEqual(chapitres[1].numero, 2)
        self.assertEqual(chapitres[2].numero, 3)


class DatabaseDataIntegrityTest(TestCase):
    """Tests pour l'intégrité des données"""
    
    def test_user_default_niveau(self):
        """Test la valeur par défaut du niveau d'étude"""
        user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            email='test@example.com'
        )
        # Doit avoir la valeur par défaut
        self.assertEqual(user.niveau_etude, '6e')
    
    def test_matiere_default_icon(self):
        """Test l'icône par défaut d'une matière"""
        matiere = Matiere.objects.create(
            nom='Test',
            code='TEST',
            niveau='college'
        )
        self.assertEqual(matiere.icone, '📚')
    
    def test_flashcard_default_level(self):
        """Test le niveau par défaut d'une flashcard"""
        user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            email='test@example.com'
        )
        deck = Deck.objects.create(
            user=user,
            titre='Deck Test'
        )
        flashcard = Flashcard.objects.create(
            deck=deck,
            recto='Question',
            verso='Réponse'
        )
        self.assertEqual(flashcard.niveau, 0)
        self.assertEqual(flashcard.nombre_revisions, 0)
        self.assertEqual(flashcard.nombre_success, 0)

