sciurus.factory('Domain', function(CONFIG, $resource) {

    return $resource(CONFIG.apiURL+'domains/:name', {}, 
        {
            'query': { method: 'GET', isArray: false },
            'put' : { method : 'PUT'},
            'get' : { method : 'GET'},
            'post': { method : 'POST'}
    });

});
