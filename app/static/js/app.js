'use strict';

var wishListApp = angular.module('wishListApp', ['ngRoute' , 'ngCookies']).
run(function($cookies, $rootScope, $location, $http, $log){
    if(!$cookies.get('loggedIn')){
        $cookies.put('loggedIn' , false);
        $rootScope.loggedIn = false;
    }else if($cookies.get('loggedIn') === 'true'){
        $rootScope.loggedIn = true;
        $rootScope.currentUserName = $cookies.get('currentUserName');
    }
    $rootScope.getMyWishlist= function(){
        $cookies.put('selectedUser' , $cookies.get('currentUserId'));
        $location.path('/me');
    };
    $rootScope.logout = function(){
        $http.delete('/logout/' + $cookies.get('currentUserId'), {headers:{'AuthToken': $cookies.get('authToken')}}).
            success(function(data , status){
                $log.log('Status: ' + status);
                $log.log(JSON.stringify(data));
                $cookies.put('loggedIn' , false);
                $cookies.remove('authToken');
                $cookies.remove('currentUserId');
                $cookies.remove('currentUserName');
                $rootScope.loggedIn = false;
                delete $rootScope.currentUserName;
                $location.path('/login');
            }).
        error(function(data , status){
            $log.log('Status: ' + status);
            $log.log(JSON.stringify(data));
            $rootScope.error = true;
            $rootScope.errors = data;
        });
    };
    $rootScope.error = false;
    $rootScope.errors = {};
});

wishListApp.controller('SignUpController' , ['$scope' , '$http', '$log', '$location','$rootScope',
        function($scope , $http, $log, $location, $rootScope){
            $rootScope.error = false;
            $scope.user = {};
            $scope.validate = function(){
                $http.post('/signup' , $scope.user).
                    success(function(data , status){
                        $location.path('/login');
                    }).
                error(function(data , status){
                    $rootScope.error = true;
                    $rootScope.errors = data;
                });
            };
        }]);

wishListApp.controller('LoginController' , ['$scope', '$cookies', '$http', '$log', '$location','$rootScope',
        function($scope , $cookies, $http, $log, $location,$rootScope){
            if($cookies.get('loggedIn') === 'true'){
                $location.path('/friends');
            }
            $rootScope.error = false;
            $scope.credentials = {};
            $scope.login = function(){
                $http.post('/login' , $scope.credentials).
                    success(function(data , status){
                        $cookies.put('loggedIn' , true);
                        $cookies.put('authToken' , data.token);
                        $cookies.put('currentUserId' , data.id);
                        $cookies.put('currentUserName' , data.firstname);
                        $rootScope.loggedIn = true;
                        $rootScope.currentUserName = data.firstname;
                        $location.path('/friends');
                    }).
                error(function(data , status){
                    $log.log(JSON.stringify(data));
                    $rootScope.error = true;
                    $rootScope.errors = data;
                });
            };
        }]);

wishListApp.controller('FriendsController' , ['$scope', '$http', '$log', '$cookies','$location','$rootScope',
        function($scope, $http , $log, $cookies, $location, $rootScope){
            $rootScope.error = false;
            $scope.$on('$routeChangeSuccess' , function(event , current){
                $http.get('/wishlist').
                    success(function(data , status){
                        $scope.users = data;
                    }).
                error(function(data , status){
                    $log.log(JSON.stringify(data));
                    $rootScope.error = true;
                    $rootScope.errors = data;
                });
            });
            $scope.getWish = function(id){
                $cookies.put('selectedUser' , id)
                    $location.path('/wishlist')
            };

            $scope.currentUser = function(id){
                return $cookies.get('currentUserId') == id
            }
        }]);

wishListApp.controller('WishListController' , ['$scope' , '$cookies' , '$http' , '$location', '$log', '$rootScope' ,
        function($scope , $cookies, $http, $location, $log, $rootScope){
            $rootScope.error = false;
            if($cookies.get('selectedUser')){
                $scope.id = $cookies.get('selectedUser');
            }else if($cookies.get('currentUserId')){
                $scope.id = $cookies.get('currentUserId');
            }else{
                $location.path('/login');
            }
            $http.get('/wishlist/' + $scope.id).
                success(function(data , status){
                    $scope.firstname = data.firstname;
                    $scope.items = data.items;
                }).
            error(function(data , status){
                $log.log(JSON.stringify(data));
                $rootScope.error=true;
                $rootScope.errors = data;
            });
            $scope.currentUser = function(){
                return $scope.id == $cookies.get('currentUserId');
            }
            $scope.openAddItemForm = function(){
                $location.path('/new');
            };
            $scope.deleteItem = function(id , index){
                $http.delete('/wishlist/' + $cookies.get('currentUserId') + '/' + id , {headers:{'AuthToken': $cookies.get('authToken')}}).
                    success(function(data , status){
                        $scope.items.splice(index , 1);
                    }).
                error(function(data , status){
                    $log.log(JSON.stringify(data));
                    $rootScope.error = true;
                    $rootScope.errors = data;
                });
            }
            $scope.viewItem = function(id){
                $cookies.put('item' , id);
                $cookies.put('selectedUser', $scope.id);
                $location.path('/item');
            }
        }]);

wishListApp.controller('NewItemController' , ['$scope' , '$cookies', '$log', '$location', '$http','$rootScope' ,
        function($scope , $cookies , $log, $location, $http,$rootScope){
            $rootScope.error = false;
            if($cookies.get('loggedIn') !== 'true'){
                $location.path('/login');
            }
            $scope.scrape = function(url){
                $http.post('/scrape' , {'url': url} ).
                    success(function(data , status){
                        $scope.images = data.images;
                        $scope.selectedImage = $scope.images[0].url;
                        $scope.title = data.title;
                    }).
                error(function(data , status){
                    $log.log(data);
                    $rootScope.error = true;
                    $rootScope.errors = data;
                });
                $scope.selectImage = function(image){
                    $scope.selectedImage = image;
                };

            }
            $scope.createItem = function(){
                var item = {'thumbnail_url' : $scope.selectedImage,
                    'name': $scope.title,
                    'description': $scope.description}; 
                $http.post('/wishlist/' + $cookies.get('currentUserId') , item , {headers:{'AuthToken': $cookies.get('authToken')}}).
                    success(function(data , status){
                        $location.path('/wishlist'); 
                    }).
                error(function(data , status){
                    $log.log(JSON.stringify(data));
                    $rootScope.error = true;
                    $rootScope.errors = data;
                });
            };

        }]);
wishListApp.controller('ItemController' , ['$scope' , '$cookies', '$location','$http','$log','$rootScope',
        function($scope , $cookies, $location, $http, $log,$rootScope){
            $rootScope.error = false;
            if(!$cookies.get('selectedUser') || !$cookies.get('item')){
                $location.path('/friends');
            }
            var userId = $cookies.get('selectedUser');
            var itemId = $cookies.get('item');
            $http.get('/wishlist/' + userId + '/' + itemId).
                success(function(data ,status){
                    $scope.title = data.name;
                    $scope.thumbnailUrl = data.thumbnailUrl;
                    $scope.description = data.description;
                }).
            error(function(data , status){
                $log.log(JSON.stringify(data));
                $rootScope.error = true;
                $rootScope.errors = data;
            });
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
    when('/friends', {
        templateUrl: 'static/js/partials/friends.html',
        controller: 'FriendsController'
    }).
    when('/wishlist', {
        templateUrl: 'static/js/partials/wishlist.html',
        controller: 'WishListController'
    }).
    when('/new' , {
        templateUrl: 'static/js/partials/new.html',
        controller: 'NewItemController'
    }).
    when('/item', {
        templateUrl: 'static/js/partials/item.html',
        controller: 'ItemController'
    }).
    when('/me' , {
        templateUrl: 'static/js/partials/wishlist.html',
        controller: 'WishListController'
    }).
    otherwise({
        redirectTo: '/login'
    });
});
