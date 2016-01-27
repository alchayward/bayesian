(ns swiss.request
   (:require [ajax.core :refer [GET POST]]
             [re-frame.core :refer [register-handler]]
             [cognitect.transit :as t]
             ))

(def my-endpoint "http://localhost:8888/api/user-data")

(register-handler
  :request-it   
  (fn [db _]
    ;; kick off the GET, making sure to supply a callback for success and failure
    (ajax.core/GET
      my-endpoint
      {:handler       #(dispatch [:process-response %1])   ;; further dispatch !!
       :error-handler #(dispatch [:bad-response %1])})     ;; further dispatch !!

     ;; update a flag in `app-db` ... presumably to trigger UI changes
     (assoc db :fetchng true)))    ;; pure handlers must return a db



(defn roundtrip [x]
  (let [w (t/writer :json)
        r (t/reader :json)]
    (t/read r (t/write w x))))


(register-handler            ;; when the GET succeeds 
  :process-response    
  (fn
    [db [_ response]]
    (let [r t/reader :json]
    (-> db
        (assoc :fetching false)      
        (assoc :service-data (t/read r response)))))


(register-handler
  :error-handler             
  (fn [db response]
    (assoc db :fetching false)))
