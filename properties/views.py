from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Property, User, Like, Collection, Review, UserProfile, AgencyProfile
from .forms import PropertyForm, ReviewForm, UserProfileForm, AgencyProfileForm
from django.conf import settings


from django.db.models import Avg

def home(request):
    query = request.GET.get('q', '').strip()
    search_by = request.GET.get('search_by', 'postcode')
    filter_by = request.GET.get('filter_by', '')

    properties = Property.objects.all()

    # Search logic
    if query:
        if search_by == 'postcode':
            properties = properties.filter(zip_code__icontains=query)
        elif search_by == 'address':
            properties = properties.filter(address__icontains=query)
        elif search_by == 'agency':
            properties = properties.filter(user__username__icontains=query)
        elif search_by == 'area':
            properties = properties.filter(area__icontains=query)

    # Rating annotation for rating filter
    properties = properties.annotate(avg_review_rating=Avg('reviews__rating'))

    # Filter logic
    if filter_by == 'price_low':
        properties = properties.order_by('price')
    elif filter_by == 'price_high':
        properties = properties.order_by('-price')
    elif filter_by == 'rating_high':
        properties = properties.order_by('-avg_review_rating', '-created_at')
    else:
        properties = properties.order_by('-created_at')

    return render(request, "home.html", {
        "properties": properties,
        "query": query,
        "search_by": search_by,
        "filter_by": filter_by,
    })


@login_required
def property_detail(request, pk):
    property_obj = get_object_or_404(Property, pk=pk)

    is_liked = Like.objects.filter(user=request.user, property=property_obj).exists()
    is_collected = Collection.objects.filter(user=request.user, property=property_obj).exists()

    existing_review = Review.objects.filter(
        user=request.user,
        property=property_obj
    ).first()

    reviews = Review.objects.filter(
        property=property_obj
    ).select_related('user')

    if request.method == "POST":
        if existing_review:
            form = ReviewForm(request.POST, instance=existing_review)
        else:
            form = ReviewForm(request.POST)

        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.property = property_obj
            review.save()
            messages.success(request, "Your review has been saved.")
            return redirect('property_detail', pk=pk)
    else:
        form = ReviewForm(instance=existing_review)

    review_count = reviews.count()
    avg_rating = 0
    if review_count > 0:
        avg_rating = round(sum(review.rating for review in reviews) / review_count, 1)

    return render(request, "properties/property_detail.html", {
        "property": property_obj,
        "is_liked": is_liked,
        "is_collected": is_collected,
        "like_count": property_obj.likes.count(),
        "form": form,
        "reviews": reviews,
        "review_count": review_count,
        "avg_rating": avg_rating,
        "existing_review": existing_review,
        "google_maps_key": settings.GOOGLE_MAPS_API_KEY,
    })


@login_required
def post_property(request):
    if request.user.role != 'agency' and not request.user.is_superuser:
        messages.error(request, "Only Agency accounts can post properties.")
        return redirect('home')

    if request.method == "POST":
        form = PropertyForm(request.POST, request.FILES)
        if form.is_valid():
            new_prop = form.save(commit=False)
            new_prop.user = request.user
            new_prop.save()
            messages.success(request, "Property posted successfully!")
            return redirect('home')
    else:
        form = PropertyForm()

    return render(request, "properties/property_form.html", {"form": form})


@login_required
def toggle_like(request, pk):
    property_obj = get_object_or_404(Property, pk=pk)
    like_qs = Like.objects.filter(user=request.user, property=property_obj)

    if like_qs.exists():
        like_qs.delete()
    else:
        Like.objects.create(user=request.user, property=property_obj)

    return redirect('property_detail', pk=pk)


@login_required
def toggle_collection(request, pk):
    property_obj = get_object_or_404(Property, pk=pk)
    collection_qs = Collection.objects.filter(user=request.user, property=property_obj)

    if collection_qs.exists():
        collection_qs.delete()
        messages.info(request, "Removed from collections.")
    else:
        Collection.objects.create(user=request.user, property=property_obj)
        messages.success(request, "Added to collections!")

    return redirect('property_detail', pk=pk)


@login_required
def my_likes(request):
    liked_properties = Property.objects.filter(
        likes__user=request.user
    ).order_by("-created_at")
    return render(request, "collections/my_likes.html", {"properties": liked_properties})


@login_required
def my_collection(request):
    collected_properties = Property.objects.filter(
        collected_by__user=request.user
    ).order_by("-created_at")
    return render(request, "collections/my_collection.html", {"properties": collected_properties})


def register(request):
    role_param = request.GET.get('role', 'user')

    if request.method == "POST":
        username = request.POST.get('username').strip()
        email = request.POST.get('email').strip()
        pass1 = request.POST.get('password1')
        pass2 = request.POST.get('password2')
        is_agency = request.POST.get('is_agency')

        final_username = username
        final_role = 'user'

        if is_agency == 'on':
            if not username.endswith('-agency'):
                final_username = f"{username}-agency"
            final_role = 'agency'

        if pass1 != pass2:
            messages.error(request, "The two passwords do not match!")
            return render(request, "register.html", {
                "typed_username": username,
                "typed_email": email,
                "role": role_param
            })

        if User.objects.filter(username=final_username).exists():
            messages.error(request, "The username already exists.")
            return render(request, "register.html", {
                "typed_username": username,
                "typed_email": email,
                "role": role_param
            })

        try:
            user = User.objects.create_user(
                username=final_username,
                password=pass1,
                email=email
            )
            user.role = final_role
            user.save()
            login(request, user)
            messages.success(request, f"Welcome, {final_username}!")
            return redirect('home')
        except Exception as e:
            messages.error(request, f"Registration failed: {e}")

    return render(request, "register.html", {"role": role_param})


@login_required
def dashboard_redirect(request):
    if request.user.role == 'admin' or request.user.is_staff:
        return redirect('admin_dashboard')
    elif request.user.role == 'agency':
        return redirect('agency_dashboard')
    else:
        return redirect('user_dashboard')


@login_required
def user_dashboard(request):

    profile, created = UserProfile.objects.get_or_create(user=request.user)

    my_collections_count = Collection.objects.filter(user=request.user).count()
    my_likes_count = Like.objects.filter(user=request.user).count()
    my_reviews_count = Review.objects.filter(user=request.user).count()
    
    recent_collections = Property.objects.filter(
        collected_by__user=request.user
    ).order_by('-collected_by__created_at')[:3]
    
    recent_likes = Property.objects.filter(
        likes__user=request.user
    ).order_by('-likes__created_at')[:3]
    
    recent_reviews = Review.objects.filter(
        user=request.user
    ).select_related('property').order_by('-created_at')[:3]
    
    context = {
        'profile': profile,
        'my_collections_count': my_collections_count,
        'my_likes_count': my_likes_count,
        'my_reviews_count': my_reviews_count,
        'recent_collections': recent_collections,
        'recent_likes': recent_likes,
        'recent_reviews': recent_reviews,
    }
    
    return render(request, "dashboards/user_dashboard.html", context)


@login_required
def agency_dashboard(request):
    if request.user.role != 'agency':
        messages.warning(request, "You don't have permission to access this page")
        return redirect('user_dashboard')

    profile, created = AgencyProfile.objects.get_or_create(user=request.user)
    
    properties = Property.objects.filter(user=request.user).order_by('-created_at')
    
    total_properties = properties.count()
    avg_rating = profile.get_avg_rating()
    
    recent_properties = properties[:5]
    
    context = {
        'profile': profile,
        'properties': recent_properties,
        'total_properties': total_properties,
        'avg_rating': avg_rating,
    }
    
    return render(request, "dashboards/agency_dashboard.html", context)

@login_required
def admin_dashboard(request):
    return render(request, "dashboards/admin_dashboard.html")


@login_required
def user_info(request):
    return render(request, "info/user_info.html")


@login_required
def agency_info(request, user_id):
    agency_user = get_object_or_404(User, pk=user_id, role='agency')
    agency_profile, created = AgencyProfile.objects.get_or_create(user=agency_user)
    properties = Property.objects.filter(user=agency_user).order_by('-created_at')
    
    total_properties = properties.count()
    avg_rating = agency_profile.get_avg_rating()
    
    recent_properties = properties[:5]
    
    context = {
        'agency_user': agency_user,
        'agency_profile': agency_profile,
        'properties': properties,
        'total_properties': total_properties,
        'avg_rating': avg_rating,
    }
    
    return render(request, "info/agency_info.html", context)

@login_required
def edit_user_profile(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully!")
            return redirect('user_dashboard')
    else:
        form = UserProfileForm(instance=profile)
    
    return render(request, "info/edit_user_profile.html", {
        'form': form,
        'profile': profile
    })


@login_required
def edit_agency_profile(request):
    if request.user.role != 'agency':
        messages.warning(request, "You don't have permission to access this page")
        return redirect('user_dashboard')
    profile, created = AgencyProfile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        form = AgencyProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully!")
            return redirect('agency_dashboard')
    else:
        form = AgencyProfileForm(instance=profile)
    
    return render(request, "info/edit_agency_profile.html", {
        'form': form,
        'profile': profile
    })
