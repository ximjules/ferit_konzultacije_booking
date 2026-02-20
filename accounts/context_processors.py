def role_flags(request):
    user = request.user
    is_mentor = False
    is_student = False

    if user.is_authenticated:
        is_mentor = user.is_superuser or user.groups.filter(name="mentor").exists()
        is_student = not is_mentor  # svi ostali prijavljeni korisnici tretiraju se kao studenti

    return {
        "is_mentor": is_mentor,
        "is_student": is_student,
    }
