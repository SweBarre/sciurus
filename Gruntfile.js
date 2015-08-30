module.exports = function(grunt) {
    grunt.initConfig({
        copy: {
            js: {
                files: [
                    { src:'node_modules/bootstrap/dist/js/bootstrap.min.js', dest:'www-root/assets/js/bootstrap.min.js' },
                    { src:'node_modules/angular/angular.min.js', dest:'www-root/assets/js/angular.min.js' },
                    { src:'node_modules/angular-flash-alert/dist/angular-flash.min.js', dest:'www-root/assets/js/angular-flash.min.js' },
                    { src:'node_modules/angular-animate/angular-animate.min.js', dest:'www-root/assets/js/angular-animate.min.js' },
                    { src:'node_modules/ngstorage/ngStorage.min.js', dest:'www-root/assets/js/ngStorage.min.js' },
                    { src:'node_modules/angular-ui-bootstrap/ui-bootstrap-tpls.min.js', dest:'www-root/assets/js/ui-bootstrap-tpls.min.js' },
                    { src:'node_modules/angular-resource/angular-resource.min.js', dest:'www-root/assets/js/angular-resource.min.js' },
                    { src:'node_modules/angular-route/angular-route.min.js', dest:'www-root/assets/js/angular-route.min.js' }
                ]
            },
            css: {
                files: [
                    { src:'node_modules/bootstrap/dist/css/bootstrap.min.css', dest:'www-root/assets/css/bootstrap.min.css'},
                ]
            },
            fonts: {
                files: [
                    { expand: true, cwd:'node_modules/bootstrap/fonts/', src:['**'], dest:'www-root/assets/fonts/'}
                ]
            }
        },
        concat: {
            options: {
                seperator: ';'
            },
            sciurus: {
                src: ['spa/app.js','spa/config.js','spa/**/*.js'],
                dest: 'www-root/assets/js/sciurus.js'
            }
        }
    });

    grunt.loadNpmTasks('grunt-contrib-copy');
    grunt.loadNpmTasks('grunt-contrib-concat');
    grunt.registerTask('default', ['copy','concat']);
};
