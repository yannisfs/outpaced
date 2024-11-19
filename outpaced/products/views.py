# products/views.py

from django.views.generic import ListView, DetailView
from django.shortcuts import get_object_or_404
from .models import Product, Category
from django.db.models import Q
from reviews.forms import ReviewForm

class ProductListView(ListView):
    """
    Displays a list of available products with pagination.
    Supports optional filtering by category and searching by name or description.
    """
    model = Product
    template_name = 'products/product_list.html'  # Specify your template name
    context_object_name = 'products'
    paginate_by = 12  # Number of products per page
    ordering = ['-created']  # Order products by newest first

    def get_queryset(self):
        """
        Override the default queryset to allow filtering by category and searching.
        """
        queryset = Product.objects.filter(available=True).order_by('-created')
        category_slug = self.kwargs.get('category_slug')
        search_query = self.request.GET.get('q', '')

        if category_slug:
            # Filter products by the given category slug
            category = get_object_or_404(Category, slug=category_slug)
            queryset = queryset.filter(category=category)

        if search_query:
            # Filter products by search query in name or description
            queryset = queryset.filter(
                Q(name__icontains=search_query) |
                Q(description__icontains=search_query)
            )

        return queryset

    def get_context_data(self, **kwargs):
        """
        Add additional context to the template, such as categories and current category.
        """
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['current_category_slug'] = self.kwargs.get('category_slug', '')
        context['search_query'] = self.request.GET.get('q', '')
        return context


class ProductDetailView(DetailView):
    """
    Displays detailed information about a specific product, including its images and reviews.
    """
    model = Product
    template_name = 'products/product_detail.html'
    context_object_name = 'product'

    def get_queryset(self):
        """
        Override the default queryset to ensure only available products are displayed.
        """
        return Product.objects.filter(available=True)

    def get_context_data(self, **kwargs):
        """
        Add additional context to the template, such as related products and the review form.
        """
        context = super().get_context_data(**kwargs)
        product = self.object
        # Fetch related products from the same category, excluding the current product
        related_products = Product.objects.filter(
            category=product.category,
            available=True
        ).exclude(id=product.id)[:4]  # Limit to 4 related products
        context['related_products'] = related_products
        context['review_form'] = ReviewForm()
        return context


# Optional: Category List View if you want a separate page for categories
class CategoryListView(ListView):
    """
    Displays a list of product categories.
    """
    model = Category
    template_name = 'products/category_list.html'  # Specify your template name
    context_object_name = 'categories'
    paginate_by = 10  # Adjust as needed
    ordering = ['name']

    def get_queryset(self):
        """
        Override the default queryset to order categories by name.
        """
        return Category.objects.all().order_by('name')
