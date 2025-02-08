from Animations import odometer, jitter, bouncingBall, randomDesigns, chaosGame
def getAnimator(animation):
    animators = {
        "odometer": odometer.Odometer,
        "randomDesigns": randomDesigns.randomDesigns,
        "chaosGame": chaosGame.chaosGame
    }
    return animators[animation]
