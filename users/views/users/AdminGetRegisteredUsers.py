from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from users.permissions import IsSuperUser
from users.models import User

class AdminGetRegisteredUsers(APIView):
    permission_classes = [IsSuperUser & IsAuthenticated]

    def get(self, request):
        # Filtra los usuarios por parámetros de búsqueda
        search_query = request.query_params.get('search', '')
        location_filter = request.query_params.get('location', '')
        position_filter = request.query_params.get('position', '')  # Nuevo filtro para posición
        sector_filter = request.query_params.get('sector', '')  # Nuevo filtro para sector

        users = User.objects.all()

        if search_query:
            users = users.filter(username__icontains=search_query)  # Búsqueda por nombre de usuario

        if location_filter:
            users = users.filter(location__icontains=location_filter)  # Filtra por ubicación

        if position_filter:
            users = users.filter(position__title__icontains=position_filter)  # Filtra por posición (title)

        if sector_filter:
            users = users.filter(sector__name__icontains=sector_filter)  # Filtra por sector (name)

        # Obtener limit y offset
        limit = int(request.query_params.get('limit', 10))  # Valor por defecto para limit
        offset = int(request.query_params.get('offset', 0))  # Valor por defecto para offset

        # Paginación de los resultados utilizando Paginator de Django
        paginator = Paginator(users, limit)  # Utilizamos limit como tamaño de la página
        page_number = (offset // limit) + 1  # Calculamos la página actual

        try:
            page = paginator.page(page_number)
        except PageNotAnInteger:
            return Response({"error": "Número de página inválido."}, status=400)
        except EmptyPage:
            return Response({"error": "Página fuera de rango."}, status=404)

        # Obtener los resultados paginados
        paginated_users = page.object_list

        # Serializa los datos de los usuarios incluyendo el nombre de la posición y sector
        response_data = [{
            "username": user.username,
            "email": user.email,
            "location": user.location,
            "company": user.company,
            "position_title": user.position.title if user.position else "Sin posición asignada",  # Nombre de la posición
            "sector_name": user.sector.name if user.sector else "Sin sector asignado"  # Nombre del sector
        } for user in paginated_users]

        return Response({
            "count": paginator.count,  # Total de usuarios sin paginar
            "limit": limit,
            "offset": offset,
            "results": response_data
        })
