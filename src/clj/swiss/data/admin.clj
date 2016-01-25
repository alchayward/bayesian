(ns swiss.admin
  :require [swiss.schema]
  )

;; admin actions
; add a game (round, teams)
; remove a game
; assign a game to a court. This may result in a non-satisfiable round. This should come up with a warning. 
;(what do i present in the case of no perfect matching? Algo should still work)
; give a score to a game (or set back to nil)
; update the rankings
; ask for the set of recommended games.

;would really love to use datomic, cause then I can just return the database !


(add-game 
  
  )



