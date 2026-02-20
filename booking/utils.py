from django.contrib.auth.models import Group

def is_mentor(user):
    """True ako je korisnik superuser ili pripada grupi 'mentor'."""
    if not user or not user.is_authenticated:
        return False
    return user.is_superuser or user.groups.filter(name="mentor").exists()


def is_student(user):
    """Student je svaki autentificirani korisnik koji NIJE mentor/admin."""
    if not user or not user.is_authenticated:
        return False
    return not is_mentor(user)
