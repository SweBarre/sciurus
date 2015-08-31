sciurus.factory('AuthService', function($http, Session, CONFIG, Flash) {

    var authService = {};

    authService.login = function(credentials) {
        return $http.post(CONFIG.apiURL+'login', credentials)
               .then(function(response) {
                   Session.create(response.data.user, response.data.token);
                   return response.data.user;
               });
    };

    authService.isAuthenticated = function() {
        return !!Session.token;
    };

    authService.isAuthorized = function(check, domain) {
        var access_object = check.split("_")[0];
        var access_right = check.split("_")[1];

        //check if user has super_admin
        if(angular.isArray(Session.user.super_admin)) {
            if(Session.user.super_admin.indexOf(check) > -1) {
                return true;
            }
            if(access_right == "READ") {
                if(Session.user.super_admin.indexOf(access_object+'_EDIT') > -1){
                    return true;
                } else if (Session.user.super_admin.indexOf(access_object+'_FULL') > -1){
                    return true;
                }
            }
            if(access_right == "EDIT") {
                if(Session.user.super_admin.indexOf(access_object+'_FULL') > -1){
                    return true;
                }
            }
        }
        // check if user has domain access
        if(angular.isArray(Session.user.admin[domain])){
            if(Session.user.admin[domain].indexOf(check) > -1) {
                return true;
            }
            if(access_right == "READ") {
                if(Session.user.admin[domain].indexOf(access_object+'_EDIT') > -1){
                    return true;
                } else if (Session.user.admin[domain].indexOf(access_object+'_FULL') > -1){
                    return true;
                }
            }
            if(access_right == "EDIT") {
                if(Session.user.admin[domain].indexOf(access_object+'_FULL') > -1){
                    return true;
                }
            }
        }
        return false;
    };

    return authService;
});
