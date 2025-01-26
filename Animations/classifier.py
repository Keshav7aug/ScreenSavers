from Animations import odometer, jitter, bouncingBall
def applyAnimation(animations, theDisplay, animationArgs):
    theThings = {"data": [], "args": {}}
    for animation in animations.split("|"):
        if animation == "odometer":
            newThing = odometer.animate(theDisplay, animationArgs)
        elif animation == "jitter":
            newThing = jitter.animate(**kargs)
        elif animation == "bouncingball":
            newThing = bouncingBall.animate(**kargs)
        theThings["data"] += newThing["data"]
        theThings["args"][animation] = newThing["args"]
    return theThings
