sciurus.controller('ApplicationController', function ($scope, $rootScope, $location, Session) {

    Session.load();

    $rootScope.currentUser = Session.user;

    $rootScope.setCurrentUser = function (user) {
        $rootScope.currentUser = user;
    };

    $scope.userMenu = [
        { caption: 'Dashboard', link: '#/' },
        { caption: 'Settings', link: '#/settings', },
        { caption: 'Quarantine', link: '#/quarantine' }
    ];


    $scope.adminMenu = [
        { caption: 'Domains', link: '#/' },
        { caption: 'Users', link: '#/users', },
        { caption: 'Amavis', link: '#/' }
    ];

    $scope.filterKeyword = "";

});
