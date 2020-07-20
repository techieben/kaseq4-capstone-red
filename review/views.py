from django.shortcuts import render, reverse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.views.generic import View
from review.models import Review
from review.forms import EditReviewForm


@ login_required
def UpvoteView(request, id):
    review = Review.objects.get(id=id)
    # if Review.objects.filter(id=id).filter(voters=request.user):
    review.upvotes += 1
    review.voters.add(request.user)
    review.save()
    return HttpResponseRedirect(reverse('recipe', args=(review.recipe.title,)))

# @login_required
# def UpvoteView(request, id):
#     review = Review.objects.get(id=id)
#     print("upvote clicked")
#     if request.user.username not in review.voters.values_list('username'):
#         print("request.user.username = ", request.user.username)
#         print("review.voters.values_list = ", review.voters.values_list('username'))
#         print("upvotes before = ", review.upvotes)
#         review.upvotes += 1
#         review.voters.add(request.user)
#         review.save()
#         print("upvotes after = ", review.upvotes)
#     else:
#         print("upvote exiting no action")
#     return HttpResponseRedirect(reverse('recipe', args=(review.recipe.title,)))


@ login_required
def DownvoteView(request, id):
    review = Review.objects.get(id=id)
    # if Review.objects.filter(id=id).filter(voters=request.user):
    review.downvotes += 1
    review.voters.add(request.user)
    review.save()
    return HttpResponseRedirect(reverse('recipe', args=(review.recipe.title,)))


class ReviewEditView(View):

    def get(self, request, id):
        html = 'recipe_edit.html'
        review = Review.objects.get(id=id)
        form = EditReviewForm(instance=review)
        return render(request, html, {'form': form})

    def post(self, request, id):
        html = 'recipe_edit.html'
        review = Review.objects.get(id=id)
        form = EditReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('recipe', args=(review.recipe.title,)))
        return render(request, html, {'form': form})
