(ns swiss.api
(:require [ring.util.http-response :refer :all]
            [compojure.handler :refer [api]]
            [compojure.core :refer [GET POST context]]
            [swiss.schema :refer :all]
            [prismatic.schema :as s]))

(def get-tournaments [])

;;
;;Routes
;; man, this is real dumb. Pretty sure there's a better way then this dumb http stuff

(defn session-admin [t-id s-id]
  (POST "/" [] )
  )

(defn sessions [t-id] 
  (context "/sessions" []
    (Get "/" []
      :return [Session]
      :summary "returns all sessions in tournament :id"
      (ok (get-sessions t-id))
      (context "/:s-id" []
        :path-params [s-id :- s/Int]
        (GET "/" []
          :return (s/maybe Session)
          :summary "Gets a session in t-id with s-id"
          (ok (get-session t-id s-id)))
        (GET "/get-updates/:state"
          :path-params [:state s/Int]
          :return (s/maybe DateTime)
          :summary "returns an updater to get the client
                   up to the latest state from :state"
          (ok (get-update t-id s-id state)))
        (session-admin t-id s-id)
        ))))

(defn team-admin [team-id]
  
  )

(defn teams [] 
  (context "/teams" []
    (GET "/" []
      :return [Team]   
      :summary "return a list of teams"
      (ok (get-teams t-id)))
    (GET "/:team-id" []
      :path-params [team-id :- s/Int]
      :return (s/maybe Team)
      :summary "return team with id team-id"
      (ok (get-team t-id team-id)))
    (team-admin team-id)
    ))

(defn tournament-admin [t-id]
  (routes
    (POST "/new-tournament" [])
                  
                                ))

(defn tournament-routes []
  (context "/tournaments" []
    :tags ["sessions" "teams"]
    (GET "/" []
      :return [Tournament]
      :summary "Gets all tournaments, but only name + id"
      (ok (get-tournaments)))
    (context "/:t-id" [t-id]
      (GET "/" [] (ok (get-tournament t-id)))
      (tournament-admin t-id)
      (teams)
      (sessions)
      )))



(defn player-routes [] 
  (GET "/players/:p-id" [p-id]
        :path-params [p-id :- s/Int]
        :return (s/maybe Player)
        :summary "gets a p-id player map "
        (ok (get-player p-id))))

(defn api-routes []
  (routes 
    (tournament-routes)
    (player-routes)))

(api (defroutes (context "/api" [] (api-routes))))

 


;;I repeat myself A LOT here. seems like a fairly standard pattern too.
;; should probably write a function (might even need a macro) 
;; Put in a structure for the api, and spit out this route. since all the names are repeted it would just reuse that info all the time.







