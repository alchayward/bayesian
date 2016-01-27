(defproject swiss "0.2.0-SNAPSHOT"
  :dependencies [[org.clojure/clojure "1.7.0"]
                 [org.clojure/clojurescript "1.7.170"]
                 [com.taoensso/carmine "2.12.1"]
                 [reagent "0.5.1"]
                 [re-frame "0.6.0"]
                 [re-com "0.7.0"]
                 [secretary "1.2.3"]
                 [garden "1.3.0"]
                 [compojure "1.4.0"]
                 [com.cemerick/friend "0.2.1"]
                 [cljs-ajax "0.5.2"]
                 [metosin/compojure-api "0.24.3"]
                 [com.cognitect/transit-cljs "0.8.237"]
                 [differ "0.2.1"]
                 [environ "1.0.1"]
                 [ring "1.4.0"]]

  :min-lein-version "2.5.3"

  :source-paths ["src/clj"]
  
  :main ^:skip-aot swiss.core

  :profiles {:uberjar {:aot :all}} 

  :plugins [[lein-cljsbuild "1.1.1"]
            [lein-figwheel "0.5.0-2"]
            [lein-garden "0.2.6"] ]

  :clean-targets ^{:protect false} ["resources/public/js/compiled" "target"
                                    "test/js"
                                    "resources/public/css/compiled"]

  :figwheel {:css-dirs ["resources/public/css"]
             :ring-handler swiss.handler/handler}

  :garden {:builds [{:id "screen"
                     :source-paths ["src/clj"]
                     :stylesheet swiss.css/screen
                     :compiler {:output-to "resources/public/css/compiled/screen.css"
                                :pretty-print? true}}]}

  :cljsbuild {:builds [{:id "dev"
                        :source-paths ["src/cljs"]

                        :figwheel {:on-jsload "swiss.core/mount-root"}

                        :compiler {:main swiss.core
                                   :output-to "resources/public/js/compiled/app.js"
                                   :output-dir "resources/public/js/compiled/out"
                                   :asset-path "js/compiled/out"
                                   :source-map-timestamp true}}

                       {:id "test"
                        :source-paths ["src/cljs" "test/cljs"]
                        :notify-command ["phantomjs" "test/unit-test.js" "test/unit-test.html"]
                        :compiler {:optimizations :whitespace
                                   :pretty-print true
                                   :output-to "test/js/app_test.js"
                                   :warnings {:single-segment-namespace false}}}

                       {:id "min"
                        :source-paths ["src/cljs"]
                        :compiler {:main swiss.core
                                   :output-to "resources/public/js/compiled/app.js"
                                   :optimizations :advanced
                                   :closure-defines {goog.DEBUG false}
                                   :pretty-print false}}]})
