'use strict';

var wishListApp = angular.module('wishListApp', ['ngRoute' , 'ngCookies']).
run(function($cookies){
    if(!$cookies.get('loggedIn')){
        $cookies.put('loggedIn' , false);
    }
});

wishListApp.controller('SignUpController' , ['$scope' , '$http', '$log', '$location',
        function($scope , $http, $log, $location){
            $scope.user = {};
            $scope.validate = function(){
                $http.post('/signup' , $scope.user).
                    success(function(data , status){
                        $location.path('/login');
                    }).
                error(function(data , status){
                    $log.log('Status: ' + status);
                    $log.log('Data: ' +JSON.stringify(data));
                });
            };
        }]);

wishListApp.controller('LoginController' , ['$scope', '$cookies', '$http', '$log',
        function($scope , $cookies, $http, $log){
            $scope.credentials = {};
            $scope.login = function(){
                $http.post('/login' , $scope.credentials).
                    success(function(data , status){
                        $cookies.put('loggedIn' , true);
                        $cookies.put('authToken' , data.token);
                    }).
                error(function(data , status){
                    $log.log(JSON.stringify(data));
                });
            };
        }]);


wishListApp.config(function($routeProvider){
    $routeProvider.when('/signup',{
        templateUrl: 'static/js/partials/sign_up.html',
        controller: 'SignUpController',
    }).
    when('/login' , {
        templateUrl: 'static/js/partials/login.html',
        controller: 'LoginController'
    }).
    otherwise({
        redirectTo: '/signup'
    })
});
