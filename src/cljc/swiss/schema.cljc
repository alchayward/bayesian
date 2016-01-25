(ns swiss.schema
  :require [prismatic.schema :as s])


(def Game
  {:teams [s/Int] ;should specify two exactly
  :results (s/maybe [s/Int]) ; nil if unplayed. should specify two exactly
  :round s/Int
  :status (s/maybe s/Keyword) ;possible status. played/unplayed. canceled etc. 
  :id s/Int})

(def Player
  {:id s/Int
   :name s/Str
   :home s/Str})

(def Team
  {:name s/Str
  :id s/Int
  :players [s/Int]})

(def Court
  {:id s/Int
   :name s/Str
   :last-played (s/maybe s/Int)
   :now-playing (s/maybe s/Int)
   :scheduled [s/Int]})

(def Session
  {:name s/Str
   :id s/Int
   :type s/Keyword
   :games [Game]
   :settings
     { :allow-multiple-meets s/Bool
       :ranking-method s/Keyword}
   :courts [Court]})

(def Tournament
  {:id s/Int
   :name s/Str
   :location (s/maybe s/Str)
   (s/optional-key :sessions) [Session]
   })

