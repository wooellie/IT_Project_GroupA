from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django import forms

# 导入你的模型和表单
from .models import Property, User, Like, Collection
from .forms import PropertyForm  # 确保你已经创建了 forms.py

# --- 1. 首页：增加搜索逻辑 (M2) ---
def home(request):
    query = request.GET.get('q') # 获取搜索框的内容
    if query:
        # 根据邮编进行模糊查询
        properties = Property.objects.filter(zip_code__icontains=query).order_by("-created_at")
    else:
        properties = Property.objects.all().order_by("-created_at")
    
    return render(request, "home.html", {"properties": properties, "query": query})

# --- 2. 房源详情页 (M3) ---
@login_required
def property_detail(request, pk):
    property_obj = get_object_or_404(Property, pk=pk)
    # 检查状态
    is_liked = Like.objects.filter(user=request.user, property=property_obj).exists()
    is_collected = Collection.objects.filter(user=request.user, property=property_obj).exists()
    
    return render(request, "properties/property_detail.html", {
        "property": property_obj,
        "is_liked": is_liked,
        "is_collected": is_collected,
        "like_count": property_obj.likes.count()
    })

# --- 3. 发布房源：合并逻辑并增加保存功能 (M5) ---
@login_required
def post_property(request):
    # 权限检查
    if request.user.role != 'agency' and not request.user.is_superuser:
        messages.error(request, "Only Agency accounts can post properties.")
        return redirect('home')
    
    if request.method == "POST":
        # 注意：上传图片必须传 request.FILES
        form = PropertyForm(request.POST, request.FILES)
        if form.is_valid():
            new_prop = form.save(commit=False)
            new_prop.owner = request.user # 绑定当前发布者
            new_prop.save()
            messages.success(request, "Property posted successfully!")
            return redirect('home')
    else:
        form = PropertyForm()
    
    return render(request, "properties/property_form.html", {"form": form})

# --- 4. 互动逻辑：点赞与收藏 ---
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

# --- 5. 列表页：我的点赞与我的收藏 ---
@login_required
def my_likes(request):
    liked_properties = Property.objects.filter(likes__user=request.user).order_by("-created_at")
    return render(request, "collections/my_likes.html", {"properties": liked_properties})

@login_required
def my_collection(request):
    collected_properties = Property.objects.filter(collected_by__user=request.user).order_by("-created_at")
    return render(request, "collections/my_collection.html", {"properties": collected_properties})

# --- 6. 身份认证：注册与仪表盘 ---
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
            return render(request, "register.html", {"typed_username": username, "typed_email": email, "role": role_param})

        if User.objects.filter(username=final_username).exists():
            messages.error(request, "The username already exists.")
            return render(request, "register.html", {"typed_username": username, "typed_email": email, "role": role_param})

        try:
            user = User.objects.create_user(username=final_username, password=pass1, email=email)
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

# 各类占位视图
@login_required
def user_dashboard(request): return render(request, "dashboards/user_dashboard.html")
@login_required
def agency_dashboard(request): return render(request, "dashboards/agency_dashboard.html")
@login_required
def admin_dashboard(request): return render(request, "dashboards/admin_dashboard.html")
@login_required
def user_info(request): return render(request, "info/user_info.html")
@login_required
def agency_info(request): return render(request, "info/agency_info.html")