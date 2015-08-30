sciurus.controller('UserInstanceCtrl', function($scope, $modalInstance, User, user) {
    
    $scope.user = user;
    $scope.modalUser = angular.copy($scope.user);
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
        User.put({email:$scope.modalUser.email}, $scope.modalUser).
         $promise.then(function(response){
             $scope.user=response.user;
             user = $scope.user;
             $scope.modalUser = angular.copy($scope.user);
             $modalInstance.close($scope.user);
         });
        $scope.editUser = false;
    };
});
