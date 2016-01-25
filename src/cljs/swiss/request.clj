(ns swiss.request
   (:require [ajax.core :refer [GET POST]]
             [re-frame.core :refer [register-handler]]))

(register-handler
  :request-it   
  (fn [db _]
    ;; kick off the GET, making sure to supply a callback for success and failure
    (ajax.core/GET
      "http://json.my-endpoint.com/blah"
      {:handler       #(dispatch [:process-response %1])   ;; further dispatch !!
       :error-handler #(dispatch [:bad-response %1])})     ;; further dispatch !!

     ;; update a flag in `app-db` ... presumably to trigger UI changes
     (assoc db :fetchng true)))    ;; pure handlers must return a db

(register-handler
  :process-response             
  (fn [db response]
    (assoc db :fetchng false)))

(register-handler
  :error-handler             
  (fn [db response]
    (assoc db :fetching false)))
