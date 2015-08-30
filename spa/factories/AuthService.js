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

    return authService;
});
