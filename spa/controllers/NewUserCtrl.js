sciurus.controller('NewUserCtrl', function($scope, Flash, User, Domain) {

    $scope.user = {};
    $scope.domains = ['rre.nu', 'forsberg.co'];
    $scope.newUser = true;
    $scope.access = false;

    Domain.query(function(data) {
        $scope.domains = data.domains;
    });

    $scope.reset = function() {
            $scope.user = {};
            $scope.userForm.$setPristine();
    }

    $scope.save = function(){
        User.post($scope.user).
            $promise.then(function(response){
                Flash.create("success", "User "+user.email+" created");
            });
    }
    $scope.userChanged = function() {
        $scope.user.email = $scope.userID + '@' + $scope.userDomain;
    }

    $scope.setAccess= function (){
        console.log($scope.currentAdminDomain);
        if($scope.currentAdminDomain == "super") {
            $scope.access = $scope.user.super_admin;
        } else {
            $scope.access = $scope.user.admin[$scope.currentAdminDomain];
        }
    }
});
