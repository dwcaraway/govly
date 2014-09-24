module.exports = function(grunt) {
    require('time-grunt')(grunt);
    require('load-grunt-tasks')(grunt);
 
    var spawn = require('child_process').spawn,
        appConfig = grunt.file.readJSON('package.json'),
        python_server;
 
    var pathsConfig = function (appName) {
        this.app = appName || appConfig.name;
 
        return {
            app: this.app,
            bower: this.app + '/bower_components',
            css: this.app + '/static/css',
            scss: this.app + '/static/sass',
            js: this.app + '/static/js',
            runScript: './run_' + this.app.toLowerCase() + '.sh'
        }
    };
 
    grunt.initConfig({
        paths: pathsConfig(),
        pkg: appConfig,
        sass: {
            options: {
                includePaths: ['<%= paths.bower %>']
            },
            dist: {
                options: {
                // outputStyle: 'compressed'
                },
                files: {
                    '<%= paths.css %>/styles.css': '<%= paths.scss %>/styles.scss'
                }
            }
        },
        requirejs: {
            dist: {
                // Options: https://github.com/jrburke/r.js/blob/master/build/example.build.js
                options: {
                    baseUrl: '<%= paths.js %>',
                    mainConfigFile: '<%= paths.js %>/main.js',
                    optimize: 'none',
                    preserveLicenseComments: false,
                    useStrict: true,
                    wrap: true,
                    name: 'main',
                    optimize: 'uglify2',
                    out: '<%= paths.js %>/main-built.js'
                }
            }
        },
        watch: {
            grunt: {
                files: ['Gruntfile.js']
            },
            sass: {
                files: '<%= paths.scss %>/**/*.scss',
                tasks: ['sass']
            }
        }
    });
 
    grunt.registerTask('runApp', function () {
        python_server = spawn(grunt.config.data.paths.runScript, [], {
            cwd: grunt.config.data.paths.app
        });
 
        python_server.stdout.on('data', function (data) {
          grunt.log.write('stdout: ' + data + '\n');
        });
 
        python_server.stderr.on('data', function (data) {
          grunt.log.write('stderr: ' + data + '\n');
        });
 
        python_server.on('close', function (code) {
          grunt.log.write('child process exited with code ' + code + '\n');
        });
    });
 
    grunt.registerTask('server', ['runApp', 'watch']);
 
    grunt.registerTask('build', ['sass', 'requirejs']);
    grunt.registerTask('default', ['build','watch']);
}
