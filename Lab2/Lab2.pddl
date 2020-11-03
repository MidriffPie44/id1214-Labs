(define domain(Lab2)
    (:requirements :strips :equality)
    (:predicates (clear ?x)
                 (on-table ?x)
                 (gripper ?g)
                 (arm-empty)
                 (holding ?x)
                 (on ?x ?y))
                 (move ?x ?y)
                 (Room ?r)
                 (at-robby ?r)
                 (free ?g)
                 (carry ?o ?g)) 

    (:action pick
       :parameters (?obj ?room ?gripper)
       :precondition  (and  (ball ?obj) (room ?room) (gripper ?gripper)
			    (at ?obj ?room) (at-robby ?room) (free ?gripper))
       :effect (and (carry ?obj ?gripper)
		    (not (at ?obj ?room)) 
		    (not (free ?gripper))))


   (:action drop
       :parameters  (?obj  ?room ?gripper)
       :precondition  (and  (ball ?obj) (room ?room) (gripper ?gripper)
			    (carry ?obj ?gripper) (at-robby ?room))
       :effect (and (at ?obj ?room)
		    (free ?gripper)
		    (not (carry ?obj ?gripper)))))


    (:action stack
        :parameters  (?ob ?underob)
      //:precondition (and  (clear ?underob) (holding ?ob) (not (= ?ob ?underob)) )
        :precondition (and  (clear ?underob) (holding ?ob))
        :effect (and (arm-empty) (clear ?ob) (on ?ob ?underob)
               (not (clear ?underob)) (not (holding ?ob))))

    (:action unstack
        :parameters  (?ob ?underob)
        :precondition (and (on ?ob ?underob) (clear ?ob) (arm-empty))
        :effect (and (holding ?ob) (clear ?underob)
               (not (on ?ob ?underob)) (not (clear ?ob)) (not (arm-empty))))) 

    (:action move
       :parameters  (?from ?to)
       :precondition (and  (room ?from) (room ?to) (at-robby ?from))
       :effect (and  (at-robby ?to)
		     (not (at-robby ?from))))                 
