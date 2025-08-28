from Animations import odometer, jitter, bouncingBall, randomDesigns, chaosGame, ParticleEffect
def getAnimator(animation):
    animators = {
        "odometer": odometer.Odometer,
        "randomDesigns": randomDesigns.randomDesigns,
        "chaosGame": chaosGame.chaosGame,
        "particleEffect": ParticleEffect.ParticleEffect
    }
    return animators[animation]
