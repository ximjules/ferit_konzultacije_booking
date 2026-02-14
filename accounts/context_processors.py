def role_flags(request):
    user = request.user
    is_mentor = False
    if user.is_authenticated:
        is_mentor = user.is_superuser or user.groups.filter(name="mentor").exists()
    return {"is_mentor": is_mentor}
