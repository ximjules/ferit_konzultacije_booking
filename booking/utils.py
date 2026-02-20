def is_mentor(user):
    """
    Jednostavna provjera: ako je user.is_staff ili pripada grupi 'mentors'.
    Ako imaš propratni accounts app, možeš zamijeniti logiku.
    """
    if not user or not user.is_authenticated:
        return False
    if getattr(user, "is_staff", False):
        return True
    return user.groups.filter(name="mentors").exists()
