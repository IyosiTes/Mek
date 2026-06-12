import uuid

from django.conf import settings

from .models import CommunityUser
#future we add redis caching 

class CommunityUserMiddleware:

    COOKIE_NAME = "community_uuid"

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        community_uuid = request.COOKIES.get(
            self.COOKIE_NAME
        )

        community_user = None
        set_new_cookie = False

        if community_uuid:
            try:
                uuid.UUID(community_uuid)

                community_user = (
                    CommunityUser.objects
                    .only(
                        "id",
                        "uuid",
                        "display_name",
                        "avatar",
                        "is_verified"
                    )
                    .get(uuid=community_uuid)
                )

            except (
                CommunityUser.DoesNotExist,
                ValueError
            ):
                pass

        if not community_user:

            community_user = (
                CommunityUser.objects.create()
            )

            set_new_cookie = True

        request.community_user = community_user

        response = self.get_response(request)

        if set_new_cookie:

            response.set_cookie(
                self.COOKIE_NAME,
                str(community_user.uuid),
                max_age=60 * 60 * 24 * 365 * 2,
                httponly=True,
                secure=not settings.DEBUG,
                samesite="Lax"
            )

        return response