from django.db import models
from django.conf import settings
# Create your models here.

class AritcleLike(models.Model):
    # 좋아요 한 사람의 id
    likefrom_id = models.IntegerField()
    # 좋아요 한 사람의 닉네임
    likefrom = models.CharField(max_length=150)
    # 좋아요 받은 글의 id
    liked_article = models.IntegerField()
    # 좋아요 받은 글의 내용
    liked_content = models.CharField(max_length=250)
    # 좋아요 받은 글의 길드id
    guild = models.IntegerField()
    # 좋아요 받은 글의 길드 이름
    guildname = models.CharField(max_length=200)
    # 좋아요 받은 사람의 id
    liketo = models.IntegerField()
    # 좋아요 받은 시각
    created_at = models.DateTimeField(auto_now_add=True)
    # 알림 확인 여부
    state = models.IntegerField(default=0)




class Guild(models.Model):
    name = models.CharField(max_length=150)
    manager = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='my_guilds')
    guild_img = models.CharField(max_length=200,null=True)
    guild_image = models.ImageField(upload_to='guild_img/', null=True)
    profile_content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_open = models.BooleanField()
    users = models.ManyToManyField(settings.AUTH_USER_MODEL, through='GuildUser')
    # tags =  models.ManyToManyField(Tag, through='GuildTag')
    
# guild와 tag의 정보를 담는 모델
class GuildTag(models.Model):
    tag = models.CharField(max_length=150)
    guild = models.IntegerField()

# guild와 user의 중계테이블
class GuildUser(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    guild = models.ForeignKey(Guild,on_delete=models.CASCADE)
    

# 길드 작성글
class GuildArticle(models.Model):
    # 작성자 정보
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    nickname = models.CharField(max_length=150)
    profile_img = models.CharField(max_length=300,null=True)

    # 길드이름 추가 
    guild_name = models.CharField(max_length=150)
    # 해당 길드에서 몇번째 글인지 
    article_num = models.IntegerField()
    guild_id = models.ForeignKey(Guild, on_delete=models.CASCADE)
    content = models.TextField()
    img = models.ImageField(upload_to='origins/', null=True)

    # 참조하는 글은 해당 길드에서 몇번째인지
    parent_article = models.IntegerField(null=True)
    # 참조하는 글의 작성자
    parent_username = models.CharField(max_length=150,null=True)


    created_at = models.DateTimeField(auto_now_add=True)
    like_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='like_articles',blank=True)

# 해당 길드 몇번째 글까지 작성했는지 기록하는 모델
class GuildArticleCount(models.Model):
    guild=models.IntegerField()
    cnt = models.IntegerField(default=1)

# 길드 신청 (해당길드, 신청자)
class GuildSignup(models.Model):
    guild = models.IntegerField()
    user = models.IntegerField()