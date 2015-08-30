sciurus.controller('UsersCtrl', function($scope, $modal, User) {
    
    User.query(function(data){
        $scope.users = data.users;
    });

    $scope.orderBy = 'email';
    $scope.reverseOrder = false;
    $scope.selectedUser = false;



    $scope.viewUser = function(user) {
        user = user;

        $modalInstance = $modal.open({
            animation: true,
            backdrop: true,
            templateUrl: "partials/userModal.html",
            controller: "UserInstanceCtrl",
            size: '',
            resolve: {
                user: function() {
                    return user;
                }
            }
        });

        $modalInstance.result.then(function(changedUser) {
            user = angular.copy(changedUser);
            console.log(changedUser);
        });
    }

});
