from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Count, Sum, F, Q, Value, IntegerField, CharField, ExpressionWrapper, Case, When, Exists, OuterRef
from django.db.models.functions import Coalesce
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from users.permissions import IsCompany
from interactions.models import Interaction
from events.models import Stand
from users.models import User


class GetCompanyInterestedUsers(APIView):
    """
    Devuelve una lista paginada de usuarios interesados y calcula su nivel de interés.
    También proporciona las opciones de filtros disponibles.
    """
    permission_classes = [IsAuthenticated, IsCompany]

    def get(self, request, company_id):
        try:
            # Validar si el usuario pertenece a la compañía
            user = request.user
            if not user.company_relation or user.company_relation.id != company_id:
                return Response(
                    {"error": "No tienes permiso para acceder a esta información."},
                    status=403
                )

            # Obtener los stands de la compañía
            stands = Stand.objects.filter(company_id=company_id)
            if not stands.exists():
                return Response(
                    {"error": "No se encontraron stands para esta empresa."},
                    status=404
                )

            # Obtener las interacciones relacionadas con esos stands
            interactions = Interaction.objects.filter(stand__in=stands)

            # Calcular los puntos de interés por usuario
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
                                stand__in=stands,
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
                                stand__in=stands,
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
                                stand__in=stands,
                                interaction_type="show_video",
                                visit__user_id=OuterRef("visit__user_id")
                            )),
                            then=Value(10)
                        ),
                        default=Value(0),
                    ),
                    output_field=IntegerField()
                ),
                meeting_points=ExpressionWrapper(
                    Case(
                        When(
                            Exists(Interaction.objects.filter(
                                stand__in=stands,
                                interaction_type="schedule_meeting",
                                visit__user_id=OuterRef("visit__user_id")
                            )),
                            then=Value(40)
                        ),
                        default=Value(0),
                    ),
                    output_field=IntegerField()
                ),
                catalog_points=ExpressionWrapper(
                    Case(
                        When(
                            Exists(Interaction.objects.filter(
                                stand__in=stands,
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
                time_points_limited=Case(
                    When(time_points__gte=60, then=Value(60)),
                    default=F("time_points"),
                    output_field=IntegerField()
                ),
                chatbot_points_limited=Case(
                    When(chatbot_points__gte=30, then=Value(30)),
                    default=F("chatbot_points"),
                    output_field=IntegerField()
                ),
                total_points=(
                    F("time_points_limited") +
                    F("chatbot_points_limited") +
                    F("website_points") +
                    F("mailbox_points") +
                    F("video_points") +
                    F("meeting_points") +
                    F("catalog_points")
                )
            ).annotate(
                priority=Case(
                    When(
                        Q(meeting_points=40) &
                        Q(website_points=15) &
                        Q(catalog_points=15),
                        then=Value("Decidido")
                    ),
                    When(
                        Q(meeting_points=40) &
                        Q(catalog_points=15),
                        then=Value("Estratégico")
                    ),
                    When(
                        Q(website_points=15) &
                        Q(catalog_points=15),
                        then=Value("Evaluador")
                    ),
                    When(
                        Q(video_points=10) &
                        Q(chatbot_points_limited__gte=5),
                        then=Value("Explorador")
                    ),
                    When(
                        Q(video_points=10) &
                        Q(mailbox_points=15),
                        then=Value("Curioso")
                    ),
                    When(
                        Q(mailbox_points=15),
                        then=Value("Lejano")
                    ),
                    default=Value("Confundido"),
                    output_field=CharField()
                )
            )

            # Obtener todas las opciones para filtros
            all_locations = list(
                User.objects.filter(id__in=user_scores.values("visit__user_id"))
                .values_list("location", flat=True)
                .distinct()
            )
            all_priorities = list(user_scores.values_list("priority", flat=True).distinct())

            # Aplicar filtros de búsqueda, ubicación, prioridad y puntos
            search = request.query_params.get("search", "").strip().lower()
            location = request.query_params.get("location", "").strip()
            priority = request.query_params.get("priority", "").strip()
            points_min = request.query_params.get("points_min", "").strip()
            points_max = request.query_params.get("points_max", "").strip()

            if search:
                user_scores = user_scores.filter(
                    Q(visit__user__username__icontains=search) |
                    Q(visit__user__email__icontains=search)
                )

            if location:
                user_scores = user_scores.filter(visit__user__location__iexact=location)

            if priority:
                user_scores = user_scores.filter(priority__iexact=priority)

            if points_min:
                user_scores = user_scores.filter(total_points__gte=int(points_min))

            if points_max:
                user_scores = user_scores.filter(total_points__lte=int(points_max))

            # Paginación
            limit = int(request.query_params.get('limit', 10))
            offset = int(request.query_params.get('offset', 0))
            paginator = Paginator(list(user_scores), limit)
            page_number = (offset // limit) + 1

            try:
                page = paginator.page(page_number)
            except PageNotAnInteger:
                return Response({"error": "Número de página inválido."}, status=400)
            except EmptyPage:
                return Response({"error": "Página fuera de rango."}, status=404)

            # Obtener información de los usuarios
            user_ids = [item["visit__user_id"] for item in page.object_list]
            users = User.objects.filter(id__in=user_ids).values(
                "id", "username", "email", "location", "company", "position__title", "sector__name"
            )

            # Combinar información del usuario con sus niveles de interés y prioridades
            response_data = []
            for user in users:
                score_data = next((item for item in page.object_list if item["visit__user_id"] == user["id"]), {})
                response_data.append({
                    "username": user["username"],
                    "email": user["email"] or "Sin email asignado",
                    "location": user["location"] or "Sin ubicación asignada",
                    "company": user["company"] or "Sin empresa asignada",
                    "position_title": user["position__title"] or "Sin posición asignada",
                    "sector_name": user["sector__name"] or "Sin sector asignado",
                    "priority": score_data.get("priority", "Desconocido"),
                    "total_points": score_data.get("total_points", 0),
                })

            return Response({
                "total": paginator.count,
                "limit": limit,
                "offset": offset,
                "results": response_data,
                "filters": {
                    "locations": all_locations,
                    "priorities": all_priorities,
                }
            }, status=200)

        except Exception as e:
            return Response({"error": str(e)}, status=500)
