(ns swiss.handler
  (:require [compojure.core :refer [GET defroutes]]
            [ring.util.response :refer [file-response]]))

(defroutes handler
  (GET "/" [] (file-response "index.html" {:root "resources/public"})))



(defn generate-response [data & [status]]
  {:status (or status 200)
   :headers {"Content-Type" "application/edn"}
   :body (pr-str data)})

(defn update-class [id params]
  (let [db    (d/db conn)
        title (:class/title params)
        eid   (ffirst
                (d/q '[:find ?class
                       :in $ ?id
                       :where 
                       [?class :class/id ?id]]
                  db id))]
    (d/transact conn [[:db/add eid :class/title title]])
    (generate-response {:status :ok})))
