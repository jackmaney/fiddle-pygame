import numpy as np


def handleCollision(ball1, ball2):

    # (I used http://stackoverflow.com/a/3349134 to double-check
    # my reasoning and calculations here)
    #
    # Now is where we need a bit of a mathematical explanation.
    # Denote ball1.getCenter() and ball2.getCenter() by C1 and C2.
    # Let d be the distance from C1 to C2, and let the radii of
    # ball1 and ball2 be r1 and r2, respectively.
    #
    # Since this method is only called when there's an intersection,
    # we'll assume that d <= r1 + r2. Since the tangent case is easy
    # (no position change, just a velocity change), we'll assume that
    # d < r1 + r2 so that we have two points of intersection.
    #
    # Let L denote the line through these points of intersection. We know
    # that L is orthogonal to the line between C1 and C2. We seek the
    # point of intersection of these lines, which I'll call Q.
    #
    # Let a denote the distance from C1 to Q, let b denote the distance
    # from C2 to Q, and let h denote the distance from Q to either of the
    # intersection points. Pythagoras tells us that:
    #
    #       a^2 + h^2 == r1^2 and b^2 + h^2 == r2^2.
    #
    # Therefore,
    #
    #       a^2 - b^2 == r1^2 - r2^2
    #
    # and taking advantage of the fact that d == a + b, we have
    #
    #       a^2 - (d - a)^2 == r1^2 - r2^2
    #
    # which simplifies to:
    #
    #       -d^2 + 2*a*d == r1^2 - r2^2
    #
    # and solving for a, we get:
    #
    #       a == (r1^2 - r2^2 + d^2) / 2*d
    #
    # We can play a similar trick and get
    #
    #       b == (r2^2 - r1^2 + d^2) / 2*d
    #
    # In particular, this means that
    #
    #   Q = C1 + a*(C2 - C1) / d
    #
    # All that we have to do now is move each of the circles away from each ball2
    # along the line between the centers, and in the amounts that are the distances
    # between Q and the edges of each circle (which are r1 - a and r2 - b, respectively).
    #
    # So, we move C1 to C1 + (r1 - a)*(C1 - C2)/r1 and C2 to C2 + (r2 - b)*(C2 - C1)/r2
    #
    # Note that we've also assumed that neither of the centers are included in the ball2 circle
    # (ie d > max(r1,r2)). We'll deal with this case--and the case of d == r1 + r2 (ie one point of
    # intersection) below.
    #

    d = ball1.distanceBetweenCenters(ball2)
    r1 = ball1.radius
    r2 = ball2.radius

    # First, though, a really dumb case...
    if d == 0:
        # Move ball1 to the left, or if we can't, move ball1 to the right
        if ball1.position[0] > r1 + r2:
            ball1.position[0] -= r1 + r2
        else:
            ball1.position[0] += r1 + r2

        ball1.velocity *= -1
        ball2.velocity *= -1
        return

    C1 = ball1.getCenter().astype(float)
    C2 = ball2.getCenter().astype(float)
    a = float(r1 * r1 - r2 * r2 + d * d) / float(2 * d)
    b = float(r2 * r2 - r1 * r1 + d * d) / float(2 * d)
    Q = C1 + a * (C2 - C1) / d

    if d < r1 + r2:

        centerCandidate = ball1.getCenter().copy()
        ball2CenterCandidate = ball2.getCenter().copy()

        if d > r1 and d > r2:

            centerCandidate = np.around(
                C1 + (r1 - a) * (C1 - C2) / r1).astype(np.int32)
            ball2CenterCandidate = np.around(
                C2 + (r2 - b) * (C2 - C1) / r2).astype(np.int32)

            # Are these candidates in bounds?

            if ball1.outOfBoundsCenter(ball2CenterCandidate):
                # Move ball1 the extra mile
                ball2CenterCandidate = ball2.getCenter()
                centerCandidate += np.around((r2 - b)
                                             * (C1 - C2) / r2).astype(np.int32)
            elif ball1.outOfBoundsCenter(centerCandidate):
                # Likewise...
                centerCandidate = ball1.getCenter()
                ball2CenterCandidate += np.around((r1 - a)
                                                  * (C2 - C1) / r1).astype(np.int32)

        elif d > r1:
            # If this is the case, then d <= r2, which means that C2 is inside of
            # the ball for ball1. We'll cheat and move ball2 the hell out of
            # dodge.

            ball2CenterCandidate = np.around(
                C2 + (d - r1 + r2) * (C2 - C1) / r2).astype(np.int32)

            if ball1.outOfBoundsCenter(ball2CenterCandidate):
                # Unless we can't...mumble grumble...
                ball2CenterCandidate = ball2.getCenter()

                centerCandidate = np.around(
                    C1 + (d - r2 + r1) * (C1 - C2) / r1).astype(np.int32)

        elif d > r2:
            # Similar case: d <= r1, so move ball1 the hell out of dodge

            centerCandidate = np.around(
                C1 + (d - r2 + r1) * (C1 - C2) / r1).astype(np.int32)

            if ball1.outOfBoundsCenter(centerCandidate):
                centerCandidate = ball1.getCenter()
                ball2CenterCandidate = np.around(
                    C2 + (d - r1 + r2) * (C2 - C1) / r2).astype(np.int32)
        else:
            # If d <= r1 and d <= r2, then C1 is inside ball2 and C2 is inside ball1
            # Again, we'll cheat and move ball1 out of dodge.

            centerCandidate = np.around(
                C1 + (r2 - d + r1) * (C1 - C2) / r1).astype(np.int32)

            if ball1.outOfBoundsCenter(centerCandidate):
                centerCandidate = ball1.getCenter()
                ball2CenterCandidate = np.around(
                    C2 + (r1 - d + r2) * (C2 - C1) / r2).astype(np.int32)

        ball1.setCenter(centerCandidate)
        ball2.setCenter(ball2CenterCandidate)

    # Ideally, we shouldn't need to worry about d == r1 + r2, but we need to fudge things a bit,
    # because otherwise the two balls will be in a perpetual state of
    # collision.
    else:
        # In this case, Q is now the point of tangency when the collision begins (as opposed to
        # the point of tangency after the collision is resolved). We move each of ball1 and ball2
        # one unit away along the line between C1 and C2. This involves adding unit vectors in the
        # appropriate directions.

        u1 = C1 - C2
        u2 = C2 - C1

        u1 /= np.linalg.norm(u1)
        u2 /= np.linalg.norm(u2)

        ball1.setCenter(C1 + u1)
        ball2.setCenter(C2 + u2)

    # Remember Q? That (up to a rounding error) is our point of tangency.
    # We'll pass Q along to the changeVelocity function.
    changeVelocity(ball1, ball2, Q)


def changeVelocity(ball1, ball2, tangentPoint):
    """
    We're given two colliding balls and the point of tangency between them. This introduces two lines:
    
        * The tangent line that goes through the tangentPoint and hits both of the bounding circles of 
            ball1 and ball2.

        * The normal line that is orthogonal to the tangent line (and goes through the center of each ball).

    This method does two main things:

        1. Resolves the velocities of each of the balls along the tangent line and along the normal.
        
        2. Treats the collision as a 1-D collision along the normal line, and finds the new 
            normal velocity components. The velocities of the balls are changed accordingly.
    """

    C1 = ball1.getCenter().astype(float)
    C2 = ball2.getCenter().astype(float)
    v1 = ball1.velocity.astype(float)
    v2 = ball2.velocity.astype(float)

    # In order to enforce a common frame of reference, we will denote the "positive" direction along
    # the normal line to be from C1 to C2. For the sake of convenience, let's take a unit vector
    # along this "positive" direction.

    u = C2 - C1
    u /= np.linalg.norm(u)

    # The 1-D velocities for our collision along the normal line will be the scalar projection of
    # v1 and v2 upon u. Since u is a unit vector, these scalar projections will just be dot products.
    # Since we've chosen a single unit vector along the tangent line, if the balls are moving in opposite
    # directions along the tangent line, then we get for free that these scalar projections will be
    # opposite in sign.

    oneDimV1 = (v1 * u).sum()
    oneDimV2 = (v2 * u).sum()

    # Before dropping into 1-D, we also compute the vector projection of the velocities onto
    # the tangent line, since we will need this to convert from the coordinate frame defined by
    # the tangent and vector lines back to our initial (ie normal x-y) coordinates.
    # Since we already have the normal components, we can just scale the unit normal vectors
    # accordingly and subtract from the velocities, like so:
    tangentVector1 = v1 - oneDimV1 * u
    tangentVector2 = v2 - oneDimV2 * u

    # Now, we're implicitly assuming that this collision is elastic (ie momentum and kinetic energy
    # are conserved). Also, the change in force occurs along the normal line. So, this is now equivalent
    # to a 1-dimensional collision problem, which is already solved.
    #
    # Look at http://en.wikipedia.org/wiki/Elastic_collision

    m1 = ball1.mass
    m2 = ball2.mass

    newOneDimV1 = (oneDimV1 * (m1 - m2) + 2 * m2 * oneDimV2) / (m1 + m2)
    newOneDimV2 = (oneDimV2 * (m2 - m1) + 2 * m1 * oneDimV1) / (m1 + m2)

    # We piece this back together to get our new velocities. And voila! We're
    # done. We just have to round to int32 coordinates.

    newVelocity1 = np.round(newOneDimV1 * u + tangentVector1).astype(np.int32)
    newVelocity2 = np.round(newOneDimV2 * u + tangentVector2).astype(np.int32)

    ball1.velocity = newVelocity1
    ball2.velocity = newVelocity2
