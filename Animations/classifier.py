from Animations import odometer, jitter, bouncingBall
def getAnimator(animation, theDisplay):
    animators = {
        "odometer": odometer.Odometer,
    }
    return animators[animation](theDisplay)
