var gulp        = require('gulp'),
    concat      = require('gulp-concat'),
    uglify      = require('gulp-uglify'),
    jade        = require('gulp-jade'),
    less        = require('gulp-less'),
    path        = require('path'),
    livereload  = require('gulp-livereload'), // Livereload plugin needed: https://chrome.google.com/webstore/detail/livereload/jnihajbhpnppcggbcgedagnkighmdlei
    marked      = require('marked'), // For :markdown filter in jade
    path        = require('path'),
    changed     = require('gulp-changed'),
    prettify    = require('gulp-html-prettify'),
    w3cjs       = require('gulp-w3cjs'),
    rename      = require('gulp-rename'),
    flip        = require('css-flip'),
    through     = require('through2'),
    gutil       = require('gulp-util'),
    htmlify     = require('gulp-angular-htmlify'),
    PluginError = gutil.PluginError;

// LiveReload port. Change it only if there's a conflict
var lvr_port = 35729;

var W3C_OPTIONS = {
  // Set here your local validator if your using one. leave it empty if not
  //uri: 'http://validator/check',
  doctype: 'HTML5',
  output: 'json',
  // Remove some messages that angular will always display.
  filter: function(message) {
    if( /Element head is missing a required instance of child element title/.test(message) )
      return false;
    if( /Attribute .+ not allowed on element .+ at this point/.test(message) )
      return false;
    if( /Element .+ not allowed as child of element .+ in this context/.test(message) )
      return false;
    if(/Comments seen before doctype./.test(message))
      return false;
  }
};

// ignore everything that begins with underscore
var hidden_files = '**/_*.*';
var ignored_files = '!'+hidden_files;

//  Edit here the scripts that will be included statically
//  in the app. Compiles to vendor/base.js
var vendorBaseScripts = [
  // jQuery
  '../vendor/jquery/jquery.min.js',
  // Angular
  '../vendor/angular/angular.min.js',
  '../vendor/angular/angular-route.min.js',
  '../vendor/angular/angular-cookies.js',
  '../vendor/angular/angular-animate.min.js',
  '../vendor/angular/angular-ui-router.js',
  '../vendor/angular/angular-sanitize.min.js',
  '../vendor/angular/angular-resource.js',
  // '../vendor/angular/angular-touch.js',
  // Angular storage
  '../vendor/angularstorage/ngStorage.js',
  // Angular Translate
  '../vendor/angulartranslate/angular-translate.js',
  '../vendor/angulartranslate/angular-translate-loader-url.js',
  '../vendor/angulartranslate/angular-translate-loader-static-files.js',
  '../vendor/angulartranslate/angular-translate-storage-local.js',
  '../vendor/angulartranslate/angular-translate-storage-cookie.js',
  // oclazyload
  '../vendor/oclazyload/ocLazyLoad.min.js',
  // UI Bootstrap
  '../vendor/bootstrap/js/ui-bootstrap-tpls-0.12.0.min.js',
  // Loading Bar
  '../vendor/loadingbar/loading-bar.js'
];

// SOURCES CONFIG 
var source = {
  scripts: {
    app:    [ 'js/app.init.js',
              'js/modules/*.js',
              'js/modules/controllers/*.js',
              'js/modules/directives/*.js',
              'js/modules/services/*.js',
              'js/modules/filters/*.js',
              'js/custom/**/*.js',
              ignored_files
            ],
    vendor: vendorBaseScripts,
    watch: ['js/**/*.js']
  },
  templates: {
    app: {
        files : ['jade/index.jade'],
        watch: ['jade/index.jade', hidden_files]
    },
    views: {
        files : ['jade/views/*.jade', 'jade/views/**/*.jade', ignored_files],
        watch: ['jade/views/**/*.jade']
    },
    pages: {
        files : ['jade/pages/*.jade'],
        watch: ['jade/pages/*.jade']
    }
  },
  styles: {
    app: {
      main: ['less/app.less', '!less/themes/*.less'],
      dir:  'less',
      watch: ['less/*.less', 'less/**/*.less', '!less/themes/*.less']
    },
    themes: {
      main: ['less/themes/*.less', ignored_files],
      dir:  'less/themes',
      watch: ['less/themes/*.less']
    },
  },
  bootstrap: {
    main: 'less/bootstrap/bootstrap.less',
    dir:  'less/bootstrap',
    watch: ['less/bootstrap/*.less']
  }
};

// BUILD TARGET CONFIG 
var build = {
  scripts: {
    app: {
      main: 'app.js',
      dir: '../app/js'
    },
    vendor: {
      main: 'base.js',
      dir: '../app/js'
    }
  },
  styles: '../app/css',
  templates: {
    app: '..',
    views: '../app/views',
    pages: '../app/pages'
  }
};

//---------------
// TASKS
//---------------


// JS APP
gulp.task('scripts:app', function() {
    // Minify and copy all JavaScript (except vendor scripts)
    return gulp.src(source.scripts.app)
        //.pipe(uglify())  /* UNCOMMENT TO MINIFY * /
        .pipe(concat(build.scripts.app.main))
        .pipe(gulp.dest(build.scripts.app.dir));
});

// JS APP
gulp.task('scripts:vendor', function() {
    // Minify and copy all JavaScript (except vendor scripts)
    return gulp.src(source.scripts.vendor)
        .pipe(uglify())  /* UNCOMMENT TO MINIFY */
        .pipe(concat(build.scripts.vendor.main))
        .pipe(gulp.dest(build.scripts.vendor.dir))
        ;
});

// APP LESS
gulp.task('styles:app', function() {
    return gulp.src(source.styles.app.main)
        .pipe(less({
            paths: [source.styles.app.dir]
        }))
        .on("error", handleError)
        .pipe(gulp.dest(build.styles));
});

// APP RTL
gulp.task('styles:app:rtl', function() {
    return gulp.src(source.styles.app.main)
        .pipe(less({
            paths: [source.styles.app.dir]
        }))
        .on("error", handleError)
        .pipe(flipcss())
        .pipe(rename(function(path) {
            path.basename += "-rtl";
            return path;
        }))
        .pipe(gulp.dest(build.styles));
});

// LESS THEMES
gulp.task('styles:themes', function() {
    return gulp.src(source.styles.themes.main)
        .pipe(less({
            paths: [source.styles.themes.dir]
        }))
        .on("error", handleError)
        .pipe(gulp.dest(build.styles));
});

// BOOSTRAP
gulp.task('bootstrap', function() {
    return gulp.src(source.bootstrap.main)
        .pipe(less({
            paths: [source.bootstrap.dir]
        }))
        .on("error", handleError)
        .pipe(gulp.dest(build.styles));
});

// JADE
gulp.task('templates:app', function() {
    return gulp.src(source.templates.app.files)
        .pipe(changed(build.templates.app, { extension: '.html' }))
        .pipe(jade())
        .on("error", handleError)
        .pipe(prettify({
            indent_char: ' ',
            indent_size: 3,
            unformatted: ['a', 'sub', 'sup', 'b', 'i', 'u']
        }))
        // .pipe(htmlify({
        //     customPrefixes: ['ui-']
        // }))
        // .pipe(w3cjs( W3C_OPTIONS ))
        .pipe(gulp.dest(build.templates.app))
        ;
});

// JADE
gulp.task('templates:pages', function() {
    return gulp.src(source.templates.pages.files)
        .pipe(changed(build.templates.pages, { extension: '.html' }))
        .pipe(jade())
        .on("error", handleError)
        .pipe(prettify({
            indent_char: ' ',
            indent_size: 3,
            unformatted: ['a', 'sub', 'sup', 'b', 'i', 'u']
        }))
        // .pipe(htmlify({
        //     customPrefixes: ['ui-']
        // }))
        // .pipe(w3cjs( W3C_OPTIONS ))
        .pipe(gulp.dest(build.templates.pages))
        ;
});

// JADE
gulp.task('templates:views', function() {
    return gulp.src(source.templates.views.files)
        .pipe(changed(build.templates.views, { extension: '.html' }))
        .pipe(jade())
        .on("error", handleError)
        .pipe(prettify({
            indent_char: ' ',
            indent_size: 3,
            unformatted: ['a', 'sub', 'sup', 'b', 'i', 'u']
        }))
        // .pipe(htmlify({
        //     customPrefixes: ['ui-']
        // }))
        // .pipe(w3cjs( W3C_OPTIONS ))
        .pipe(gulp.dest(build.templates.views))
        ;
});

//---------------
// WATCH
//---------------

// Rerun the task when a file changes
gulp.task('watch', function() {
  livereload.listen();

  gulp.watch(source.scripts.watch,           ['scripts:app']);
  gulp.watch(source.styles.app.watch,        ['styles:app', 'styles:app:rtl']);
  gulp.watch(source.styles.themes.watch,     ['styles:themes']);
  gulp.watch(source.bootstrap.watch,         ['styles:app']); //bootstrap
  gulp.watch(source.templates.pages.watch,   ['templates:pages']);
  gulp.watch(source.templates.views.watch,   ['templates:views']);
  gulp.watch(source.templates.app.watch,     ['templates:app']);

  gulp.watch([
      '../app/**'
  ]).on('change', function(event) {
      livereload.changed();
      // console.log('File', event.path, 'was', event.type);
      // console.log('Triggering LiveReload..');
  });

});

//---------------
// DEFAULT TASK
//---------------

gulp.task('default', [
          'scripts:vendor',
          'scripts:app',
          'styles:app',
          'styles:app:rtl',
          'styles:themes',
          'templates:app',
          'templates:pages',
          'templates:views',
          'watch'
        ]);


// Error handler
function handleError(err) {
  console.log(err.toString());
  this.emit('end');
}

// Mini gulp plugin to flip css (rtl)
function flipcss(opt) {
  
  if (!opt) opt = {};

  // creating a stream through which each file will pass
  var stream = through.obj(function(file, enc, cb) {
    if(file.isNull()) return cb(null, file);

    if(file.isStream()) {
        console.log("todo: isStream!");
    }

    var flippedCss = flip(String(file.contents), opt);
    file.contents = new Buffer(flippedCss);
    cb(null, file);
  });

  // returning the file stream
  return stream;
}
