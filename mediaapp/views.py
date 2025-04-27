from django.shortcuts import render, redirect, get_object_or_404
from .models import MediaFile
from .forms import MediaFileForm
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib import messages  # For success messages

# Upload Media
def upload_media(request):
    if request.method == 'POST':
        form = MediaFileForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Media uploaded successfully!')
            return redirect('media_list')
    else:
        form = MediaFileForm()
    return render(request, 'mediaapp/upload.html', {'form': form})

# List Media with Pagination and Search
def media_list(request):
    query = request.GET.get('q', '')
    files = MediaFile.objects.filter(
        Q(title__icontains=query) | Q(tags__icontains=query)
    ).order_by('-uploaded_at')

    paginator = Paginator(files, 5)  # 5 per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'mediaapp/media_list.html', {'page_obj': page_obj, 'query': query})

# Edit Media
def edit_media(request, pk):
    media = get_object_or_404(MediaFile, pk=pk)
    if request.method == 'POST':
        form = MediaFileForm(request.POST, request.FILES, instance=media)
        if form.is_valid():
            form.save()
            messages.success(request, 'Media updated successfully!')
            return redirect('media_list')
    else:
        form = MediaFileForm(instance=media)
    return render(request, 'mediaapp/edit_media.html', {'form': form})

# Delete Media
def delete_media(request, pk):
    media = get_object_or_404(MediaFile, pk=pk)
    media.delete()
    messages.success(request, 'Media deleted successfully!')
    return redirect('media_list')

# View Media Details (New View)
def view_media(request, pk):
    media = get_object_or_404(MediaFile, pk=pk)
    return render(request, 'mediaapp/view_media.html', {'media': media})
