from django.db import models

class Video(models.Model):
    name = models.CharField(max_length=100)
    file = models.FileField(upload_to='videos/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class VideoSegment(models.Model):
    name = models.CharField(max_length=100)
    original_video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name='segments')
    file = models.FileField(upload_to='video_segments/')
    start_time = models.FloatField()
    end_time = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.name} ({self.original_video.name})"

class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class VideoCategory(models.Model):
    video_segment = models.ForeignKey(VideoSegment, on_delete=models.CASCADE, related_name='categories')
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.video_segment.name} - {self.category.name}"

class DefectAnalysis(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    severity = models.CharField(max_length=50, choices=[('Critical', 'Critical'), ('Moderate', 'Moderate'), ('Low', 'Low')])
    defect_type = models.CharField(max_length=100)
    dimensions = models.CharField(max_length=100)
    progress = models.IntegerField(default=0)
    video_segment = models.ForeignKey(VideoSegment, on_delete=models.CASCADE, related_name='analyses', null=True, blank=True)

    def __str__(self):
        return f"{self.category.name} - {self.defect_type}"
