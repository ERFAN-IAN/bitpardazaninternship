def user_has_permission(user, permission):
    if permission == "authenticated":
        return user.is_authenticated
    if permission == "anonymous":
        return not user.is_authenticated
    if permission == "superuser":
        return user.is_superuser
    if permission.startswith("group:"):
        group_name = permission.split(":", 1)[1]
        return user.groups.filter(name=group_name).exists()
    return False


def check_permissions(user, permissions):
    if not permissions:
        return True
    return any(user_has_permission(user, perm) for perm in permissions)
