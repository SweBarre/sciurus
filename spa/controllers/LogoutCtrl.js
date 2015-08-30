sciurus.controller('LogoutCtrl', function($scope, $rootScope, $location, Session, Flash) {
    var email = $rootScope.currentUser.email;
    $rootScope.currentUser = null;
    Session.destroy()
    Flash.create('success', 'Logging out '+email);
    $location.path("/");
});
