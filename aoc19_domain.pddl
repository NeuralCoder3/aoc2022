(define (domain aoc19_domain)

    ;remove requirements that are not needed
    ; (:requirements :strips :typing :numeric-fluents :action-costs :negative-preconditions)
    ; (:requirements :strips :typing :action-costs)
    ;(:requirements :strips :fluents :durative-actions :timed-initial-literals :typing :conditional-effects :negative-preconditions :duration-inequalities :equality)

    (:requirements :action-costs :conditional-effects :typing :negative-preconditions :adl)

    (:predicates
        (done)
    )

    (:functions
        (time) - number
        (ore) - number
        (clay) - number
        (obsidian) - number
        (geode) - number
        (robotOre) - number
        (robotClay) - number
        (robotObsidian) - number
        (robotGeode) - number
    )

    (:action finish
        :precondition (and
            (= (time) 0)
        )
        :effect (and
            (done)
        )
    )

    (:action step
        :precondition (and
            (> (time) 0)
        )
        :effect (and
            (decrease (time) 1)
            (increase (ore) robotOre)
            (increase (clay) robotClay)
            (increase (obsidian) robotObsidian)
            (increase (geode) robotGeode)
        )
    )

    (:action buyOreRobot
        :precondition (and
            (>= (ore) 4)
            (> (time) 0)
        )
        :effect (and
            (increase (ore) robotOre)
            (increase (clay) robotClay)
            (increase (obsidian) robotObsidian)
            (increase (geode) robotGeode)
            (decrease (time) 1)
            (increase (robotOre) 1)
            (decrease (ore) 4)
        )
    )

    (:action buyClayRobot
        :precondition (and
            (>= (ore) 2)
            (> (time) 0)
        )
        :effect (and
            (increase (ore) robotOre)
            (increase (clay) robotClay)
            (increase (obsidian) robotObsidian)
            (increase (geode) robotGeode)
            (decrease (time) 1)
            (increase (robotClay) 1)
            (decrease (ore) 2)
        )
    )

    (:action buyObsidianRobot
        :precondition (and
            (>= (ore) 3)
            (>= (clay) 14)
            (> (time) 0)
        )
        :effect (and
            (increase (ore) robotOre)
            (increase (clay) robotClay)
            (increase (obsidian) robotObsidian)
            (increase (geode) robotGeode)
            (decrease (time) 1)
            (increase (robotObsidian) 1)
            (decrease (ore) 3)
            (decrease (clay) 14)
        )
    )

    (:action buyGeodeRobot
        :precondition (and
            (>= (ore) 2)
            (>= (obsidian) 7)
            (> (time) 0)
        )
        :effect (and
            (increase (ore) robotOre)
            (increase (clay) robotClay)
            (increase (obsidian) robotObsidian)
            (increase (geode) robotGeode)
            (decrease (time) 1)
            (increase (robotGeode) 1)
            (decrease (ore) 2)
            (decrease (obsidian) 7)
        )
    )

    

)
