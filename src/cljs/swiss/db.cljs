(ns swiss.db)

(def swiss-bracket
  {:rankings []
   :team-focus nil
   :view-focus nil
   })
(def bracket
  {:type :swiss
   :page-data swiss-bracket
   })
(def user-page 
  {:tournament-id nil
   :bracket nil
   })

(def admin-page
  {}
  )
(def court
  {:name "A"
   :games [1 2 3 4]
   }
  )

(def courts
  [court]
  )
(def app-db
  {:app-name "bayesian-swiss"
   :active-tournament nil
   :admin false 
   :user nil
   :tournament-list nil 
   :user-page user-page 
   :admin-page admin-page
   })


