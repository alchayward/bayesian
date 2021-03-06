(ns swiss.views
    (:require [re-frame.core :as re-frame]
              [re-com.core :as re-com]
              [swiss.user :as user]
              ))


;; home

(defn home-title []
  (let [name (re-frame/subscribe [:name])]
    (fn []
      [re-com/title
       :label (str "Hello from " @name ". This is the Home Page.")
       :level :level1])))

(defn link-to-about-page []
  [re-com/hyperlink-href
   :label "go to About Page"
   :href "#/about"])

(defn link-to-user-page []
  [re-com/hyperlink-href
   :label "go to User Page"
   :href "#/user"])

(defn home-panel []
  [re-com/v-box
   :gap "1em"
   :children [[home-title] [link-to-about-page]]])


;; about

(defn about-title []
  [re-com/title
   :label "This is the About Page."
   :level :level1])

(defn link-to-home-page []
  [re-com/hyperlink-href
   :label "go to Home Page"
   :href "#/"])

(defn about-panel []
  [re-com/v-box
   :gap "1em"
   :children [[about-title] [link-to-home-page]]])


;; main

(defmulti panels identity)
(defmethod panels :user-panel [] [user-panel])
(defmethod panels :home-panel [] [home-panel])
(defmethod panels :about-panel [] [about-panel])
(defmethod panels :default [] [:div])

(defn main-panel []
  (let [active-panel (re-frame/subscribe [:active-panel])]
    (fn []
      [re-com/v-box
       :height "100%"
       :children [(panels @active-panel)]])))

(defn top-panel    ;; this is new
  []
  (let [ready?  (subscribe [:initialised?])]
    (fn []
      (if-not @ready?         ;; do we have good data?
        [:div "Initialising ..."]   ;; tell them we are working on it
        [main-panel]))))      ;; all good, render this component

