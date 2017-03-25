'use strict';

var browserify = require('browserify');
var gulp = require('gulp');
var source = require('vinyl-source-stream');
var buffer = require('vinyl-buffer');
var uglify = require('gulp-uglify');
var sourcemaps = require('gulp-sourcemaps');
var gutil = require('gulp-util');
var del = require('del');
var reactify = require('reactify');

var paths = {
  javascript: 'js/**/*'
}

gulp.task('clean', function() {
  return del(['./static']);
});

gulp.task('homepage-js', function() {
  var b = browserify({
    entries: './js/homepage.js',
    debug: true
  });

  return b.transform(reactify)
    .bundle()
    .pipe(source('homepage.js'))
    .pipe(buffer())
    .pipe(sourcemaps.init({loadMaps: true}))
      .pipe(uglify())
      .on('error', gutil.log)
    .pipe(sourcemaps.write('./'))
    .pipe(gulp.dest('./static/js/'));
});

gulp.task('javascript', ['homepage-js']);

gulp.task('build', ['javascript'])

gulp.task('watch', function() {
  gulp.watch(paths.javascript, ['javascript']);
});

gulp.task('default', ['watch', 'build']);
