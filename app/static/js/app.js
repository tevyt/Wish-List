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

wishListApp.controller('LoginController' , ['$scope', '$cookies',  function($scope , $cookies){
    $scope.login = function(){
        $cookies.put('loggedIn' , true);
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
