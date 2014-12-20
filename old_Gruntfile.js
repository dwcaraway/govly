'use strict';

var proxySnippet = require('grunt-connect-proxy/lib/utils').proxyRequest;

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
    yeoman: {
      // configurable paths
      app: require('./bower.json').appPath || 'frontend',
      dist: 'dist'
    },
//    sync: {
//      main: {
//        files: [{
//          cwd: '<%= yeoman.app %>',
//          dest: '<%= yeoman.dist %>',
//          src: ['**', '!dist', '!*.md']
//        }],
//         verbose: true
//
//      }
//    },
    open: {
      server: {
        url: 'http://localhost:8000'
      }
    },
    watch: {
      js: {
        files: ['<%= yeoman.app %>/js/{,*/}*.js'],
        tasks: ['newer:jshint:all'],
        options: {
          livereload: true
        }
      },
      jsTest: {
        files: ['test/client/spec/{,*/}*.js'],
        tasks: ['newer:jshint:test', 'karma']
      },
      compass: {
        files: ['<%= yeoman.app %>/styles/{,*/}*.{scss,sass}'],
        tasks: ['compass:server', 'autoprefixer']
      },
      gruntfile: {
        files: ['Gruntfile.js']
      },
      livereload: {
        files: [
          '<%= yeoman.app %>/views/{,*//*}*.{html,jade}',
          '{.tmp,<%= yeoman.app %>}/styles/{,*//*}*.css',
          '{.tmp,<%= yeoman.app %>}/js/{,*//*}*.js',
          '<%= yeoman.app %>/images/{,*//*}*.{png,jpg,jpeg,gif,webp,svg}'
        ],

        options: {
          livereload: true
        }
      }
    },
    connect: {
        example: {
            port: 1337,
            base: '<%=yeoman.dist %>'
        },
      server: {
        options: {
          port: 8000,
          // Change this to '0.0.0.0' to access the server from outside.
          hostname: 'localhost',
            base:
            '<%= yeoman.dist %>'

        },
        livereload: {
          options: {
            open: true,
            base:
              '<%= yeoman.dist %>'
          }
        }
      }
    },
    // Make sure code styles are up to par and there are no obvious mistakes
    jshint: {
      options: {
        jshintrc: '.jshintrc',
        reporter: require('jshint-stylish')
      },
      all: [
        '<%= yeoman.app %>/js/{,*/}*.js'
      ],
      test: {
        options: {
          jshintrc: 'tests/client/.jshintrc'
        },
        src: ['tests/client/spec/{,*/}*.js']
      }
    },

      bower: {
          install: {
              options: {
//                  targetDir: '<%= yeoman.dist %>/libs',
                  layout: 'byType',
                  install: true,
                  verbose: false,
                  cleanTargetDir: false,
                  cleanBowerDir: false,
                  bowerOptions: {}
              }
          }
      },

    // Empties folders to start fresh
    clean: {
      dist: {
        files: [{
          dot: true,
          src: [
            '.tmp',
            '<%= yeoman.dist %>/*',
            '!<%= yeoman.dist %>/.git*'
          ]
        }]
      },
      server: '.tmp'

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

     // By default, your `index.html`'s <!-- Usemin block --> will take care of
    // minification. These next options are pre-configured if you do not wish
    // to use the Usemin blocks.
     cssmin: {
       dist: {
//         files: {
//           '<%= yeoman.dist %>/styles/main.css': [
//             '.tmp/styles/{,*/}*.css',
//             '<%= yeoman.app %>/assets/styles/{,*/}*.css'
//           ]
//         }
       }
     },
     uglify: {
       dist: {
//         files: {
//           '<%= yeoman.dist %>/scripts/scripts.js': [
//             '<%= yeoman.app %>/assets/js/*.js'
//           ]
//         }
       }
     },
     concat: {
       dist: {}
     },

    // Automatically inject Bower components into the app
      'wiredep': {
          task: {
              // Point to the files that should be updated when
              // you run `grunt wiredep`
              src: [
                  '<%= yeoman.dist %>/index.html'
              ],

              options: {
//                  directory: 'dist/libs'
              }


          }
      },

    // Compiles Sass to CSS and generates necessary files if requested
    compass: {
      options: {
        sassDir: '<%= yeoman.app %>/assets/styles',
        cssDir: '<%= yeoman.app %>/assets/styles',
        generatedImagesDir: '.tmp/images/generated',
        imagesDir: '<%= yeoman.app %>/assets/img',
        javascriptsDir: '<%= yeoman.dist %>/js',
        fontsDir: '<%= yeoman.app %>/assets/fonts',
        httpImagesPath: '/images',
        httpGeneratedImagesPath: '/images/generated',
        httpFontsPath: '/styles/fonts',
        relativeAssets: false,
        assetCacheBuster: false,
        raw: 'Sass::Script::Number.precision = 10\n'
      },
      dist: {
        options: {
          generatedImagesDir: '<%= yeoman.dist %>/public/images/generated'
        }
      },
      server: {
        options: {
          debugInfo: true
        }
      }
    },

    // Renames files for browser caching purposes
    rev: {
      dist: {
        files: {
          src: [
            '<%= yeoman.dist %>/public/scripts/{,*/}*.js',
            '<%= yeoman.dist %>/public/styles/{,*/}*.css',
            '<%= yeoman.dist %>/public/images/{,*/}*.{png,jpg,jpeg,gif,webp,svg}',
            '<%= yeoman.dist %>/public/styles/fonts/*'
          ]
        }
      }
    },

    // Reads HTML for usemin blocks to enable smart builds that automatically
    // concat, minify and revision files. Creates configurations in memory so
    // additional tasks can operate on them
    useminPrepare: {
      html: ['frontend/app/index.html'],
      options: {
        dest: '<%= yeoman.dist %>/public'
      }
    },

    // Performs rewrites based on rev and the useminPrepare configuration
    usemin: {
      html: ['<%= yeoman.dist %>/templates/{,*/}*.html',
             '<%= yeoman.dist %>/templates/{,*/}*.jade'],
      css: ['<%= yeoman.dist %>/public/styles/{,*/}*.css'],
      options: {
        assetsDirs: ['<%= yeoman.dist %>/public']
      }
    },

    // The following *-min tasks produce minified files in the dist folder
    imagemin: {
      options : {
        cache: false
      },
      dist: {
        files: [{
          expand: true,
          cwd: '<%= yeoman.app %>/images',
          src: '{,*/}*.{png,jpg,jpeg,gif}',
          dest: '<%= yeoman.dist %>/public/images'
        }]
      }
    },

    svgmin: {
      dist: {
        files: [{
          expand: true,
          cwd: '<%= yeoman.app %>/images',
          src: '{,*/}*.svg',
          dest: '<%= yeoman.dist %>/public/images'
        }]
      }
    },

    htmlmin: {
      dist: {
        options: {
          //collapseWhitespace: true,
          //collapseBooleanAttributes: true,
          //removeCommentsFromCDATA: true,
          //removeOptionalTags: true
        },
        files: [{
          expand: true,
          cwd: '<%= yeoman.app %>/views',
          src: ['*.html', 'partials/**/*.html'],
          dest: '<%= yeoman.dist %>/views'
        }]
      }
    },

    // Allow the use of non-minsafe AngularJS files. Automatically makes it
    // minsafe compatible so Uglify does not destroy the ng references
//    ngmin: {
//      dist: {
//        files: [{
//          expand: true,
//          cwd: '.tmp/concat/scripts',
//          src: '*.js',
//          dest: '.tmp/concat/scripts'
//        }]
//      }
//    },

    // Copies remaining files to places other tasks can use
    copy: {
      dist: {
        files: [{
          expand: true,
          dot: true,
          cwd: '<%= yeoman.app %>/',
          dest: '<%= yeoman.dist %>/',
          src: [
            'assets/**/*',
              '*.html'
          ]
        },{
            expand: true,
            flatten: true,
            cwd: '<%= yeoman.app %>/app/',
            dest: '<%= yeoman.dist %>/js/',
            src: [
            '**/*.js'
            ]
        }
//            ,{
//          expand: true,
//          cwd: '.tmp/images',
//          dest: '<%= yeoman.dist %>/public/images',
//          src: ['generated/*']
//        }
        ]
      },
      styles: {
        expand: true,
        cwd: '<%= yeoman.app %>/styles',
        dest: '.tmp/styles/',
        src: '{,*/}*.css'
      }
    },

    // Run some tasks in parallel to speed up the build process
    concurrent: {
      server: [
        'compass:server'
      ],
      debug: {
        options: {
          logConcurrentOutput: true
        }
      },
      dist: [
        'compass:dist',
        'imagemin',
        'svgmin',
        'htmlmin'
      ]
    },

    // Test settings
    karma: {
      unit: {
        configFile: 'karma.conf.js',
        singleRun: true 
      }
    }
  });

  // Used for delaying livereload until after server has restarted
  grunt.registerTask('wait', function () {
    grunt.log.ok('Waiting for server reload...');

    var done = this.async();

    setTimeout(function () {
      grunt.log.writeln('Done waiting!');
      done();
    }, 500);
  });

  grunt.registerTask('flask', 'Run flask server.', function() {
    var spawn = require('child_process').spawn;
    grunt.log.writeln('Starting Flask development server.');
    // stdio: 'inherit' let us see flask output in grunt
    var PIPE = {stdio: 'inherit'};
    spawn('python', ['manage.py', 'runserver'], PIPE);
    
    spawn.on('close', function (code) {
      grunt.log.write('child process exited with code ' + code + '\n');
    });

  });

  grunt.registerTask('serve', function (target) {
    grunt.task.run([
      'clean:server',
      'load-dep',
      'concurrent:server',
      'autoprefixer',
//      'configureProxies:server',
      'connect:server',
      'watch'
//      'flask'
    ]);
  });

    grunt.registerTask('test', function (target) {
        return grunt.task.run([
            'clean:server',
            'autoprefixer',
            'karma'
        ]);
    });

  //run `bower install` and then update the html to reflect the dependencies
  grunt.registerTask('load-dep', [
  'bower:install',
      'wiredep'
  ]);

  grunt.registerTask('build', [
    'clean:dist',
//    'useminPrepare',
//    'concurrent:dist',
//    'autoprefixer',
//    'concat',
//    'ngmin',
    'copy:dist',
//    'cssmin',
//    'uglify',
//    'rev',
//    'usemin'
    'load-dep'
  ]);

  grunt.registerTask('default', [
    'newer:jshint',
    'build'
//    'test'
  ]);
};
