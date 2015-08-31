sciurus.controller('UserDetailCtrl', function($scope ,$routeParams, AuthService, Flash, User) {

    var $initialUser = {};

    User.get({email:$routeParams.userEmail}, 
        function(data) {
            $initialUser = data.user;
            $scope.user = angular.copy($initialUser);
        },
        function(error){
            Flash.create('danger', error.status + ': ' + error.statusText);
        });

    $scope.reset = function() {
            $scope.user = angular.copy($initialUser);
            $scope.userForm.$setPristine();
    }

    $scope.save = function(){
        User.put({email:$scope.user.email}, $scope.user).
            $promise.then(function(response){
                $scope.userForm.$setPristine();
                $initialUser=response.user;
                $scope.user = angular.copy($initialUser);
            });
    }

});
