from django.contrib import admin

from .models import Round, Question, Choice, Game, Player

admin.site.site_header = "Walter Admin"
admin.site.site_title = "Walter Admin Area"
admin.site.index_title = "Welcome to the Walter admin area"

class RoundInline(admin.TabularInline):
    model = Round
    extra = 3


class PlayerInline(admin.TabularInline):
    model = Player
    extra = 3


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3


class QuestionInline(admin.TabularInline):
    model = Question
    extra = 3


class QuestionAdmin(admin.ModelAdmin):
    inlines = [ChoiceInline]


class RoundAdmin(admin.ModelAdmin):
    inlines = [QuestionInline]


class GameAdmin(admin.ModelAdmin):
    inlines = [RoundInline, PlayerInline]


admin.site.register(Player)
admin.site.register(Game)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Round, RoundAdmin)
