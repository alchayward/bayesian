(ns swiss.data.game
  (:require [taoensso.carmine :as car :refer  (wcar)]
            ))


(use '[clojure.string :only (join split)])

;REDIS address
(def server1-conn {:pool {} :spec {:host "127.0.0.1" :port 6379}})

(defmacro wcar* [& body] `(wcar server1-conn ~@body))

(def ^:dynamic write-game)
;we send through the whole updated game
;need to indicate that the state has changed.
;only need to say when the score has changed.
;Or maybe we leave it up to the admin to run the scores. we can test current status by increasing the session clock.

(
  [:add (fn [game] 
          )]
  )

(defn add-game
  [game]
  (write-game (update-in game [:id] (new-game-id))))

()

(defn change-game-score
  [game results]
  
  )

(defn change-game-)

(defn games-key
  [t-id s-id g-id]
  (join "" ["t:" t-id ":s:" s-id ":game:" g-id]))
(games 0) 
(wcar* (car/del games-key))
(def games {0 [0 1 -1 -1 1]
           1 [2 3 3 1 1]})

(games 1)

(defn write-game 
  [t-id s-id g-id game]
  (let [k (games-key t-id s-id g-id)]
   (wcar* (car/del k)
          (mapv
            (fn [x] (car/rpush k x))
            game)) ))

(write-game 1 1 0 (games 0))

(wcar* (car/del "games"))
(wcar* (car/rpush games-key (str ) ))
(wcar* (car/rpush games-key (str [2 3 1 4 1]) ))

(wcar* (car/lrange "games" 0 -1))

(wcar* (car/set "games" 0))
(wcar* (car/set "games" games))
