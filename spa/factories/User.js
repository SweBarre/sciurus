sciurus.factory('User', function($http, CONFIG, Session, Flash, $resource) {

    return $resource(CONFIG.apiURL+'users/:email', {}, 
        {
            'query': { method: 'GET', isArray: false },
            'put' : { method : 'PUT'},
            'get' : { method : 'GET'}
    });

});
