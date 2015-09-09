sciurus.controller('UserDetailCtrl', function($scope ,$routeParams, AuthService, Flash, User, Domain) {

    var $initialUser = {};

    $scope.changePassword = false;
    $scope.newPassword1 = '';
    $scope.newPassword2 = '';
    
    Domain.query(function(data) {
        $scope.domains = data.domains;
    });


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

    $scope.disablePasswordSave = function() {
        if($scope.passForm.$pristine){
            return true;
        }
        if($scope.newPassword1 == '' || $scope.newPassword2 == ''){
            return true;
        }
        if($scope.newPassword1 == $scope.newPassword2) {
            return false;
        }
        return true;
    }

    $scope.updatePassword = function() {
        data = { 'oldPassword': $scope.oldPassword,
                 'newPassword': $scope.newPassword1 };
        User.post({email:$scope.user.email, action:'password'}, data).
            $promise.then(function(response) {
                $scope.oldPassword='';
                $scope.newPassword1='';
                $scope.newPassword2='';
                $scope.changePassword = false;
                Flash.create('success', 'Password updated');


            },function(data){
                Flash.create('danger', data.status + ': ', data.statusText)
            });
    }

});
