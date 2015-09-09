sciurus.controller('ApplicationController', function ($scope, $rootScope, $location, AuthService, Session) {

    Session.load();

    $rootScope.currentUser = Session.user;
    $rootScope.isAuthorized = function(check, domain) {
        return AuthService.isAuthorized(check, domain);
    };

    $rootScope.setCurrentUser = function (user) {
        $rootScope.currentUser = user;
    };

    $scope.userMenu = [
        { caption: 'Dashboard', link: '#/' },
        { caption: 'Settings', link: '#/settings', },
        { caption: 'Quarantine', link: '#/quarantine' }
    ];


    $scope.adminMenu = [
        { caption: 'Domains', accsess: 'DOMAIN_READ', link: '#/' },
        { caption: 'Users', access: 'USERS_READ', link: '#/users' },
        { caption: 'New User', access: 'USERS_EDIT', link: '#/newuser' },
        { caption: 'Amavis', access: 'AMAVIS_READ', link: '#/' }
    ];

    $scope.filterKeyword = "";

    $scope.redirect = function(path) {
        console.log('redirecting: '+path);
        $location.path(path);
    };

    $scope.isActive = function(path) {
        var current = $location.path().substring(1).split('/')[0];
        return path === current ? "active" : "";
    };

    $scope.currentDomain = function() {
        if($location.path().substring(1).split('/')[0] == "domains") {
            return $location.path().substring(1).split('/')[1];
        }
        return false;
    };

});
