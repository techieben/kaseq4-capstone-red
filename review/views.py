from django.shortcuts import render, reverse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.views.generic import View
from review.models import Review, Voter
from review.forms import EditReviewForm


@login_required
def UpvoteView(request, id):
    review = Review.objects.get(id=id)
    if Voter.objects.filter(user=request.user, review=review):
        voter = Voter.objects.get(user=request.user, review=review)
    else:
        voter = False
    if Review.objects.filter(id=id):
        if voter:
            if voter.vote == 'Upvote':
                voter.delete()
                review.upvotes -= 1
            elif voter.vote == 'Downvote':
                voter.delete()
                review.downvotes -= 1
                review.upvotes += 1
                Voter.objects.create(
                    user=request.user,
                    review=review,
                    vote='Upvote'
                )
        else:
            review.upvotes += 1
            Voter.objects.create(
                user=request.user,
                review=review,
                vote='Upvote'
            )
        review.save()
    return HttpResponseRedirect(reverse('recipe', args=(review.recipe.title,)))


@login_required
def DownvoteView(request, id):
    review = Review.objects.get(id=id)
    if Voter.objects.filter(user=request.user, review=review):
        voter = Voter.objects.get(user=request.user, review=review)
    else:
        voter = False
    if Review.objects.filter(id=id):
        if voter:
            if voter.vote == 'Downvote':
                voter.delete()
                review.downvotes -= 1
            elif voter.vote == 'Upvote':
                voter.delete()
                review.upvotes -= 1
                review.downvotes += 1
                Voter.objects.create(
                    user=request.user,
                    review=review,
                    vote='Downvote'
                )
        else:
            review.downvotes += 1
            Voter.objects.create(
                user=request.user,
                review=review,
                vote='Downvote'
            )
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
