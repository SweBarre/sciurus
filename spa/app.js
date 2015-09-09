var sciurus = angular.module("sciurus", ['ngRoute', 'ngStorage', 'ui.bootstrap', 'flash', 'ngAnimate', 'ngResource']).

 config(function($routeProvider) {
    $routeProvider
    
    .when('/', {
        templateUrl : 'dashboard.html',
        controller  : 'DashboardCtrl'
    })
    
 .when('/quarantine', {
        templateUrl : 'quarantine.html',
        controller  : 'QuarantineCtrl'
    })

    .when('/login', {
        templateUrl : 'login.html',
        controller  : 'LoginCtrl'
    })

    .when('/logout', {
        templateUrl : 'login.html',
        controller  : 'LogoutCtrl'
    })

    .when('/users', {
        templateUrl : 'users.html',
        controller  : 'UsersCtrl'
    })

    .when('/newuser', {
        templateUrl : 'user.html',
        controller  : 'NewUserCtrl'
    })

    .when('/users/:userEmail', {
        templateUrl : 'user.html',
        controller  : 'UserDetailCtrl'
    })

    .when('/domains', {
        templateUrl : 'domains.html',
        controller  : 'DomainsCtrl'
    })
    
    .when('/domains/:domainName', {
        templateUrl : 'domains.html',
        controller  : 'DomainsCtrl'
    })
    
    .otherwise({
        redirectTo: '/'
    });
 }).
    
 run(function($rootScope, $location, AuthService, $http) {
    $rootScope.$on( "$routeChangeStart", function(event, next, current) {
        if (!AuthService.isAuthenticated()) {
            // User not authenticated
            if ( next.templateUrl === "login.html") {
            } else {
                $location.path("/login");
            }
        }
    });
    $http.defaults.headers.common['Accept']='application/json';
});
