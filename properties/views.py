from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .filters import PropertyFilter
from .models import Property, PropertyImage
from .serializers import (
    AdminPropertyDetailSerializer,
    AdminPropertyListSerializer,
    PropertyCreateUpdateSerializer,
    PropertyImageSerializer,
    PublicPropertyDetailSerializer,
    PublicPropertyListSerializer,
)


# ---------------------------------------------------------------------------
# Public views
# ---------------------------------------------------------------------------

class PublicPropertyListView(APIView):
    """
    GET /api/public/properties/

    Open endpoint — no authentication required.
    Returns paginated list of public, available-focused properties.
    Supports: search, city, type, min_price, max_price, status, ordering.
    """

    permission_classes = [AllowAny]

    def get(self, request):
        from rest_framework.filters import SearchFilter, OrderingFilter
        from django_filters.rest_framework import DjangoFilterBackend
        from rest_framework.pagination import PageNumberPagination

        qs = Property.objects.filter(is_public=True).prefetch_related("images")

        # Apply django-filter
        filterset = PropertyFilter(request.GET, queryset=qs)
        qs = filterset.qs

        # Apply search
        search_query = request.GET.get("search", "")
        if search_query:
            from django.db.models import Q
            qs = qs.filter(
                Q(title_fr__icontains=search_query)
                | Q(title_ar__icontains=search_query)
                | Q(location_fr__icontains=search_query)
                | Q(location_ar__icontains=search_query)
                | Q(description_fr__icontains=search_query)
                | Q(description_ar__icontains=search_query)
            )

        # Apply ordering
        ordering = request.GET.get("ordering", "-created_at")
        allowed_orderings = ["price", "-price", "created_at", "-created_at", "surface", "-surface"]
        if ordering in allowed_orderings:
            qs = qs.order_by(ordering)

        # Paginate
        paginator = PageNumberPagination()
        paginator.page_size = 20
        page = paginator.paginate_queryset(qs, request)
        serializer = PublicPropertyListSerializer(page, many=True, context={"request": request})
        return paginator.get_paginated_response(serializer.data)


class PublicPropertyDetailView(APIView):
    """
    GET /api/public/properties/{id}/

    Open endpoint — no authentication required.
    Returns full property detail with WhatsApp URLs.
    """

    permission_classes = [AllowAny]

    def get(self, request, pk):
        try:
            prop = Property.objects.prefetch_related("images").get(pk=pk, is_public=True)
        except Property.DoesNotExist:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = PublicPropertyDetailSerializer(prop, context={"request": request})
        return Response(serializer.data)


# ---------------------------------------------------------------------------
# Admin views
# ---------------------------------------------------------------------------

class AdminPropertyViewSet(viewsets.ModelViewSet):
    """
    Admin CRUD for properties — authentication required.

    GET    /api/admin/properties/         → list
    POST   /api/admin/properties/         → create
    GET    /api/admin/properties/{id}/    → detail
    PATCH  /api/admin/properties/{id}/    → partial update
    DELETE /api/admin/properties/{id}/    → delete
    POST   /api/admin/properties/{id}/images/ → upload image
    """

    permission_classes = [IsAuthenticated]
    filterset_class = PropertyFilter
    search_fields = ["title_fr", "title_ar", "location_fr", "location_ar"]
    ordering_fields = ["price", "created_at", "surface"]
    ordering = ["-created_at"]

    def get_queryset(self):
        return Property.objects.all().prefetch_related("images")

    def get_serializer_class(self):
        if self.action == "list":
            return AdminPropertyListSerializer
        if self.action in ("create", "update", "partial_update"):
            return PropertyCreateUpdateSerializer
        return AdminPropertyDetailSerializer

    def get_serializer_context(self):
        ctx = super().get_serializer_context()
        ctx["request"] = self.request
        return ctx

    def create(self, request, *args, **kwargs):
        serializer = PropertyCreateUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        prop = serializer.save()
        return Response(
            AdminPropertyDetailSerializer(prop, context={"request": request}).data,
            status=status.HTTP_201_CREATED,
        )

    def update(self, request, *args, **kwargs):
        kwargs["partial"] = True  # Always partial — PATCH only
        instance = self.get_object()
        serializer = PropertyCreateUpdateSerializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        prop = serializer.save()
        return Response(
            AdminPropertyDetailSerializer(prop, context={"request": request}).data
        )

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response({"detail": "Property deleted successfully."}, status=status.HTTP_200_OK)

    @action(
        detail=True,
        methods=["post"],
        url_path="images",
        parser_classes=[MultiPartParser, FormParser],
    )
    def upload_image(self, request, pk=None):
        """
        POST /api/admin/properties/{id}/images/

        Multipart: image (file), is_primary (bool, optional)
        """
        prop = self.get_object()
        image_file = request.FILES.get("image")
        if not image_file:
            return Response({"image": ["No image file provided."]}, status=status.HTTP_400_BAD_REQUEST)

        is_primary = request.data.get("is_primary", "false")
        is_primary = is_primary in (True, "true", "True", "1", 1)

        # If setting this as primary, demote all existing primaries
        if is_primary:
            prop.images.filter(is_primary=True).update(is_primary=False)

        img = PropertyImage.objects.create(
            property=prop,
            image=image_file,
            is_primary=is_primary,
        )
        return Response(
            PropertyImageSerializer(img, context={"request": request}).data,
            status=status.HTTP_201_CREATED,
        )


class AdminPropertyImageDeleteView(APIView):
    """
    DELETE /api/admin/property-images/{id}/
    """

    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):
        try:
            img = PropertyImage.objects.get(pk=pk)
        except PropertyImage.DoesNotExist:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)

        img.image.delete(save=False)  # Remove file from disk
        img.delete()
        return Response({"detail": "Image deleted successfully."}, status=status.HTTP_200_OK)
