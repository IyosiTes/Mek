import uuid

from .models import CommunityUser


class CommunityUserMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        community_uuid = request.headers.get(
            "X-Community-UUID"
        )

        community_user = None

        generated_uuid = None

        if community_uuid:

            try:

                community_uuid = uuid.UUID(
                    str(community_uuid)
                )

                community_user = (
                    CommunityUser.objects
                    .filter(
                        uuid=community_uuid
                    )
                    .first()
                )

                if not community_user:

                    community_user = (
                        CommunityUser.objects.create(
                            uuid=community_uuid
                        )
                    )

            except ValueError:
                pass

        if not community_user:

            community_user = (
                CommunityUser.objects.create()
            )

            generated_uuid = str(
                community_user.uuid
            )

        request.community_user = (
            community_user
        )

        response = self.get_response(
            request
        )

        if generated_uuid:

            response[
                "X-Community-UUID"
            ] = generated_uuid

        return response