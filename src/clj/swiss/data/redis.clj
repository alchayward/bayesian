(ns swiss.redis
  (:require [taoensso.carmine :as car :refer  (wcar)]))

(require '[environ.core :refer [env]])
(def redis-spec (env :redis-spec))
(def server1-conn {:pool {} :spec redis-spec})



