(define (domain aoc16_domain)

    ;remove requirements that are not needed
    ; (:requirements :strips :typing :numeric-fluents :action-costs :negative-preconditions)
    ; (:requirements :strips :typing :action-costs)
    ;(:requirements :strips :fluents :durative-actions :timed-initial-literals :typing :conditional-effects :negative-preconditions :duration-inequalities :equality)

    (:requirements :action-costs :conditional-effects :typing :negative-preconditions :adl)

    (:types player field)

    (:predicates
        (on ?player - player ?loc - field)
        (neighbor ?start - field ?end - field)
        (closed ?loc - field)
    )

    (:functions
        (flow-total) - number
        (time) - number
        (flow-value ?loc - field) - number
    )

    (:action move
        :parameters (?player - player ?from - field ?to - field)
        :precondition (and
            (on ?player ?from)
            (neighbor ?from ?to)
            (> (time) 0)
        )
        :effect (and
            (on ?player ?to)
            (not (on ?player ?from))
            (decrease (time) 1)
        )
    )

    (:action activate
        :parameters (?player - player ?loc - field)
        :precondition (and
            (on ?player ?loc)
            (closed ?loc)
            (> (time) 0)
        )
        :effect (and
            (not (closed ?loc))
            (decrease (time) 1)
            (increase (flow-total) (* time (flow-value ?loc)))
        )
    )

)
