from interactions.models import Interaction
from users.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models.functions import Coalesce
from users.permissions import IsCompany
from django.db.models import Count, Sum, F, Q, Value, IntegerField, CharField, ExpressionWrapper, Case, When, Exists, OuterRef
from rest_framework import status
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


class UsersScheduledMeetingView(APIView):
    """
    Devuelve los usuarios que han intentado hacer un schedule meeting,
    ordenados por puntos de interés de mayor a menor y con soporte de paginación.
    """
    permission_classes = [IsAuthenticated, IsCompany]

    def get(self, request, company_id):
        try:
            # Validar parámetros de paginación
            page = int(request.query_params.get("page", 1))
            limit = int(request.query_params.get("limit", 8))

            # Filtrar interacciones del tipo "schedule_meeting"
            interactions = Interaction.objects.filter(
                interaction_type="schedule_meeting",
                stand__company_id=company_id
            )

            # Calcular puntos de interés
            user_scores = interactions.values("visit__user_id").annotate(
                time_points=ExpressionWrapper(
                    Coalesce(
                        Sum(
                            Case(
                                When(
                                    Q(interaction_type="stand_entry"),
                                    then=F("interaction_duration")
                                )
                            )
                        ),
                        0
                    ) / 10,
                    output_field=IntegerField()
                ),
                chatbot_points=ExpressionWrapper(
                    Coalesce(
                        Count("id", filter=Q(interaction_type="talk_chatbot")) * 5,
                        0
                    ),
                    output_field=IntegerField()
                ),
                website_points=ExpressionWrapper(
                    Case(
                        When(
                            Exists(Interaction.objects.filter(
                                stand__company_id=company_id,
                                interaction_type="info_pc",
                                visit__user_id=OuterRef("visit__user_id")
                            )),
                            then=Value(15)
                        ),
                        default=Value(0),
                    ),
                    output_field=IntegerField()
                ),
                mailbox_points=ExpressionWrapper(
                    Case(
                        When(
                            Exists(Interaction.objects.filter(
                                stand__company_id=company_id,
                                interaction_type="mailbox",
                                visit__user_id=OuterRef("visit__user_id")
                            )),
                            then=Value(15)
                        ),
                        default=Value(0),
                    ),
                    output_field=IntegerField()
                ),
                video_points=ExpressionWrapper(
                    Case(
                        When(
                            Exists(Interaction.objects.filter(
                                stand__company_id=company_id,
                                interaction_type="show_video",
                                visit__user_id=OuterRef("visit__user_id")
                            )),
                            then=Value(10)
                        ),
                        default=Value(0),
                    ),
                    output_field=IntegerField()
                ),
                catalog_points=ExpressionWrapper(
                    Case(
                        When(
                            Exists(Interaction.objects.filter(
                                stand__company_id=company_id,
                                interaction_type="download_catalog",
                                visit__user_id=OuterRef("visit__user_id")
                            )),
                            then=Value(15)
                        ),
                        default=Value(0),
                    ),
                    output_field=IntegerField()
                )
            ).annotate(
                total_points=(
                    F("time_points") +
                    F("chatbot_points") +
                    F("website_points") +
                    F("mailbox_points") +
                    F("video_points") +
                    F("catalog_points")
                )
            ).order_by("-total_points")

            # Obtener IDs de los usuarios
            user_ids = [score["visit__user_id"] for score in user_scores]

            # Filtrar los usuarios relacionados
            users = User.objects.filter(id__in=user_ids).values(
                "id", "username", "email", "location", "company", "position__title", "sector__name", "profile_picture"
            )

            # Combinar información de puntos con información de usuarios
            response_data = []
            for user in users:
                score_data = next((item for item in user_scores if item["visit__user_id"] == user["id"]), {})
                response_data.append({
                    "id": user["id"],
                    "username": user["username"],
                    "email": user.get("email", "Sin email asignado"),
                    "location": user.get("location", "Sin ubicación asignada"),
                    "company": user.get("company", "Sin empresa asignada"),
                    "position": user.get("position__title", "Sin posición asignada"),
                    "sector": user.get("sector__name", "Sin sector asignado"),
                    "profile_picture": user.get("profile_picture", "/multimedia/images/default-avatar.jpg"),
                    "total_points": score_data.get("total_points", 0),
                })

            # Paginación
            paginator = Paginator(response_data, limit)
            try:
                paginated_data = paginator.page(page)
            except PageNotAnInteger:
                return Response({"error": "Número de página inválido."}, status=status.HTTP_400_BAD_REQUEST)
            except EmptyPage:
                return Response({"error": "Página fuera de rango."}, status=status.HTTP_404_NOT_FOUND)

            return Response({
                "total": paginator.count,
                "total_pages": paginator.num_pages,
                "current_page": page,
                "users": list(paginated_data)
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
