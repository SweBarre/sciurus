sciurus.controller('DashboardCtrl', function($scope, Flash, Session) {
    $scope.accessRights = ["QUARANTINE_READ", 
                           "QUARANTINE_EDIT", 
                           "QUARANTINE_FULL", 
                           "AMAVIS_READ", 
                           "AMAVIS_EDIT", 
                           "AMAVIS_FULL", 
                           "USER_READ", 
                           "USER_EDIT", 
                           "USER_FULL", 
                           "DOMAIN_READ", 
                           "DOMAIN_EDIT", 
                           "DOMAIN_FULL"
                          ];
});
