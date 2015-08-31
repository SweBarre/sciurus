sciurus.controller('UsersCtrl', function($scope, User) {
    
    User.query(function(data){
        $scope.users = data.users;
    });

    $scope.orderBy = 'email';
    $scope.reverseOrder = false;

});
