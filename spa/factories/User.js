sciurus.factory('User', function($http, CONFIG, Session, Flash, $resource) {

    return $resource(CONFIG.apiURL+'users/:email', {id: '@email'}, 
        {
            'query': { method: 'GET', isArray: false },
            'put' : { method : 'PUT'}
    });

});
