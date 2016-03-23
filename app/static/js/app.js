'use strict';

var wishListApp = angular.module('wishListApp', ['ngRoute']);
wishListApp.controller('SignUpController' , ['$scope' , '$http', '$log',
        function($scope , $http, $log){
            $scope.user = {};
            $scope.validate = function(){
                $http.post('/signup' , $scope.user).
                    success(function(data , status){
                        $log.log('Status: ' + status);
                        $log.log('Data: ' + JSON.stringify(data));
                    }).
                error(function(data , status){
                    $log.log('Status: ' + status);
                    $log.log('Data: ' +JSON.stringify(data));
                });
            };
        }]);

wishListApp.config(function($routeProvider){
    $routeProvider.when('/signup',{
        templateUrl: 'static/js/partials/sign_up.html',
        controller: 'SignUpController',
    }).otherwise({
        redirectTo: '/signup'
    })
});
