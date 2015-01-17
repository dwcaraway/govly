// Generated on 2014-12-20 using generator-angular 0.10.0
'use strict';

// # Globbing
// for performance reasons we're only matching one level down:
// 'test/spec/{,*/}*.js'
// use this if you want to recursively match all subfolders:
// 'test/spec/**/*.js'

module.exports = function (grunt) {

    // Load grunt tasks automatically
    require('load-grunt-tasks')(grunt);

    // Time how long tasks take. Can help when optimizing build times
    require('time-grunt')(grunt);

    // Define the configuration for all the tasks
    grunt.initConfig({

        // Project settings
        appConfig: {
        app: require('./bower.json').appPath || 'frontend',
        dist: 'dist',
        temp: '.tmp',
        test: './tests/client'
        },

        html2js: {
            /**
             * These are the templates from `src/app`.
             */
            app: {
                options: {
                    base: '<%= appConfig.app %>'
                },
                src: ['**/*.tpl.html'],
                dest: '<%= appConfig.dist %>/templates-app.js'
            }
        },

        less: {
            all: {
                src: '<%= appConfig.app %>/styles/style.less',
                dest: '<%= appConfig.dist %>/styles/style.css',
                options: {
                    report: 'gzip'
                }
            }
        },

        concat_sourcemap: {
            options: {
                sourcesContent: true
            },
            app: {
                src: ['src/**/*.js', 'src/*.js'],
                dest: 'build/app.js'
            },
            libs: {
                src: [
                    'libs/angular/angular.js',
                    'libs/angular-animate/angular-animate.js',
                    'libs/angular-mocks/angular-mocks.js',
                    'libs/angular-ui-router/release/angular-ui-router.js'
                ],
                dest: 'build/libs.js'
            }
        },

        // Watches files for changes and runs tasks based on the changed files
        watch: {
            bower: {
                files: ['bower.json'],
                //tasks: ['wiredep']
                tasks: ['bower_concat']
            },
            templates: {
                files: ['<%= appConfig.app %>/**/*.tpl.html'],
                tasks: ['html2js']
            },
            less: {
                files: ['<%= appConfig.app=>/styles/style.less', '<%= appConfig.app =>/**/*.less'],
                tasks: ['less']
            },
            js: {
                files: ['<%= appConfig.app %>/scripts/{,*/}*.js'],
                tasks: ['newer:jshint:all'],
                options: {
                    livereload: '<%= connect.options.livereload %>'
                }
            },
            jsTest: {
                files: ['<%=appConfig.test%>/spec/{,*/}*.js'],
                tasks: ['newer:jshint:test', 'karma']
            },
            gruntfile: {
                files: ['Gruntfile.js']
            },
            livereload: {
                options: {
                    livereload: '<%= connect.options.livereload %>'
                },
                files: [
                    '<%= appConfig.app %>/{,*/}*.html',
                    '<%= appConfig.dist %>/templates-app.js',
                    '<%= appConfig.app %>/images/{,*/}*.{png,jpg,jpeg,gif,webp,svg}'
                ]
            }
        },

        // The actual grunt server settings
        connect: {
            options: {
                port: 9000,
                // Change this to '0.0.0.0' to access the server from outside.
                hostname: 'localhost',
                livereload: 35729
            },
            livereload: {
                options: {
                    open: true,
                    middleware: function (connect) {
                        return [
                            connect.static('.tmp'),
                            connect().use(
                                '/bower_components',
                                connect.static('./bower_components')
                            ),
                            connect.static('<%= appConfig.app %>')
                        ];
                    }
                }
            },
            test: {
                options: {
                    port: 9001,
                    middleware: function (connect) {
                        return [
                            connect.static('.tmp'),
                            connect.static('test'),
                            connect().use(
                                '/bower_components',
                                connect.static('./bower_components')
                            ),
                            connect.static('<%= appConfig.app %>')
                        ];
                    }
                }
            },
            dist: {
                options: {
                    open: true,
                    base: '<%= appConfig.dist %>'
                }
            }
        },

        // Make sure code styles are up to par and there are no obvious mistakes
        jshint: {
            options: {
                jshintrc: '.jshintrc',
                reporter: require('jshint-stylish')
            },
            all: {
                src: [
                    'Gruntfile.js',
                    '<%= appConfig.app %>/scripts/{,*/}*.js'
                ]
            },
            test: {
                options: {
                    jshintrc: '<%=appConfig.test%>/.jshintrc'
                },
                src: ['<%appConfig.test%>/spec/{,*/}*.js']
            }
        },

        // Empties folders to start fresh
        clean: {
            dist: {
                files: [{
                    dot: true,
                    src: [
                        '.tmp',
                        '<%= appConfig.dist %>/{,*/}*',
                        '!<%= appConfig.dist %>/.git{,*/}*'
                    ]
                }]
            }
        },

        // Add vendor prefixed styles
        autoprefixer: {
            options: {
                browsers: ['last 1 version']
            },
            dist: {
                files: [{
                    expand: true,
                    cwd: '.tmp/styles/',
                    src: '{,*/}*.css',
                    dest: '.tmp/styles/'
                }]
            }
        },

        // Automatically inject Bower components into the app
        wiredep: {
            app: {
                src: ['<%= appConfig.app %>/index.html'],
                ignorePath: /\.\.\//
            },
            test: {
                src: 'tests/client/karma.conf.js',
                ignorePath: /\.\.\/\.\.\//,
                fileTypes: {
                    js: {
                        block: /(([\s\t]*)\/\/\s*bower:*(\S*))(\n|\r|.)*?(\/\/\s*endbower)/gi,
                        detect: {
                            js: /'(.*\.js)'/gi
                        },
                        replace: {
                            js: '\'{{filePath}}\','
                        }
                    }
                }
            }
        },

        bower_concat: {
            all: {
                dest: '<%= appConfig.dist %>/scripts/_bower.js',
                cssDest: '<%= appConfig.dist %>/styles/_bower.css',
                exclude: ['es5-shim', 'json3'],
                mainFiles: {
                    'angulartics': 'dist/angulartics-ga.min.js'
                }
            }
        },

        replace: {
            production: {
                src: ['<%= appConfig.dist %>/index.html'],   // source files array (supports minimatch)
                dest: '<%= appConfig.dist %>/',             // destination directory or file
                replacements: [
                    {
                        from: 'UA-XXXXXXXX-X',
                        to: 'UA-37455300-1'
                    }
                ]
            }
        },

        // Renames files for browser caching purposes
        filerev: {
            dist: {
                src: [
                    '<%= appConfig.dist %>/scripts/{,*/}*.js',
                    '<%= appConfig.dist %>/styles/{,*/}*.css',
                    '<%= appConfig.dist %>/images/{,*/}*.{png,jpg,jpeg,gif,webp,svg}',
                    '<%= appConfig.dist %>/styles/fonts/*'
                ]
            }
        },

        // Reads HTML for usemin blocks to enable smart builds that automatically
        // concat, minify and revision files. Creates configurations in memory so
        // additional tasks can operate on them
        useminPrepare: {
            html: '<%= appConfig.app %>/index.html',
            options: {
                dest: '<%= appConfig.dist %>',
                flow: {
                    html: {
                        steps: {
                            js: ['concat', 'uglifyjs'],
                            css: ['cssmin']
                        },
                        post: {}
                    }
                }
            }
        },

        // Performs rewrites based on filerev and the useminPrepare configuration
        usemin: {
            html: ['<%= appConfig.dist %>/{,*/}*.html'],
            css: ['<%= appConfig.dist %>/styles/{,*/}*.css'],
            options: {
                assetsDirs: ['<%= appConfig.dist %>', '<%= appConfig.dist %>/images']
            }
        },

        // The following *-min tasks will produce minified files in the dist folder
        // By default, your `index.html`'s <!-- Usemin block --> will take care of
        // minification. These next options are pre-configured if you do not wish
        // to use the Usemin blocks.
        // cssmin: {
        //   dist: {
        //     files: {
        //       '<%= appConfig.dist %>/styles/main.css': [
        //         '.tmp/styles/{,*/}*.css'
        //       ]
        //     }
        //   }
        // },
        // uglify: {
        //   dist: {
        //     files: {
        //       '<%= appConfig.dist %>/scripts/scripts.js': [
        //         '<%= appConfig.dist %>/scripts/scripts.js'
        //       ]
        //     }
        //   }
        // },
        // concat: {
        //   dist: {}
        // },

        imagemin: {
            dist: {
                files: [{
                    expand: true,
                    cwd: '<%= appConfig.app %>/images',
                    src: '{,*/}*.{png,jpg,jpeg,gif}',
                    dest: '<%= appConfig.dist %>/images'
                }]
            }
        },

        svgmin: {
            dist: {
                files: [{
                    expand: true,
                    cwd: '<%= appConfig.app %>/images',
                    src: '{,*/}*.svg',
                    dest: '<%= appConfig.dist %>/images'
                }]
            }
        },

        htmlmin: {
            dist: {
                options: {
                    collapseWhitespace: true,
                    conservativeCollapse: true,
                    collapseBooleanAttributes: true,
                    removeCommentsFromCDATA: true,
                    removeOptionalTags: true
                },
                files: [{
                    expand: true,
                    cwd: '<%= appConfig.dist %>',
                    src: ['*.html', 'views/{,*/}*.html'],
                    dest: '<%= appConfig.dist %>'
                }]
            }
        },

        // ng-annotate tries to make the code safe for minification automatically
        // by using the Angular long form for dependency injection.
        ngAnnotate: {
            dist: {
                files: [{
                    expand: true,
                    cwd: '.tmp/concat/scripts',
                    src: ['*.js', '!oldieshim.js'],
                    dest: '.tmp/concat/scripts'
                }]
            }
        },

        // Copies remaining files to places other tasks can use
        copy: {
            dist: {
                files: [{
                    expand: true,
                    dot: true,
                    cwd: '<%= appConfig.app %>',
                    dest: '<%= appConfig.dist %>',
                    src: [
                        '*.{ico,png,txt}',
                        '*.html',
                        //'views/{,*/}*.html',
                        'images/{,*/}*.{webp}',
                        'fonts/{,*/}*.*'
                    ]
                }, {
                    expand: true,
                    cwd: '.tmp/images',
                    dest: '<%= appConfig.dist %>/images',
                    src: ['generated/*']
                },
                    {
                        expand: true,
                        cwd: 'bower_components/font-awesome',
                        src: 'fonts/*',
                        dest: '<%= appConfig.dist %>'
                    }]
            }
        },

        // Run some tasks in parallel to speed up the build process
        concurrent: {
            server:[
                'less',
                'html2js',
                'ngconstant:development',
                'bower_concat'
            ],
            dist: [
                'ngconstant:production',
                'less',
                'imagemin',
                'svgmin',
                'bower_concat'
            ]
        },

        // Test settings
        karma: {
            unit: {
                configFile: '<%=appConfig.test%>/karma.conf.js',
                singleRun: true
            }
        },

        // SauceLabs testing for running multiple concurrent tests
        sauce_connect: {
            your_target: {
                // Target-specific file lists and/or options go here.
                options: {
                    username: process.env.SAUCE_USER,
                    accessKey: process.env.SAUCE_API_KEY
                }
            }
        },

        ngconstant: {
            // Options for all targets
            options: {
                space: '  ',
                wrap: '"use strict";\n\n {%= __ngModule %}',
                name: 'config'
            },
            // Environment targets
            development: {
                options: {
                    dest: '<%= appConfig.app %>/scripts/config.js'
                },
                constants: {
                    ENV: {
                        name: 'development',
                        apiEndpoint: 'http://localhost:5000'
                    }
                }
            },
            production: {
                options: {
                    dest: '<%= appConfig.app %>/scripts/config.js'
                },
                constants: {
                    ENV: {
                        name: 'production',
                        apiEndpoint: 'https://api.fogmine.com'
                    }
                }
            }
        },

        protractor_webdriver: {
            e2eUpdate: {
                options: {
                    path: './node_modules/.bin/',
                    command: 'webdriver-manager update --standalone'
                }
            },
            e2eStart: {
                options: {
                    path: './node_modules/.bin/',
                    command: 'webdriver-manager start'
                }
            }
        },

        protractor: {
            options: {
                keepAlive: true,
                configFile: 'tests/client/protractor.conf.js'
            },
            run: {}
        }
    });


    grunt.registerTask('serve', 'Compile then start a connect web server', function (target) {
        if (target === 'dist') {
            return grunt.task.run(['build', 'connect:dist:keepalive']);
        }

        grunt.task.run([
            'clean',
            'concurrent:server',
            'copy',
            'autoprefixer',
            'connect:livereload',
            'watch'
        ]);
    });

    grunt.registerTask('test', 'Run unit or end-to-end tests', function (target) {
        if (target === 'pre') {
            return grunt.task.run([
                'clean',
                'ngconstant:development'
            ]);
        }
        if (target === 'e2e') {
            return grunt.task.run([
                'test:pre',
                'autoprefixer',
                'protractor_webdriver:e2eStart',
                'protractor:run'
            ]);
        } else if (target === 'all') {
            return grunt.task.run(['test:e2e', 'connect:test', 'karma']);
        }

        grunt.task.run([
            'test:pre',
            'connect:test',
            'karma'
        ]);

    });

    grunt.registerTask('test-sauce', [
        'sauce_connect:your_target',
        'test:all',
        'sauce-connect-close'
    ]);

    grunt.registerTask('pre-deploy', [
        'ngconstant:production',
        'replace:production'
    ]);

    grunt.registerTask('build', [
        'clean',
        'useminPrepare',
        'concurrent:dist',
        'autoprefixer',
        'concat',
        'ngAnnotate',
        'copy',
        'cssmin',
        'uglify',
        'filerev',
        'usemin',
        'htmlmin'
    ]);

    grunt.registerTask('default', [
        'newer:jshint',
        'test',
        'build'
    ]);

    grunt.registerTask('foo', ['clean', 'concat_sourcemap:libs', 'connect', 'watch']);
};
