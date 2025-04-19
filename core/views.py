from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, FileResponse
from django.conf import settings
from .models import Video, VideoSegment, Category, VideoCategory, DefectAnalysis
import os
from moviepy import VideoFileClip
import json

# core/views.py

def home(request):
    return render(request, 'core/index.html')

def file(request):
    videos = Video.objects.all().order_by('-uploaded_at')
    categories = Category.objects.all()
    
    if request.method == 'POST' and request.FILES.get('video_file'):
        video_file = request.FILES['video_file']
        video_name = request.POST.get('video_name', video_file.name)
        
        # Create new video object
        video = Video.objects.create(
            name=video_name,
            file=video_file
        )
        
        return redirect('file')
        
    return render(request, 'core/file.html', {
        'videos': videos,
        'categories': categories
    })

def video_detail(request, video_id):
    video = get_object_or_404(Video, id=video_id)
    segments = video.segments.all().order_by('created_at')
    categories = Category.objects.all()
    
    return render(request, 'core/video_detail.html', {
        'video': video,
        'segments': segments,
        'categories': categories
    })

def trim_video(request, video_id):
    if request.method == 'POST':
        video = get_object_or_404(Video, id=video_id)
        data = json.loads(request.body)
        
        segments_data = data.get('segments', [])
        created_segments = []
        
        for segment in segments_data:
            name = segment.get('name', f"Segment_{len(created_segments)+1}")
            start_time = float(segment.get('start_time', 0))
            end_time = float(segment.get('end_time', 0))
            category_ids = segment.get('categories', [])
            
            # Create the video segment
            video_path = os.path.join(settings.MEDIA_ROOT, str(video.file))
            
            # Generate output filename
            segment_filename = f"{video.name.split('.')[0]}_{name}_{start_time:.1f}_{end_time:.1f}.mp4"
            segment_path = os.path.join(settings.MEDIA_ROOT, 'video_segments', segment_filename)
            
            # Ensure directory exists
            os.makedirs(os.path.dirname(segment_path), exist_ok=True)
            
            # Trim the video using moviepy
            with VideoFileClip(video_path) as clip:
                subclip = clip.subclipped(start_time, end_time)
                subclip.write_videofile(segment_path, codec='libx264')
            
            # Create segment in database
            relative_path = os.path.join('video_segments', segment_filename)
            video_segment = VideoSegment.objects.create(
                name=name,
                original_video=video,
                file=relative_path,
                start_time=start_time,
                end_time=end_time
            )
            
            # Add categories
            for category_id in category_ids:
                try:
                    category = Category.objects.get(id=category_id)
                    VideoCategory.objects.create(
                        video_segment=video_segment,
                        category=category
                    )
                except Category.DoesNotExist:
                    pass
            
            created_segments.append({
                'id': video_segment.id,
                'name': video_segment.name,
                'url': video_segment.file.url if hasattr(video_segment.file, 'url') else f"/media/{video_segment.file}"
            })
        
        return JsonResponse({
            'success': True,
            'segments': created_segments
        })
    
    return JsonResponse({'success': False, 'error': 'Invalid request method'})

def analyze(request):
    categories = Category.objects.all()
    selected_category = request.GET.get('category')
    
    segments = VideoSegment.objects.all()
    if selected_category:
        segments = segments.filter(categories__category__name=selected_category)
    
    analyses = DefectAnalysis.objects.all()
    if selected_category:
        analyses = analyses.filter(category__name=selected_category)
    
    # Handle analysis form submission
    if request.method == 'POST':
        segment_id = request.POST.get('segment_id')
        category_id = request.POST.get('category_id')
        defect_type = request.POST.get('defect_type')
        severity = request.POST.get('severity')
        dimensions = request.POST.get('dimensions')
        progress = request.POST.get('progress', 0)
        
        if segment_id and category_id and defect_type and severity and dimensions:
            try:
                segment = VideoSegment.objects.get(id=segment_id)
                category = Category.objects.get(id=category_id)
                
                # Create new analysis
                analysis = DefectAnalysis.objects.create(
                    category=category,
                    severity=severity,
                    defect_type=defect_type,
                    dimensions=dimensions,
                    progress=progress,
                    video_segment=segment
                )
                
                # Return JSON response for AJAX requests
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return JsonResponse({
                        'success': True,
                        'analysis_id': analysis.id,
                        'message': 'Analysis saved successfully'
                    })
                
                return redirect('analyze')
            except (VideoSegment.DoesNotExist, Category.DoesNotExist):
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return JsonResponse({
                        'success': False,
                        'message': 'Invalid segment or category'
                    })
    
    return render(request, 'core/analyze.html', {
        'categories': categories,
        'segments': segments,
        'analyses': analyses,
        'selected_category': selected_category
    })

def download_video_segment(request, segment_id):
    segment = get_object_or_404(VideoSegment, id=segment_id)
    file_path = os.path.join(settings.MEDIA_ROOT, str(segment.file))
    
    if os.path.exists(file_path):
        response = FileResponse(open(file_path, 'rb'), as_attachment=True)
        response['Content-Disposition'] = f'attachment; filename="{os.path.basename(file_path)}"'
        return response
    
    return JsonResponse({'error': 'File not found'}, status=404)

def edit_categories(request):
    categories = Category.objects.all()
    
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description', '')
        
        if name:
            Category.objects.create(name=name, description=description)
            return redirect('edit_categories')
    
    return render(request, 'core/edit_categories.html', {'categories': categories})

def delete_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    
    if request.method == 'POST':
        category.delete()
        return redirect('edit_categories')
    
    return render(request, 'core/delete_category.html', {'category': category})

def export(request):
    categories = Category.objects.all()
    analyses = DefectAnalysis.objects.all().select_related('category', 'video_segment')
    
    return render(request, 'core/export.html', {
        'categories': categories,
        'analyses': analyses
    })
