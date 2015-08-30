sciurus.controller('UserInstanceCtrl', function($scope, $modalInstance, User, user) {
    
    $scope.user = user;
    $scope.currentAdminDomain = false;
    $scope.editUser = false;

    $scope.ok = function() {
        $modalInstance.close($scope.user);
    };

    $scope.cancel = function() {
        $modalInstance.dismiss("cancel");
    };

    $scope.edit = function() {
        $scope.editUser = true;
    };

    $scope.save = function() {
        User.put({email:$scope.user.email}, $scope.user).
         $promise.then(function(response){
             $scope.user=response.user;
             $modalInstance.close($scope.user);
         });
        $scope.editUser = false;
    };
});
