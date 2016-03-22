'use strict';

var wishListApp = angular.module('wishListApp', ['ngRoute']);
wishListApp.controller('SignUpController' , ['$scope' , '$http',
        function($scope , $http){
            $scope.profile_url = "https://encrypted-tbn1.gstatic.com/images?q=tbn:ANd9GcQ1uNq8D2knHJ6qlIybMOrI-Q1c0GXAXpsQH5L6qtwOeyuG6b-bGOLDk1M"
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
