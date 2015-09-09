sciurus.service('Session', function ($sessionStorage, $http, CONFIG) {

    this.create = function (user, token) {
        this.token = token;
        this.user = user;
        this.user.token = token;
        $sessionStorage.token = token;
        $sessionStorage.user = user;
        $http.defaults.headers.common['X-Auth-Token'] = token;

        this.app = $http.get(CONFIG.apiURL+'app')
                        .then(function(response) {
                            return response.data;
                        });
        console.log(this.app);
    };
    
    this.destroy = function () {
        this.token = null;
        this.user = null;
        $sessionStorage.$reset();
        delete $http.defaults.headers.common['X-Auth-Token'];
    };

    this.load = function() {
        console.log("loading session data");
        this.token = $sessionStorage.token;
        this.user = $sessionStorage.user;
        if(typeof this.token === 'undefined') {
            this.token = null;
            this.user = null;
        }
        if(typeof this.user === 'undefined') {
            this.token = null;
            this.user = null;
        }


        if(this.token) {
            console.log(this.user.email+':'+this.token);
            $http.defaults.headers.common['X-Auth-Token'] = this.token;
            this.app = $http.get(CONFIG.apiURL+'app')
                        .then(function(response) {
                            return response.data;
                        });
        }
    };

});
