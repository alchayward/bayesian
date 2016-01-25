(ns swiss.user
    (:require [re-frame.core :as rf]
              [re-com.core :as rc]))

(defn user-title []
  (let [title (rf/subscribe [:tournament-title])]
    (fn []
      [rc/title
       :label @title
       :level :level1])))

(defn show-game [game-id]
  (let [game (rf/subscribe [:games])])
  (fn []
    [rc/box
     :child (str (:team1 game) "vs" (:team2 game) " : " (:status game))]))

(defn court-panel court
  (fn []
    [rc/v-box
     :gap "1em"
     :children (into [] (cons [:div (str "court" (:name court))] 
                           (map show-game (take 4 (:games court)))))]))

(defn scheduled-games []
  (let [courts (rf/subscribe [:courts])]
    (fn []
      [rc/v-box
       :gap "1em"
       :children (into [] (map court-panel @courts))])))

(defn rankings-panel []
  (fn []
    [rc/box 
     :child
     ]))

(defn overview-panel []
  (fn []
    []))

(defn user-panel []
  [rc/v-box
   :gap "1em"
   :children [[user-title]
              [scheduled-games]
              [rc/h-box 
               :gap "iem"
               :children [[rankings-panel] [overview-panel]]]]])
