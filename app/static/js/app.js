'use strict';

var wishListApp = angular.module('wishListApp', ['ngRoute']);
wishListApp.controller('SignUpController' , ['$scope' , '$http',
        function($scope , $http){
            $scope.user = {};
        }]);

wishListApp.config(function($routeProvider){
    $routeProvider.when('/signup',{
        templateUrl: 'static/js/partials/sign_up.html',
        controller: 'SignUpController',
    }).otherwise({
        redirectTo: '/signup'
    })
});
