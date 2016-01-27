(ns swiss.subs
    (:require-macros [reagent.ratom :refer [reaction]])
    (:require [re-frame.core :as re-frame]))


(register-sub       ;; we can check if there is data
  :initialised?     ;; usage (subscribe [:initialised?])
  (fn  [db]
    (reaction (not (empty? @db)))))  ;; do we have data

(re-frame/register-sub
 :name
 (fn [db]
   (reaction (:name @db))))

(re-frame/register-sub
 :active-panel
 (fn [db _]
   (reaction (:active-panel @db))))



(re-frame/register-sub
 :teams
 (let [tournament-id (re-frame/subscribe [:active-tournament])
       bracket-id (re-frame/subscribe [:active-bracket])]
  (fn [db tournament-id bracket-id]
   (reaction (get-in @db {:tournaments tournament-id bracket-id :teams})))))

(re-frame/register-sub
 :courts
 (fn [db tournament-id bracket-id]
   (reaction (get-in @db {:tournaments tournament-id bracket-id :courts}))))

(re-frame/register-sub
 :games
 (fn [db tournament-id bracket-id]
   (reaction (get-in @db {:tournaments tournament-id bracket-id :games}))))
