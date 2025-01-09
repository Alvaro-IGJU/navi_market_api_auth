from interactions.models import Interaction
from users.models import User
from companies.models import Chat
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models.functions import Coalesce
from users.permissions import IsCompany
from django.db.models import Count, Sum, F, Q, Value, Case, When, Exists, OuterRef, DecimalField, IntegerField, ExpressionWrapper
from django.core.paginator import Paginator
from rest_framework import status


class UsersScheduledMeetingView(APIView):
    """
    Devuelve los usuarios que intentaron agendar reuniones, considerando solo solicitudes pendientes
    para usuarios sin chats existentes o solicitudes aceptadas.
    """
    permission_classes = [IsAuthenticated, IsCompany]

    def get(self, request, company_id):
        try:
            # Parámetros de paginación
            page = int(request.query_params.get("page", 1))
            limit = int(request.query_params.get("limit", 8))

            # Filtrar interacciones tipo "schedule_meeting" pendientes
            interactions = Interaction.objects.filter(
                interaction_type="schedule_meeting",
                stand__company_id=company_id,
                status="pending"  # Solo solicitudes pendientes
            )

            # Excluir usuarios con solicitudes aceptadas
            accepted_requests = Interaction.objects.filter(
                interaction_type="schedule_meeting",
                stand__company_id=company_id,
                status="accepted",
                visit__user_id=OuterRef("visit__user_id")
            )
            interactions = interactions.annotate(
                has_accepted=Exists(accepted_requests)
            ).filter(has_accepted=False)  # Excluir si hay una solicitud aceptada

            # Calcular puntos de interés
            user_scores = interactions.values("visit__user_id").annotate(
                total_points=ExpressionWrapper(
                    Coalesce(
                        Sum(
                            Case(
                                When(
                                    interaction_type="stand_entry",
                                    then=F("interaction_duration") / Value(10)
                                )
                            )
                        ), 0,
                        output_field=DecimalField()
                    ) +
                    ExpressionWrapper(
                        Count("id", filter=Q(interaction_type="talk_chatbot")) * Value(5),
                        output_field=DecimalField()
                    ) +
                    ExpressionWrapper(
                        Case(
                            When(
                                Exists(Interaction.objects.filter(
                                    interaction_type="info_pc",
                                    visit__user_id=OuterRef("visit__user_id")
                                )),
                                then=Value(15)
                            ),
                            default=Value(0),
                        ),
                        output_field=DecimalField()
                    ) +
                    ExpressionWrapper(
                        Case(
                            When(
                                Exists(Interaction.objects.filter(
                                    interaction_type="mailbox",
                                    visit__user_id=OuterRef("visit__user_id")
                                )),
                                then=Value(15)
                            ),
                            default=Value(0),
                        ),
                        output_field=DecimalField()
                    ) +
                    ExpressionWrapper(
                        Case(
                            When(
                                Exists(Interaction.objects.filter(
                                    interaction_type="show_video",
                                    visit__user_id=OuterRef("visit__user_id")
                                )),
                                then=Value(10)
                            ),
                            default=Value(0),
                        ),
                        output_field=DecimalField()
                    ) +
                    ExpressionWrapper(
                        Case(
                            When(
                                Exists(Interaction.objects.filter(
                                    interaction_type="download_catalog",
                                    visit__user_id=OuterRef("visit__user_id")
                                )),
                                then=Value(15)
                            ),
                            default=Value(0),
                        ),
                        output_field=DecimalField()
                    ),
                    output_field=DecimalField()
                )
            ).order_by("-total_points")

            # Obtener IDs de usuarios y filtrar información
            user_ids = [score["visit__user_id"] for score in user_scores]
            users = User.objects.filter(id__in=user_ids).values(
                "id", "username", "email", "location", "company", "position__title", "profile_picture"
            )

            # Combinar puntos con información de usuario
            response_data = [
                {
                    "id": user["id"],
                    "username": user["username"],
                    "email": user.get("email", "Sin email asignado"),
                    "location": user.get("location", "Sin ubicación asignada"),
                    "company": user.get("company", "Sin empresa asignada"),
                    "position": user.get("position__title", "Sin posición asignada"),
                    "profile_picture": user.get("profile_picture", "/multimedia/images/default-avatar.jpg"),
                    "total_points": next(
                        (item["total_points"] for item in user_scores if item["visit__user_id"] == user["id"]), 0
                    )
                }
                for user in users
            ]

            # Paginación
            paginator = Paginator(response_data, limit)
            paginated_data = paginator.get_page(page)

            return Response({
                "total": paginator.count,
                "total_pages": paginator.num_pages,
                "current_page": page,
                "users": list(paginated_data)
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
