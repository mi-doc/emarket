from rest_framework import serializers

from products.models import Product


class ProductSerializer(serializers.ModelSerializer):
    #url         = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Product
        fields = [
            'name',
            'price',
            'os'
        ]

    # def get_url(self, obj):
    #     # request
    #     request = self.context.get("request")
    #     return obj.get_api_url(request=request)

    # def validate_title(self, value):
    #     qs = BlogPost.objects.filter(title__iexact=value) # including instance
    #     if self.instance:
    #         qs = qs.exclude(pk=self.instance.pk)
    #     if qs.exists():
    #         raise serializers.ValidationError("This title has already been used")
    #     return value