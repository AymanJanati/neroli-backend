from django.db import models


class Property(models.Model):
    """
    Core property model — owned by PERSON_A.
    PERSON_B references this model via FK for leads, opportunities, interactions.
    Do not remove or rename fields without notifying PERSON_B.
    """

    class Status(models.TextChoices):
        AVAILABLE = "available", "Available"
        RESERVED = "reserved", "Reserved"
        SOLD = "sold", "Sold"

    class Type(models.TextChoices):
        APARTMENT = "apartment", "Apartment"
        VILLA = "villa", "Villa"
        HOUSE = "house", "House"
        LAND = "land", "Land"
        OFFICE = "office", "Office"
        STORE = "store", "Store"
        OTHER = "other", "Other"

    class Currency(models.TextChoices):
        MAD = "MAD", "MAD"
        EUR = "EUR", "EUR"
        USD = "USD", "USD"

    # Bilingual title
    title_fr = models.CharField(max_length=255)
    title_ar = models.CharField(max_length=255, blank=True, default="")

    # Type & status
    type = models.CharField(max_length=20, choices=Type.choices)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.AVAILABLE)

    # Pricing
    price = models.DecimalField(max_digits=14, decimal_places=2)
    currency = models.CharField(max_length=5, choices=Currency.choices, default=Currency.MAD)

    # Bilingual location
    location_fr = models.CharField(max_length=255)
    location_ar = models.CharField(max_length=255, blank=True, default="")
    address_fr = models.CharField(max_length=500, blank=True, default="")
    address_ar = models.CharField(max_length=500, blank=True, default="")

    # Dimensions (nullable — not all types have rooms)
    surface = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    rooms = models.PositiveSmallIntegerField(null=True, blank=True)
    bedrooms = models.PositiveSmallIntegerField(null=True, blank=True)
    bathrooms = models.PositiveSmallIntegerField(null=True, blank=True)

    # Bilingual description & features
    description_fr = models.TextField(blank=True, default="")
    description_ar = models.TextField(blank=True, default="")
    features_fr = models.JSONField(default=list, blank=True)  # ["Garage", "Ascenseur"]
    features_ar = models.JSONField(default=list, blank=True)  # ["مرآب", "مصعد"]

    # Visibility
    is_public = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Property"
        verbose_name_plural = "Properties"
        ordering = ["-created_at"]

    def __str__(self):
        return self.title_fr or self.title_ar


class PropertyImage(models.Model):
    """
    Images associated with a property.
    Only one image should have is_primary=True per property.
    """

    property = models.ForeignKey(
        Property,
        on_delete=models.CASCADE,
        related_name="images",
    )
    image = models.ImageField(upload_to="properties/")
    is_primary = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Property Image"
        verbose_name_plural = "Property Images"
        ordering = ["-is_primary", "created_at"]

    def __str__(self):
        return f"Image for {self.property} (primary={self.is_primary})"
