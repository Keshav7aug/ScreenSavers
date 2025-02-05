from Animations import odometer, jitter, bouncingBall
def getAnimator(animation):
    animators = {
        "odometer": odometer.Odometer,
    }
    return animators[animation]
