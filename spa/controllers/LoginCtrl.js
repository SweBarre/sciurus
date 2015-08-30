sciurus.controller('LoginCtrl', function($scope, $location, AuthService, Flash) {
    
    $scope.credentials = {
        email: '',
        password: ''
    };

    $scope.login = function(credentials) {
        AuthService.login(credentials).then(function(user) {
            $scope.setCurrentUser(user);
            Flash.create('success', 'Welcome '+user.email);
            $location.path("/");
        }, function(response){
            if (response.data) {
                Flash.create('danger', response.data.message);
            } else {
                Flash.create('danger', 'Unable to contact backend');
            }
        });
    };

});
