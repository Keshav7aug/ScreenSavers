from Animations import odometer, jitter, bouncingBall, randomDesigns
def getAnimator(animation):
    animators = {
        "odometer": odometer.Odometer,
        "randomDesigns": randomDesigns.randomDesigns
    }
    return animators[animation]
